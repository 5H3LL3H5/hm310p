# tests/test_console.py
import click.testing
import pytest

from hm310p_cli import console

sport:   str = '/dev/ttyS0'
pstate:  str = 'off'
vout:  float = 12.00
iout:  float = 1.000
ovp:   float = 12.50
ocp:   float = 1.100
iMinA: float = 0.0
iMaxA: float = 10.0
uMinV: float = 0.0
uMaxV: float = 30.0

arglist=[
    f'--port={sport}',
    f'--powerstate=off',
    f'--vout={vout:02.2f}',
    f'--iout={iout:02.3f}',
    f'--ovp={ovp:02.2f}',
    f'--ocp={ocp:02.3f}',
    '--debug'
]

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_fails_without_args(runner):
    result = runner.invoke(console.main)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:'])
    assert result.exit_code != 0

def test_main_fails_without_arg_port(runner):
    tmplist = list(arglist)
    del tmplist[0]
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:', '-p', '--port'])
    assert result.exit_code != 0

def test_main_fails_without_arg_powerstate(runner):
    tmplist = list(arglist)
    del tmplist[1]
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:', '-s', '--powerstate'])
    assert result.exit_code != 0

def test_main_fails_without_arg_vout(runner):
    tmplist = list(arglist)
    del tmplist[2]
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:', '-V', '--vout'])
    assert result.exit_code != 0

def test_main_fails_without_arg_iout(runner):
    tmplist = list(arglist)
    del tmplist[3]
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:', '-I', '--iout'])
    assert result.exit_code != 0

def test_main_fails_with_invalid_powerstate(runner):
    tmplist = list(arglist)
    tmplist[1] = '--powerstate=onoff'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in ['Usage', 'Error:', '-s', '--powerstate'])
    assert result.exit_code != 0

def test_main_succeeds_without_debug(runner):
    tmplist = list(arglist)
    del tmplist[6]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert result.exit_code == 0

def test_main_succeeds_with_powerstate_on(runner):
    tmplist = list(arglist)
    tmplist[1] = '--powerstate=on'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Port\t\t: {sport}',
               'Powerstate\t: on',
               f'Vout\t\t: {vout:02.3f} V',
               f'OVP\t\t: {ovp:02.3f} V',
               f'Iout\t\t: {iout:02.3f} A',
               f'OCP\t\t: {ocp:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_without_arg_ovp(runner):
    tmplist = list(arglist)
    del tmplist[4]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert result.exit_code == 0

def test_main_succeeds_without_arg_ocp(runner):
    tmplist = list(arglist)
    del tmplist[5]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert result.exit_code == 0

def test_main_succeeds_without_arg_ovp_and_without_arg_ocp(runner):
    tmplist = list(arglist)
    del tmplist[4:6]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert result.exit_code == 0

def test_main_succeeds_with_arg_ovp_and_with_arg_ocp(runner):
    tmplist = list(arglist)
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Port\t\t: {sport}',
               f'Powerstate\t: {pstate}',
               f'Vout\t\t: {vout:02.3f} V',
               f'OVP\t\t: {ovp:02.3f} V',
               f'Iout\t\t: {iout:02.3f} A',
               f'OCP\t\t: {ocp:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_without_arg_ovp_but_with_arg_ocp(runner):
    tmplist = list(arglist)
    del tmplist[4]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Port\t\t: {sport}',
               f'Powerstate\t: {pstate}',
               f'Vout\t\t: {vout:02.3f} V',
               f'OVP\t\t: {vout*1.05:02.3f} V => OVP not given,',
               f'Iout\t\t: {iout:02.3f} A',
               f'OCP\t\t: {ocp:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_arg_ovp_but_without_arg_ocp(runner):
    tmplist = list(arglist)
    del tmplist[5]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Port\t\t: {sport}',
               f'Powerstate\t: {pstate}',
               f'Vout\t\t: {vout:02.3f} V',
               f'OVP\t\t: {ovp:02.3f} V',
               f'Iout\t\t: {iout:02.3f} A',
               f'OCP\t\t: {iout*1.05:02.3f} A => OCP not given,',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_arg_ovp_and_with_arg_ocp(runner):
    tmplist = list(arglist)
    del tmplist[4:6]
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Port\t\t: {sport}',
               f'Powerstate\t: {pstate}',
               f'Vout\t\t: {vout:02.3f} V',
               f'OVP\t\t: {vout*1.05:02.3f} V => OVP not given,',
               f'Iout\t\t: {iout:02.3f} A',
               f'OCP\t\t: {iout*1.05:02.3f} A => OCP not given,',
           ])
    assert result.exit_code == 0

def test_main_succeeds_ovp_clipped_to_upper_interval_limit(runner):
    tmplist = list(arglist)
    del tmplist[4:6]
    tmp_vout=uMaxV/(1.05-0.0001)
    tmplist[2] = f'--vout={tmp_vout:02.3f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {tmp_vout:02.3f} V',
               f'OVP\t\t: {uMaxV:02.3f} V => OVP not given, clipped',
           ])
    assert result.exit_code == 0

