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
from typing import List

# third party imports
import minimalmodbus
import serial

# project imports
from hm310p_cli.hm310p_constants import PowerState, PowerSupplyError
from hm310p_cli.hm310p_regdefs import HM3xxpRegisters as Reg


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

        self._channel_map = {
            "Info": {
                "pswitch": Reg.PS_PowerSwitch,
                "pstat": Reg.PS_ProtectStat,
                "model": Reg.PS_Model,
                "cd": Reg.PS_ClassDetail,
                "decs": Reg.PS_Decimals,
            },
            "Protection": {
                "v": Reg.PS_ProtectVol,
                "c": Reg.PS_ProtectCur,
                "ph": Reg.PS_ProtectPowH,
                "pl": Reg.PS_ProtectPowL,
            },
            "Output": {
                "v": Reg.PS_Voltage,
                "c": Reg.PS_Current,
                "ph": Reg.PS_PowerH,
                "pl": Reg.PS_PowerL,
                "pc": Reg.PS_PowerCal,
            },
            "Preset": {
                "v": Reg.PS_SetVoltage,
                "c": Reg.PS_SetCurrent,
                "ts": Reg.PS_SetTimeSpan,
            },
            "M1": {
                "v": Reg.M1_V,
                "c": Reg.M1_A,
                "ts": Reg.M1_Time,
                "en": Reg.M1_Enable,
                "no": Reg.M1_NextOffset,
            },
            "M2": {
                "v": Reg.M2_V,
                "c": Reg.M2_A,
                "ts": Reg.M2_Time,
                "en": Reg.M2_Enable,
                "no": Reg.M2_NextOffset,
            },
            "M3": {
                "v": Reg.M3_V,
                "c": Reg.M3_A,
                "ts": Reg.M3_Time,
                "en": Reg.M3_Enable,
                "no": Reg.M3_NextOffset,
            },
            "M4": {
                "v": Reg.M4_V,
                "c": Reg.M4_A,
                "ts": Reg.M4_Time,
                "en": Reg.M4_Enable,
                "no": Reg.M4_NextOffset,
            },
            "M5": {
                "v": Reg.M5_V,
                "c": Reg.M5_A,
                "ts": Reg.M5_Time,
                "en": Reg.M5_Enable,
                "no": Reg.M5_NextOffset,
            },
            "M6": {
                "v": Reg.M6_V,
                "c": Reg.M6_A,
                "ts": Reg.M6_Time,
                "en": Reg.M6_Enable,
                "no": Reg.M6_NextOffset,
            },
        }

        self.max_voltage: float = 32.00
        self.min_voltage: float = 0.00
        self.max_current: float = 10.000
        self.min_current: float = 0.000
        self.max_power: float = 310.000
        self.min_power: float = 0.000

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

        # info = self.read_registers(Reg.PS_PowerSwitch, 5)
        print(self)

    def set_voltage(self, value: float, channel: str = "Preset") -> None:
        """Sets voltage value."""
        register = self._lookup_register_value(channel, "v")
        minimalmodbus._check_numerical(
            value, self.min_voltage, self.max_voltage, description="voltage value"
        )
        self.write_register(register, value, self.number_of_decimals_voltage)

    def get_voltage(self, channel: str = "Preset") -> float:
        """Returns preset voltage value."""
        register = self._lookup_register_value(channel, "v")
        return self.read_register(register, self.number_of_decimals_voltage)

    def set_current(self, value: float, channel: str = "Preset") -> None:
        """Sets maximum output current."""
        register = self._lookup_register_value(channel, "c")
        minimalmodbus._check_numerical(
            value, self.min_current, self.max_current, description="current value"
        )
        self.write_register(register, value, self.number_of_decimals_current)

    def get_current(self, channel: str = "Preset") -> float:
        """Returns preset current."""
        register = self._lookup_register_value(channel, "c")
        return self.read_register(register, self.number_of_decimals_current)

    def set_power(self, value: float, channel: str = "Protection") -> None:
        """Sets power value."""
        register = self._lookup_register_value(channel, "ph")
        minimalmodbus._check_numerical(
            value, self.min_power, self.max_power, description="power value"
        )
        self.write_long(register, int(value * 10 ** self.number_of_decimals_power))

    def get_power(self, channel: str = "Output") -> float:
        """Gets power value."""
        register = self._lookup_register_value(channel, "ph")
        return self.read_long(register) / 10 ** self.number_of_decimals_power

    def set_voltage_and_current_of_channel_list(
        self, channels: List, voltage: float, current: float
    ) -> None:
        """Sets voltage and current valus for channel list."""
        valid_channels = [
            "Output",
            "Preset",
            "Protection",
            "M1",
            "M2",
            "M3",
            "M4",
            "M5",
            "M6",
        ]

        if not all(item in valid_channels for item in channels):
            raise ValueError("Invalid channel in paramter list.")

        minimalmodbus._check_numerical(
            voltage, self.min_voltage, self.max_voltage, description="voltage value"
        )

        minimalmodbus._check_numerical(
            current, self.min_current, self.max_current, description="current value"
        )

        for chan in set(channels):
            register = self._lookup_register_value(chan, "v")
            self.write_registers(
                register,
                [
                    int(voltage * 10 ** self.number_of_decimals_voltage),
                    int(current * 10 ** self.number_of_decimals_current),
                ],
            )

    def get_powerstate(self) -> PowerState:
        """Returns power state."""
        return PowerState(self.read_register(Reg.PS_PowerSwitch.value))

    def set_powerstate(self, state: PowerState) -> None:
        """Sets power state."""
        if state not in [PowerState.On, PowerState.Off]:
            raise ValueError(repr(PowerSupplyError.ValueErrorPowerState))
        self.write_register(Reg.PS_PowerSwitch.value, state.value)

    def toggle_powerstate(self) -> None:
        """Toggles On-Off State."""
        state = self.get_powerstate()
        if state == PowerState.On:
            self.set_powerstate(PowerState.Off)
        elif state == PowerState.Off:
            self.set_powerstate(PowerState.On)
        else:
            raise ValueError(repr(PowerSupplyError.ValueErrorPowerState))

    def set_ocp(self, cur: float) -> None:
        """Sets over current protection."""
        self.set_current(cur, "Protection")

    def get_ocp(self) -> float:
        """Returns over current protection."""
        return self.get_current("Protection")

    def set_ovp(self, vol: float) -> None:
        """Sets over voltage protection."""
        self.set_voltage(vol, "Protection")

    def get_ovp(self) -> float:
        """Returns over voltage protection."""
        return self.get_voltage("Protection")

    def set_opp(self, opp: float = None) -> None:
        """Set over power protection."""
        if opp is None:
            opp = self.get_voltage() * self.get_current()
        self.set_power(opp, "Protection")

    def get_opp(self) -> float:
        """Returns over power protection."""
        return self.get_power("Protection")

    def get_protectstate(self) -> int:
        """Returns protect state."""
        return self.read_register(Reg.PS_ProtectStat.value)

    def get_model(self) -> int:
        """Returns model."""
        return self.read_register(Reg.PS_Model.value)

    def get_decimals(self) -> int:
        """Returns decimals."""
        return self.read_register(Reg.PS_Decimals.value)

    def get_slave_address(self) -> int:
        """Returns decimals."""
        return self.read_register(Reg.PS_Device.value)

    def _check_channel(self, chan: str, chan_key: str) -> None:
        """Checks if channel string is valid key in _channel_map."""
        if chan not in self._channel_map:
            raise KeyError(f"Invalid channel name {chan}")
        if chan_key not in self._channel_map[chan]:
            raise KeyError(f"Invalid channel property {chan_key}")

    def _lookup_register_value(self, chan: str, chan_key: str) -> int:
        self._check_channel(chan, chan_key)
        return self._channel_map[chan][chan_key].value  # lookup of register value
