# tests/test_console.py
import click.testing
import pytest

from hm310p_cli import console

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_main_succeeds_with_debug(runner):
    result = runner.invoke(console.main, "--debug")
    assert result.exit_code == 0

def test_main_succeeds_with_input_ovp_ocp_vout_iout(runner):
    result = runner.invoke(console.main, "--ovp 10 --ocp 10 --vout 10 --iout 10")
    assert result.exit_code == 0

def test_main_succeeds_with_input_ovp_ocp_smaller_then_vout_iout(runner):
    result = runner.invoke(console.main, "--ovp 8 --ocp 8 --vout 10 --iout 10")
    assert result.exit_code == 0

def test_main_succeeds_with_input_vout_to_max(runner):
    result = runner.invoke(console.main, "--vout 30")
    assert result.exit_code == 0

def test_main_succeeds_with_input_iout_to_max(runner):
    result = runner.invoke(console.main, "--iout 10")
    assert result.exit_code == 0

def test_main_succeeds_with_input_vout_range_max(runner):
    result = runner.invoke(console.main, "--vout 30")
    assert result.exit_code == 0

def test_main_succeeds_with_input_vout_range_min(runner):
    result = runner.invoke(console.main, "--vout 0")
    assert result.exit_code == 0

def test_main_fails_with_input_vout_out_of_range_max(runner):
    result = runner.invoke(console.main, "--vout 50")
    assert result.exit_code != 0

def test_main_fails_with_input_vout_out_of_range_min(runner):
    result = runner.invoke(console.main, "--vout -50")
    assert result.exit_code != 0

def test_main_succeeds_with_input_iout_out_range_max(runner):
    result = runner.invoke(console.main, "--iout 10")
    assert result.exit_code == 0

def test_main_succeeds_with_input_iout_out_range_min(runner):
    result = runner.invoke(console.main, "--iout 0")
    assert result.exit_code == 0

def test_main_fails_with_input_iout_out_of_range_max(runner):
    result = runner.invoke(console.main, "--iout 50")
    assert result.exit_code != 0

def test_main_fails_with_input_iout_out_of_range_min(runner):
    result = runner.invoke(console.main, "--iout -50")
    assert result.exit_code != 0
