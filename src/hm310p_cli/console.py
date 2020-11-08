# src/hm310p_cli/console.py
# -*- coding: utf-8 -*-

import click

from . import __version__

iMinA=0.0
iMaxA=10.0
uMinV=0.0
uMaxV=30.0

@click.command()
@click.option('-p',
              '--port',
              type=str,
              help='Serial device',
              required=True)
@click.option('-s',
              '--powerstate',
              type=click.Choice(['on', 'off'], case_sensitive=False),
              help='Power supply switch',
              required=True)
@click.option('-V',
              '--vout',
              type=click.FloatRange(uMinV, uMaxV),
              help="Output voltage in Volt",
              required=True)
@click.option('--ovp',
              type=click.FloatRange(uMinV, uMaxV),
              help="Over voltage protection value in Volt",
              required=False)
@click.option('-I',
              '--iout',
              type=click.FloatRange(iMinA, iMaxA),
              help="Output current in Ampere",
              required=True)
@click.option('--ocp',
              type=click.FloatRange(iMinA, iMaxA),
              help="Over current protection value in Ampere",
              required=False)
@click.option('-D', '--debug', is_flag=True) 
@click.version_option(version=__version__)

def main(port: str, powerstate: str, vout: float, ovp: float, iout: float, ocp: float, debug: bool) -> int:
    """The hm310p command line interface"""

    if ovp is None:
        """ovp value five percent higher than vout value"""
        ovp = 1.05 * vout
        if ovp>uMaxV:
            ovp=uMaxV

    if ocp is None:
        """ocp value five percent higher than iout value"""
        ocp = 1.05 * iout
        if ocp>iMaxA:
            ocp=iMaxA

    adaptedOVP=""
    if ovp<vout:
        ovp=vout
        adaptedOVP="\t(Adapted to Vout)"

    adaptedOCP=""
    if ocp<iout:
        ocp=iout
        adaptedOCP="\t(Adapted to Iout)"

    if debug:
        click.secho("Welcome to the hm310p command line interface.",
                     fg="green")
        click.echo(f"Port\t\t: {port}")
        click.echo(f"Powerstate\t: {powerstate}")
        click.echo(f"Vout\t\t: {vout:02.3f} V")
        click.echo(f"OVP\t\t: {ovp:02.3f} V" + adaptedOVP) 
        click.echo(f"Iout\t\t: {iout:02.3f} A")
        click.echo(f"OCP\t\t: {ocp:02.3f} A" + adaptedOCP)
