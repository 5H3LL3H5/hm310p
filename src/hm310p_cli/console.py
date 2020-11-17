# src/hm310p_cli/console.py
# -*- coding: utf-8 -*-

# third party imports
import click

# project imports
from . import __version__
from .hm310p import HM310P
from .hm310p_constants import PowerState

iMinA = 0.0
iMaxA = 10.0
uMinV = 0.0
uMaxV = 32.0


@click.command()
@click.option("-p", "--port", type=str, help="Serial device", required=True)
@click.option(
    "-s",
    "--powerstate",
    type=click.Choice(["on", "off"], case_sensitive=False),
    help="Power supply switch",
    required=True,
)
@click.option(
    "-V",
    "--vout",
    type=click.FloatRange(uMinV, uMaxV),
    help="Output voltage in Volt",
    required=True,
)
@click.option(
    "--ovp",
    type=click.FloatRange(uMinV, uMaxV),
    help="Over voltage protection value in Volt",
    required=False,
)
@click.option(
    "-I",
    "--iout",
    type=click.FloatRange(iMinA, iMaxA),
    help="Output current in Ampere",
    required=True,
)
@click.option(
    "--ocp",
    type=click.FloatRange(iMinA, iMaxA),
    help="Over current protection value in Ampere",
    required=False,
)
@click.option("-D", "--debug", is_flag=True)
@click.version_option(version=__version__)
def main(
    port: str,
    powerstate: str,
    vout: float,
    ovp: float,
    iout: float,
    ocp: float,
    debug: bool,
) -> None:
    """The hm310p command line interface"""

    adaptedOVP = ""
    adaptedOCP = ""

    if ovp is None:
        """ovp value five percent higher than vout value"""
        ovp = 1.05 * vout
        adaptedOVP = " => OVP not given, set 5% larger than Vout"
        if ovp > uMaxV:
            ovp = uMaxV
            adaptedOVP = f" => OVP not given, clipped to {uMaxV:02.3f} V"

    if ocp is None:
        """ocp value five percent higher than iout value"""
        ocp = 1.05 * iout
        adaptedOCP = " => OCP not given, set 5% larger than Iout"
        if ocp > iMaxA:
            ocp = iMaxA
            adaptedOCP = f" => OCP not given, clipped to {iMaxA:02.3f} A"

    if ovp < vout:
        raise click.BadOptionUsage("ovp", f"OVP={ovp:02.3f} V < Vout={vout:02.3f} V")

    if ocp < iout:
        raise click.BadOptionUsage("ocp", f"OCP={ocp:02.3f} A < Iout={iout:02.3f} A")

    if debug:
        click.secho("Welcome to the hm310p command line interface.", fg="green")
        click.echo(f"Port\t\t: {port}")
        click.echo(f"Powerstate\t: {powerstate}")
        click.echo(f"Vout\t\t: {vout:02.3f} V")
        click.echo(f"OVP\t\t: {ovp:02.3f} V" + adaptedOVP)
        click.echo(f"Iout\t\t: {iout:02.3f} A")
        click.echo(f"OCP\t\t: {ocp:02.3f} A" + adaptedOCP)

    psupply = HM310P(port, 1)

    if powerstate == "on":
        psupply.set_opp()
        print(f"OPP: {psupply.get_opp():2.3f}")
        # Iocp = 0.750 A, Iout = 0.5 A, Uout = 24 V, Uovp = 24.05 V
        psupply.set_ocp(ocp)
        psupply.set_current(iout)
        psupply.set_ovp(ovp)
        psupply.set_voltage(vout, "Preset")
        psupply.get_voltage("Output")
        psupply.get_voltage("Protection")
        psupply.set_opp(iout * vout)
        print(f"OPP CONSOLE: {psupply.get_opp():2.3f}")
        psupply.set_powerstate(PowerState.On)
        psupply.set_voltage_and_current_of_channel_list(
            ["Output", "Preset", "Protection", "M1", "M2", "M3", "M4", "M5", "M6"],
            10.10,
            5.555,
        )
    else:
        psupply.set_voltage(0)
        psupply.set_current(0)
        psupply.set_powerstate(PowerState.Off)
