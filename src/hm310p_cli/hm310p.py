# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-
"""Hanmantek power supply command line control module.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
# stdlib imports
import time

# third party imports
import minimalmodbus
import serial

# project imports
from .hm310p_constants import PowerState, PowerSupplyError
from .hm310p_regdefs import HM3xxpRegisters as Reg


class HM310P(minimalmodbus.Instrument):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, portname: str, slaveaddress: int) -> None:
        """Instrument class for HM310P.

        Args:
            portname (str): port name
            slaveaddress (int): slave address in the range 1 to 247

        """
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

        #: address of device, default is 1
        self.unit_id: int = slaveaddress
        #: used modbus transistion mode
        self.method: str = minimalmodbus.MODE_RTU
        #: baudrate
        self.baudrate: int = 9600
        #: bytesize
        self.bytesize: int = 8
        #: startbits
        self.startbits: int = 1
        #: stopbits
        self.stopbits: int = 1
        #: parity
        self.parity: str = serial.PARITY_NONE
        #: parity
        self.number_of_channels: int = 6
        #: timeout
        self.timeout: float = 0.25
        #: used serial port or device file respectivily
        self.port: str = portname

        self.max_voltage: float = 32.00
        self.min_voltage: float = 0.00
        self.max_current: float = 10.000
        self.min_current: float = 0.000

        self.mask_decimals_voltage: int = 0x0F00
        self.mask_decimals_current: int = 0x00F0
        self.mask_decimals_power: int = 0x000F
        self.shift_decimals_voltage: int = 8
        self.shift_decimals_current: int = 4
        self.shift_decimals_power: int = 0
        self.number_of_decimals_voltage: int = 0
        self.number_of_decimals_current: int = 0
        self.number_of_decimals_power: int = 0
        self.max_decimal_nums: int = 0
        self.min_decimal_nums: int = 0

        self.serial.baudrate = self.baudrate
        self.serial.startbits = self.startbits
        self.serial.stopbits = self.stopbits
        self.serial.parity = serial.PARITY_NONE
        self.serial.bytesize = self.bytesize
        self.serial.timeout = self.timeout
        self.close_port_after_each_call = False

        # get model
        self.model: int = self.get_model()
        if self.model == 3010:  # model HM310p
            self.max_current = 10.000
        else:
            self.max_current = 5.000

        # init member variables
        tmp_decimals = self.get_decimals()

        minimalmodbus._check_int(tmp_decimals)

        self.number_of_decimals_voltage = (
            tmp_decimals & self.mask_decimals_voltage
        ) >> self.shift_decimals_voltage
        self.number_of_decimals_current = (
            tmp_decimals & self.mask_decimals_current
        ) >> self.shift_decimals_current
        self.number_of_decimals_power = (
            tmp_decimals & self.mask_decimals_power
        ) >> self.shift_decimals_power
        # for input validation
        self.min_decimal_nums = 0
        self.max_decimal_nums = max(
            [
                self.number_of_decimals_voltage,
                self.number_of_decimals_current,
                self.number_of_decimals_power,
            ]
        )

        print(self)
        print(self.get_protectstate())
        print(self.model)
        print(self.number_of_decimals_voltage)
        print(self.number_of_decimals_current)
        print(self.number_of_decimals_power)

    def set_voltage(self, vol: float, chan: int = 0) -> None:
        """Sets voltage value."""
        minimalmodbus._check_numerical(
            vol, self.min_voltage, self.max_voltage, description="voltage value"
        )
        minimalmodbus._check_int(chan, 0, self.number_of_channels, "channel number")

        if chan == 0:
            reg = Reg.PS_SetVoltage
        elif chan == 1:
            reg = Reg.M1_V
        elif chan == 2:
            reg = Reg.M2_V
        elif chan == 3:
            reg = Reg.M3_V
        elif chan == 4:
            reg = Reg.M4_V
        elif chan == 5:
            reg = Reg.M5_V
        elif chan == 6:
            reg = Reg.M6_V

        self.write_register(reg, vol, self.number_of_decimals_voltage)

    def get_voltage_set(self, chan: int = 0) -> float:
        """Returns preset voltage value."""
        minimalmodbus._check_int(chan, 0, self.number_of_channels, "channel number")

        if chan == 0:
            reg = Reg.PS_SetVoltage
        elif chan == 1:
            reg = Reg.M1_V
        elif chan == 2:
            reg = Reg.M2_V
        elif chan == 3:
            reg = Reg.M3_V
        elif chan == 4:
            reg = Reg.M4_V
        elif chan == 5:
            reg = Reg.M5_V
        elif chan == 6:
            reg = Reg.M6_V

        return self.read_register(reg, self.number_of_decimals_voltage)

    def get_voltage_out(self) -> float:
        """Returns output voltage."""
        return self.read_register(Reg.PS_Voltage, self.number_of_decimals_voltage)

    def set_current(self, cur: float, chan: int = 0) -> None:
        """Sets maximum output current."""
        minimalmodbus._check_numerical(
            cur, self.min_current, self.max_current, description="current value"
        )
        minimalmodbus._check_int(chan, 0, self.number_of_channels, "channel number")

        if chan == 0:
            reg = Reg.PS_SetCurrent
        elif chan == 1:
            reg = Reg.M1_A
        elif chan == 2:
            reg = Reg.M2_A
        elif chan == 3:
            reg = Reg.M3_A
        elif chan == 4:
            reg = Reg.M4_A
        elif chan == 5:
            reg = Reg.M5_A
        elif chan == 6:
            reg = Reg.M6_A

        self.write_register(reg, cur, self.number_of_decimals_current)

    def get_current_out(self) -> float:
        """Returns output current."""
        return self.read_register(Reg.PS_Current, self.number_of_decimals_current)

    def get_current_set(self, chan: int = 0) -> float:
        """Returns preset current."""
        minimalmodbus._check_int(chan, 0, self.number_of_channels, "channel number")

        if chan == 0:
            reg = Reg.PS_SetCurrent
        elif chan == 1:
            reg = Reg.M1_A
        elif chan == 2:
            reg = Reg.M2_A
        elif chan == 3:
            reg = Reg.M3_A
        elif chan == 4:
            reg = Reg.M4_A
        elif chan == 5:
            reg = Reg.M5_A
        elif chan == 6:
            reg = Reg.M6_A

        return self.read_register(reg, self.number_of_decimals_current)

    def get_powerstate(self) -> PowerState:
        """Returns power state."""
        return PowerState(self.read_register(Reg.PS_PowerSwitch))

    def set_powerstate(self, state: PowerState) -> None:
        """Sets power state."""
        if state not in [PowerState.On, PowerState.Off]:
            raise ValueError(repr(PowerSupplyError.ValueErrorPowerState))
        self.write_register(Reg.PS_PowerSwitch, state.value)

    def toggle_powerstate(self, state: PowerState) -> None:
        """Toggles On-Off State."""
        if state == PowerState.On:
            self.set_powerstate(PowerState.Off)
        elif state == PowerState.Off:
            self.set_powerstate(PowerState.On)
        else:
            raise ValueError(repr(PowerSupplyError.ValueErrorPowerState))

    def set_ocp(self, cur: float) -> None:
        """Sets over current protection."""
        minimalmodbus._check_numerical(
            cur, self.min_current, self.max_current, description="current value"
        )
        self.write_register(Reg.PS_ProtectCur, cur, self.number_of_decimals_current)

    def get_ocp(self) -> float:
        """Returns over current protection."""
        return self.read_register(Reg.PS_ProtectCur, self.number_of_decimals_current)

    def set_ovp(self, vol: float) -> None:
        """Sets over voltage protection."""
        minimalmodbus._check_numerical(
            vol, self.min_voltage, self.max_voltage, description="voltage value"
        )
        self.write_register(Reg.PS_ProtectVol, vol, self.number_of_decimals_voltage)

    def get_ovp(self) -> float:
        """Returns over voltage protection."""
        return self.read_register(Reg.PS_ProtectVol, self.number_of_decimals_voltage)

    def get_protectstate(self) -> int:
        """Returns protect state."""
        return self.read_register(Reg.PS_ProtectStat)

    def get_model(self) -> int:
        """Returns model."""
        return self.read_register(Reg.PS_Model)

    def get_decimals(self) -> int:
        """Returns decimals."""
        return self.read_register(Reg.PS_Decimals)

    def get_slave_address(self) -> int:
        """Returns decimals."""
        return self.read_register(Reg.PS_Device)

    def _reset_powersupply(self) -> None:
        self.set_powerstate(PowerState.Off)
        for chan in range(self.number_of_channels + 1):
            self.set_voltage(self.min_voltage, chan)
            time.sleep(self.timeout)
            self.set_current(self.min_current, chan)

    def _set_safe_output_state(self, vol: float, cur: float) -> None:
        # protstate = self.get_protectstate()
        for chan in range(self.number_of_channels + 1):
            self.set_voltage(vol, chan)
            self.set_current(cur, chan)
            time.sleep(self.timeout)
