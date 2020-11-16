# src/hm310p_cli/hm310p_constants.py
# -*- coding: utf-8 -*-

from enum import auto, Enum, IntEnum, unique

UNIT = 0x01


@unique
class PowerSupplyError(Enum):
    NoError = auto()
    ConnectError = auto()
    DisconnectError = auto()
    ReadErrorDecimalRegister = auto()
    ReadErrorPowerState = auto()
    ReadErrorProtectState = auto()
    ReadErrorModel = auto()
    ReadErrorDecimals = auto()
    ReadErrorSlaveAddress = auto()
    ReadErrorOVP = auto()
    ReadErrorOCP = auto()
    ReadErrorCurrentOut = auto()
    ReadErrorCurrentSet = auto()
    ReadErrorVoltageOut = auto()
    ReadErrorVoltageSet = auto()
    WriteErrorPowerState = auto()
    WriteErrorOVP = auto()
    WriteErrorOCP = auto()
    WriteErrorCurrent = auto()
    WriteErrorCurrentSet = auto()
    WriteErrorCurrentOut = auto()
    WriteErrorVoltage = auto()
    WriteErrorVoltageSet = auto()
    WriteErrorVoltageOut = auto()
    ValueErrorPowerState = auto()
    ValueErrorCurrent = auto()
    ValueErrorCurrentOut = auto()
    ValueErrorCurrentSet = auto()
    ValueErrorVoltage = auto()
    ValueErrorChannel = auto()


@unique
class PowerState(IntEnum):
    Off = 0x00
    On = 0x01
    Invalid = 0x02
