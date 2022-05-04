import subprocess

import pytest
from typer.testing import CliRunner

from dgs_fiscal import etl
from dgs_fiscal.runner import app
from tests.unit_tests.runner import mock_etl


@pytest.fixture(scope="module", name="runner")
def fixture_cli_runner():
    """Returns a test runner for Typer CLI apps"""
    return CliRunner()


@pytest.fixture(name="contract_etl")
def fixture_contract_mgmt_etl(monkeypatch):
    """Monkeypatches the ContractManagement ETL class with the test class
    MockContractManagement to prevent calls to Citibuy or SharePoint
    """
    monkeypatch.setattr(
        etl,
        "ContractManagement",
        mock_etl.MockContractManagement,
    )


@pytest.fixture(name="aging_etl")
def fixture_aging_etl(monkeypatch):
    """Monkeypatches the ContractManagement ETL class with the test class
    MockContractManagement to prevent calls to Citibuy or SharePoint
    """
    monkeypatch.setattr(
        etl,
        "AgingReport",
        mock_etl.MockAgingReport,
    )


def test_entrypoint():
    """Tests that the entrypoints specified in setup.py work correctly"""
    # execution
    output = subprocess.run(
        ["dgs_fiscal", "hello", "Billy"],
        check=True,
        capture_output=True,
    )
    stdout = output.stdout.decode("utf-8")
    # validation
    assert output.returncode == 0
    assert "Hello, Billy" in stdout


def test_hello(runner):
    """Tests that the hello command executes correctly

    Validates the following conditions:
    - The command executes with exit code 0 (success)
    - The correct messages are printed to the console
    """
    # execution
    result = runner.invoke(app, ["hello", "Billy"])
    print(result.stdout)
    # validation
    assert result.exit_code == 0
    assert "Hello, Billy" in result.stdout


def test_contract_management(
    runner, contract_etl
):  # pylint: disable=unused-argument
    """Tests that the contract_management command

    Validates the following conditions:
    - The command executes with exit code 0 (success)
    - The correct messages are printed to the console
    """
    # setup
    messages = [
        "Starting the contract management workflow",
        "Getting data from Citibuy and Sharepoint",
        "Updating the vendor list",
        "Updating the contract list",
        "Updating the PO list",
        "Workflow ran successfully",
    ]
    # execution
    result = runner.invoke(app, ["contract_management"])
    print(result.stdout)
    # validation
    assert result.exit_code == 0
    for message in messages:
        assert message in result.stdout


def test_aging_report(runner, aging_etl):  # pylint: disable=unused-argument
    """Tests that the contract_management command

    Validates the following conditions:
    - The command executes with exit code 0 (success)
    - The correct messages are printed to the console
    """
    # setup
    messages = [
        "Starting the aging report workflow",
        "Exporting invoice and receipt data from CitiBuy",
        "Uploading the exported data to SharePoint",
        "Workflow ran successfully",
    ]
    # execution
    result = runner.invoke(app, ["aging_report"])
    print(result.stdout)
    # validation
    assert result.exit_code == 0
    for message in messages:
        assert message in result.stdout
