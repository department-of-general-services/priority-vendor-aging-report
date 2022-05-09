import typer

# instantiate typer app
app = typer.Typer()


@app.command(name="hello")
def hello_world(name: str):
    """Prints 'Hello, {name}' to the console"""
    typer.echo(f"Hello, {name}")


@app.command(name="contract_management")
def run_contract_management_etl():
    """Run the contract management workflow"""

    from dgs_fiscal import etl  # pylint: disable=import-outside-toplevel

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


@app.command(name="aging_report")
def run_aging_report_etl():
    """Run the Aging Report workflow"""

    from dgs_fiscal import etl  # pylint: disable=import-outside-toplevel

    # init the ETL workflow class
    typer.echo("Starting the aging report workflow")
    aging_etl = etl.AgingReport()

    # get data from CitiBuy and SharePoint
    typer.echo("Exporting invoice and receipt data from CitiBuy")
    invoice_data = aging_etl.get_citibuy_data(invoice_window=365)
    receipt_data = aging_etl.get_receipt_queue(receipt_window=1200)

    # get data from CitiBuy and SharePoint
    typer.echo("Uploading the exported data to SharePoint")
    aging_etl.update_sharepoint(invoice_data, "InvoiceExport")
    aging_etl.update_sharepoint(receipt_data, "ReceiptExport")

    typer.echo("Workflow ran successfully")


@app.command(name="prompt_payment")
def run_prompt_payment_etl():
    """Run the Prompt Payment Report Workflow"""

    from dgs_fiscal import etl  # pylint: disable=import-outside-toplevel

    # init the ETL workflow class
    typer.echo("Starting the prompt payment report workflow")
    prompt_etl = etl.PromptPayment()

    # Scrape the new report from CoreIntegrator
    typer.echo("Scraping the new report from CoreIntegrator")
    new_report = prompt_etl.get_new_report()

    # Download the old report from SharePoint
    old_report = prompt_etl.get_old_report()

    # Archive the copies of those reports
    typer.echo("Archiving the snapshots of the report")
    prompt_etl.update_sharepoint(
        file_path=new_report.file,
        report_name="scraped_report",
        folder_name="core_integrator",
    )
    prompt_etl.update_sharepoint(
        file_path=old_report.file,
        report_name="old_report",
        folder_name="commented_invoices",
    )

    typer.echo("Workflow ran successfully")
