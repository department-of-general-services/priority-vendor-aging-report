import typer

from dgs_fiscal import etl

# instantiate typer app
app = typer.Typer()


@app.command(name="hello")
def hello_world(name: str):
    """Prints 'Hello, {name}' to the console"""
    typer.echo(f"Hello, {name}")


@app.command(name="contract_management")
def run_contract_management_etl():
    """Run the contract management workflow"""

    # init the ETL workflow class
    typer.echo("Starting the contract management workflow")
    contract_etl = etl.ContractManagement()

    # get data from CitiBuy and SharePoint
    typer.echo("Getting data from Citibuy and Sharepoint")
    sharepoint_data = contract_etl.get_sharepoint_data()
    citibuy_data = contract_etl.get_citibuy_data()

    # update the Vendor list in SharePoint
    typer.echo("Updating the vendor list")
    vendor_output = contract_etl.update_vendor_list(
        old=sharepoint_data.vendor,
        new=citibuy_data.vendor,
    )

    # update the Contract list in SharePoint
    typer.echo("Updating the contract list")
    contract_output = contract_etl.update_contract_list(
        old=sharepoint_data.contract,
        new=citibuy_data.contract,
        vendor_lookup=vendor_output.mapping,
    )

    # update the PO list in SharePoint
    typer.echo("Updating the PO list")
    contract_etl.update_po_list(
        old=sharepoint_data.po,
        new=citibuy_data.po,
        vendor_lookup=vendor_output.mapping,
        contract_lookup=contract_output.mapping,
    )
    typer.echo("Workflow ran successfully")