def test_main_succeeds_ocp_clipped_to_upper_interval_limit(runner):
    tmplist = list(arglist)
    del tmplist[4:6]
    tmp_iout=iMaxA/(1.05-0.0001)
    tmplist[3] = f'--iout={tmp_iout:02.3f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Iout\t\t: {tmp_iout:02.3f} A',
               f'OCP\t\t: {iMaxA:02.3f} A => OCP not given, clipped',
           ])
    assert result.exit_code == 0

def test_main_succeeds_ovp_and_ocp_clipped_to_upper_interval_limit(runner):
    tmplist = list(arglist)
    del tmplist[4:6]
    tmp_vout=uMaxV/(1.05-0.0001)
    tmp_iout=iMaxA/(1.05-0.0001)
    tmplist[2] = f'--vout={tmp_vout:02.3f}'
    tmplist[3] = f'--iout={tmp_iout:02.3f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {tmp_vout:02.3f} V',
               f'OVP\t\t: {uMaxV:02.3f} V => OVP not given, clipped',
               f'Iout\t\t: {tmp_iout:02.3f} A',
               f'OCP\t\t: {iMaxA:02.3f} A => OCP not given, clipped',
           ])
    assert result.exit_code == 0


def test_main_fails_with_ovp_smaller_than_vout(runner):
    tmplist = list(arglist)
    tmplist[4] = f'--ovp={vout-1:02.3f}'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: OVP={vout-1:02.3f} V < Vout={vout:02.3f} V'
           ])
    assert result.exit_code != 0

def test_main_fails_with_ocp_smaller_than_iout(runner):
    tmplist = list(arglist)
    tmplist[5] = f'--ocp={iout-1:02.3f}'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: OCP={iout-1:02.3f} A < Iout={iout:02.3f} A'
           ])
    assert result.exit_code != 0

def test_main_fails_with_vout_out_of_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = '--vout=50'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_iout_out_of_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[3] = '--iout=50'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_ovp_out_of_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[4] = '--ovp=50'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_ocp_out_of_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[5] = '--ocp=50'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_vout_out_of_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = '--vout=-1'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_iout_out_of_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[3] = '--iout=-1'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_ovp_out_of_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[4] = '--ovp=-1'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_fails_with_ocp_out_of_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[5] = '--ocp=-1'
    result = runner.invoke(console.main, tmplist)
    assert result.exception
    assert all(x in result.output for x in [
               'Usage',
               f'Error: Invalid value'
           ])
    assert result.exit_code != 0

def test_main_succeeds_with_vout_at_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = f'--vout={uMinV:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {uMinV:02.3f} V',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_vout_and_ovp_at_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = f'--vout={uMinV:f}'
    tmplist[4] = f'--ovp={uMinV:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {uMinV:02.3f} V',
               f'OVP\t\t: {uMinV:02.3f} V',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_iout_at_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[3] = f'--iout={iMinA:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Iout\t\t: {iMinA:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_iout_and_ocp_at_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[3] = f'--iout={iMinA:f}'
    tmplist[5] = f'--ocp={iMinA:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Iout\t\t: {iMinA:02.3f} A',
               f'OCP\t\t: {iMinA:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_vout_ovp_iout_and_ocp_at_lower_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = f'--vout={uMinV:f}'
    tmplist[3] = f'--iout={iMinA:f}'
    tmplist[4] = f'--ovp={uMinV:f}'
    tmplist[5] = f'--ocp={iMinA:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {uMinV:02.3f} V',
               f'OVP\t\t: {uMinV:02.3f} V',
               f'Iout\t\t: {iMinA:02.3f} A',
               f'OCP\t\t: {iMinA:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_vout_and_ovp_at_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = f'--vout={uMaxV:f}'
    tmplist[4] = f'--ovp={uMaxV:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {uMaxV:02.3f} V',
               f'OVP\t\t: {uMaxV:02.3f} V',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_iout_and_ocp_at_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[3] = f'--iout={iMaxA:f}'
    tmplist[5] = f'--ocp={iMaxA:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Iout\t\t: {iMaxA:02.3f} A',
               f'OCP\t\t: {iMaxA:02.3f} A',
           ])
    assert result.exit_code == 0

def test_main_succeeds_with_vout_ovp_iout_and_ocp_at_upper_interval_limit(runner):
    tmplist = list(arglist)
    tmplist[2] = f'--vout={uMaxV:f}'
    tmplist[3] = f'--iout={iMaxA:f}'
    tmplist[4] = f'--ovp={uMaxV:f}'
    tmplist[5] = f'--ocp={iMaxA:f}'
    result = runner.invoke(console.main, tmplist)
    assert not result.exception
    assert all(x in result.output for x in [
               f'Vout\t\t: {uMaxV:02.3f} V',
               f'OVP\t\t: {uMaxV:02.3f} V',
               f'Iout\t\t: {iMaxA:02.3f} A',
               f'OCP\t\t: {iMaxA:02.3f} A',
           ])
    assert result.exit_code == 0
