# pylint: disable=unused-argument
import pandas as pd

from dgs_fiscal.etl.contract_management import ContractData, UpdateResult


class MockContractManagement:
    """Mock version of ContractManagement class for CLI tests"""

    def get_sharepoint_data(self):
        """Mock version of get_sharepoint_data() for CLI tests"""
        return ContractData(vendor={}, contract={}, po={})

    def get_citibuy_data(self):
        """Mock version of get_citibuy_data() for CLI tests"""
        return ContractData(vendor={}, contract={}, po={})

    def update_vendor_list(self, old, new):
        """Mock version of update_vendor_lists() for CLI tests"""
        return UpdateResult(mapping={}, upserts={}, results={})

    def update_contract_list(self, old, new, vendor_lookup):
        """Mock version of update_contract_list() for CLI tests"""
        return UpdateResult(mapping={}, upserts={}, results={})

    def update_po_list(self, old, new, vendor_lookup, contract_lookup):
        """Mock version of update_po_list() for CLI tests"""
        return UpdateResult(mapping={}, upserts={}, results={})


class MockAgingReport:
    """Mock version of ContractManagement class for CLI tests"""

    def get_citibuy_data(self, invoice_window: int = 365) -> pd.DataFrame:
        """Mock version of get_citibuy_data() for CLI tests"""
        print(invoice_window)
        return pd.DataFrame({"Col A": [1, 2, 3], "Col B": ["A", "B", "C"]})

    def get_receipt_queue(self, receipt_window: int = 365) -> pd.DataFrame:
        """Mock version of get_citibuy_data() for CLI tests"""
        print(receipt_window)
        return pd.DataFrame({"Col A": [1, 2, 3], "Col B": ["A", "B", "C"]})

    def update_sharepoint(self, df: pd.DataFrame, report_name: str):
        """Mock version of update_po_list() for CLI tests"""
        print(report_name)
