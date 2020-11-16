from enum import IntEnum, unique


@unique
class HM3xxpRegisters(IntEnum):
    """
    Register addresses of HanmaTek devices

    source: https://github.com/mckenm/HanmaTekPSUCmd/wiki/Registers
    """

    PS_PowerSwitch = 0x0001  # R/W, 0/1 Power output/stop setting
    PS_ProtectStat = 0x0002
    """R, Bit mask (OCP 0x02/OVP 0x01)
    Ptotect status
    SCP:OTP:OPP:OCP:OVP
    OVP：Over voltage protection
    OCP：Over current protection
    OPP：Over power protection
    OTP：Over tempreture protection
    SCP：short-circuit protection
    """
    PS_Model = 0x0003  # R, 3010 (HM310P)
    PS_ClassDetail = 0x0004  # R, value 0x4b58 (19280)
    PS_Decimals = 0x0005
    """R, value 0x233
    Note 2: Decimal point digit capacity
    information as follow:
    voltage current power decimal point digit capacity
    Dat=ShowPN /((2<<8)/(3<<4)/(3<<0))
    =>0.00V 0.000A 0.000W
    For example when read:0x0233 (563)
    mean that voltage 2 decimal,current 3 decimal,power 3 decimal.
    """
    PS_Voltage = 0x0010  # R, 2Decimal Voltage display value
    PS_Current = 0x0011  # R, 3Decimal Current display value
    PS_PowerH = 0x0012  # R, 3Decimal Power display value (high 16 bit)
    PS_PowerL = 0x0013  # R, 3Decimal Power display value (low 16 bit )
    PS_PowerCal = 0x0014  # ?
    PS_ProtectVol = 0x0020  # RW, 2Decimal OVP Set over volate protect value
    PS_ProtectCur = 0x0021  # RW, 2Decimal OCP Set over current protect value
    PS_ProtectPowH = (
        0x0022  # RW, 2Decimal OPP Set over power protect value (high 16 bit)
    )
    PS_ProtectPowL = (
        0x0023  # RW, 2Decimal OPP Set over power protect value (low 16 bit)
    )
    PS_SetVoltage = 0x0030  # RW, 2Dec Set voltage
    PS_SetCurrent = 0x0031  # RW, 3Dec Set current
    PS_SetTimeSpan = 0x0032  # RW, ????
    PS_PowerStat = 0x8801  # ?
    PS_defaultShow = 0x8802  # ?
    PS_SCP = 0x8803  # ?
    PS_Buzzer = 0x8804  # RW, Buzzer enable
    PS_Device = 0x9999  # R/W, Set communication address - SlaveID : 1 default
    PS_SDTime = 0xCCCC  # ?
    PS_UL = 0xC110  # ?, 11d / xC111 = 1
    PS_UH = 0xC11E  # ?, 3200d / xC11F = 1
    PS_IL = 0xC120  # ?, 21 / xC121=1
    PS_IH = 0xC12E  # ?, 10100/ xC12F=1
    M1_V = 0x1000  # also PSM_Voltage, RW, Voltage - for M1
    M1_A = 0x1001  # also PSM_Voltage, RW, Current limte
    M1_Time = 0x1002  # also PSM_Voltage, RW, Time Span
    M1_Enable = 0x1003  # also PSM_Voltage, RW, Enable/Disable in List
    PSM_NextOffset = 0x1004  # ?
    M2_V = 0x1010  # RW, Voltage - for M2
    M2_A = 0x1011  # RW, Current limte
    M2_Time = 0x1012  # RW, Time Span
    M2_Enable = 0x1013  # RW, Enable/Disable in List
    M3_V = 0x1020  # RW, Voltage - for M3
    M3_A = 0x1021  # RW, Current limte
    M3_Time = 0x1022  # RW, Time Span
    M3_Enable = 0x1023  # RW, Enable/Disable in List
    M4_V = 0x1030  # RW, Voltage - for M4
    M4_A = 0x1031  # RW, Current limte
    M4_Time = 0x1032  # RW, Time Span
    M4_Enable = 0x1033  # RW, Enable/Disable in List
    M5_V = 0x1040  # RW, Voltage - for M5
    M5_A = 0x1041  # RW, Current limte
    M5_Time = 0x1042  # RW, Time Span
    M5_Enable = 0x1043  # RW, Enable/Disable in List
    M6_V = 0x1050  # RW, Voltage - for M5
    M6_A = 0x1051  # RW, Current limte
    M6_Time = 0x1052  # RW, Time Span
    M6_Enable = 0x1053  # RW, Enable/Disable in List

    @classmethod
    def has_key(cls, name: str) -> bool:
        """Test if a key is in this enum."""
        return name in cls.__members__

    @classmethod
    def has_value(cls, value: int) -> bool:
        """Test if a value is in this enum."""
        return value in cls._value2member_map_.value
