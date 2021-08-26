# {short title of solved problem and solution}

- **Status:** Accepted
- **Last Modified:**: 2021-08-26
- **Related Issue:** #5

## Context and Problem Statement

Historically the DGS Fiscal team has built and stored the Priority Vendor Aging report using a Excel workbook hosted on SharePoint. This made sense when that report was being updated manually using Excel workbooks submitted by the vendor, but with the automation of that update workflow, we have an opportunityt to explore other storage formats.

As a result, we need to decide how and where to store the new Priority Vendor Aging Report so that it can be updated automatically on a weekly basis, while also being accessed between updates by members of the DGS Fiscal team.

## Decision Drivers

- Report format is familiar/accessible to DGS Fiscal team members
- Report supports filtering based on a variety of criteria
- Report can be updated both programmatically and manually
- Report data can be visualized in PowerBI
- Report columns can be updated quickly and easily

## Considered Options

- Excel Workbook in SharePoint
- SharePoint List

## Decision Outcome <!-- REQUIRED -->

We've chosen to use a SharePoint list as the storage format because it supports features like commenting on individual records, creating default filters, and a more reliable update mechanism through the Graph API.

### Positive Consequences <!-- OPTIONAL -->

- SharePoint list items can be added/updated individually, reducing the risk of accidentally overwriting or deleting existing invoices when updating the report.
- SharePoint list items support comments, which allow users to provide narrative updates about the status of individual invoices in the report.
- SharePoint lists support multiple pre-configured filters and allow multiple users to filter the same list in different ways without overwriting each other's view.
- SharePoint lists can still be exported to Excel documents if the user wants to conduct more detailed analysis on the list items.
- SharePoint lists can also be connected to a PowerBI dashboard.

### Negative Consequences <!-- OPTIONAL -->

- SharePoint lists less familiar to some members of the DGS Fiscal team and it may take them some time to adjust to using them.
- SharePoint lists may be harder or more expensive from a memory standpoint to load into memory than Excel workbooks.
- Use of SharePoint lists depends heavily on the Graph API so this strategy is somewhat vulnerable to changes in or deprecation of API features.

## Pros and Cons of the Options

### Excel Workbook

- **Pro**
  - DGS Fiscal staff are familiar and comfortable with Excel workbooks.
  - DGS BPIO has workarounds for reading and writing data to an Excel workbook on SharePoint that does not depend on Graph API.
  - There are a number of very stable Python packages for working with Excel workbooks.
- **Cons**
  - Because updating the contents of a workbook involves re-writing an entire worksheet, it's easy to accidentally overwite or delete data.
  - The existing workarounds we have for Excel are unstable and non-ideal.
  - Excel workbooks don't allow multiple users to filter them differently at the same time.
