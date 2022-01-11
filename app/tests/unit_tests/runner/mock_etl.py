# pylint: disable=unused-argument
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
