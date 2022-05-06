# DGS Fiscal Automations

<details open="open">
<summary>Table of Contents</summary>

<!-- TOC -->

- [DGS Fiscal Automations](#dgs-fiscal-automations)
  - [About this Project](#about-this-project)
    - [Made With](#made-with)
    - [Relevant Documents](#relevant-documents)
    - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Secret Configuration](#secret-configuration)
  - [Usage](#usage)
    - [Contract Management Report](#contract-management-report)
    - [Aging Report](#aging-report)
    - [Prompt Payment](#prompt-payment)
  - [Vision and Roadmap](#vision-and-roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Maintainers](#maintainers)
  - [Acknowledgements](#acknowledgements)

<!-- /TOC -->

</details>

## About this Project

DGS Fiscal Automations is a series of Extract, Transform, and Load (ETL) workflows that aggregates the data the DGS Fiscal team needs to report on the status of vendor contracts and invoices. This repository centralizes the code for those workflows and simplifies the process of executing them by exposing a CLI entry point for each ETL process.

### Made With

- **Project Dependencies**
  - [O365](https://github.com/O365/python-o365) - A third party package for managing calls to the Microsoft Graph API
  - [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - A python toolkit and Object Relational Mapper (ORM) for managing connections to relational databases
  - [pandas](https://github.com/pandas-dev/pandas) - A python toolkit commonly used to manipulate and analyze tabular data
- **Development Dependencies**
  - [tox](https://tox.readthedocs.io/en/latest/) - Automates and standardizes the creation of testing environments.
  - [pytest](https://docs.pytest.org/en/6.2.x/) - Simplifies the design and execution of both unit and integration testing.
  - [black](https://black.readthedocs.io/en/stable/) - Autoformats code for consistent styling.
  - [flake8](https://flake8.pycqa.org/en/latest/) - Checks that code complies with PEP8 style guidelines.
  - [pylint](https://www.pylint.org/) - Checks that code follows idiomatic best practices for Python.
  - [pre-commit](https://pre-commit.com/) - Runs code quality checks before code is committed.

### Relevant Documents

- [Invoice Fulfillment Process](docs/diagrams/invoice-fulfillment/invoice-fulfillment-process.md)
- [Architecture Decision Records](docs/adr/)
- [Project Scoping Document](docs/project-scope.md)
- [Data Dictionary](docs/data-dictionary.md)

### Project Structure

The list below represents a summary of important files and directories within the project.

- [`.github/`](.github/) Contains templates for issues and pull requests as well as configuration files for GitHub Actions
- [`app/`](app/) Contains the scripts and other files that comprise the main codebase for this project
  - [`src/dgs_fiscal/`](app/src/dgs_fiscal/) The main python package for this project
    - [`etl/`](app/src/dgs_fiscal/etl/) The Extract Transform Load sub-package which contains modules for each of the DGS Fiscal ETL workflows that can be run with this project, i.e. the Contract Management Report, Aging Report, and Prompt Payment Report.
    - [`systems/`](app/src/dgs_fiscal/systems/) The systems sub-package which contains modules for programmatically interfacing with each of the systems involved in the DGS Fiscal Workflows, i.e. CitiBuy, CoreIntegrator, SharePoint, and Integrify.
  - [`tests/`](app/tests/) Contains the unit and integration tests used to assess the quality of the code base
  - [`setup.py`](app/setup.py) Details about the package in `src/dgs_fiscal/` and the file that facilitates installation of that package
  - [`requirements.txt`](app/requirements.txt) The project's development dependencies
- [`docs/`](docs/) Contains documentation about the project
  - [`adr/`](docs/adr/) Contains key architectural decisions for the project
  - [`diagrams/`](docs/diagrams/) Contains diagrams referenced in the docs and in the `README.md`
  - [`project-scope.md`](docs/project-scope.md) An overview of the project and its goals

## Getting Started

### Prerequisites

- Python installed on your local machine, preferably a version between 3.8 and 3.9

In order to check which version of python you have installed, run the following in your command line, and the output should look something like this:

> **NOTE**: in all of the code blocks below, lines preceded with $ indicate commands you should enter in your command line (excluding the $ itself), while lines preceded with > indicate the expected output from the previous command.

```
$ python --version
> Python 3.9.0
```

If you receive an error message, or the version of python you have installed is not between 3.7 and 3.9, consider using a tool like [pyenv](https://github.com/pyenv/pyenv) (on Mac/Linux) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) (on Windows) to manage multiple python installations.

### Installation

1. [Clone the repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) on your local machine: `git clone https://github.com/department-of-general-services/priority-vendor-aging-report.git`
1. Change directory into the `app/` sub-directory of the cloned project: `cd priority-vendor-aging-report/app`
1. Create a new virtual environment: `python -m venv env`
1. Activate the virtual environment
   - On Mac/Linux: `source env/bin/activate`
   - On Windows: `.\env\Scripts\activate`
1. Install this package in editable mode by running `pip install -e .` which makes changes made to scripts within this package available without re-installing it.
1. Install the other dependencies required to contribute to the project: `pip install -r requirements.txt`
1. Install `pre-commit` to autoformat your code: `pre-commit install`
1. Execute all tests by running `tox` All tests should pass with an output that ends in something like this:
   ```
    py39: commands succeeded
    lint: commands succeeded
    checkdeps: commands succeeded
    pytest: commands succeeded
    coverage: commands succeeded
    congratulations :)
   ```

### Secret Configuration

1. Contact Billy Daly to receive access to the credentials for the Microsoft Daemon app that has permissions use the Graph API for this project.
1. Create a file called `.secrets.toml` at the root of the `app/` sub-directory:
   - On Mac/Linux: `touch .secrets.toml`
   - On Windows: `echo > .secrets.toml`
1. Open that new file in your text editor and add the credentials to it. The format should look something like this:
   ```toml
   [DEVELOPMENT]
   client_id = "test_id"
   client_secret = "test_secret"
   tenant_id = "12345"
   site_id = "acme.sharepoint.com,12345,67890"
   host_name = "acme.sharepoint.com"
   site_name = "AcmeSite"
   drive_id = "45678"
   ```
1. Test that the config variables are loading correctly. Enter all of the lines that begin with a `$` or `>>>`
   ```bash
   $ python
   >>> from aging_report.config import settings
   >>> settings.client_id
   'test_id'  # This should match the value you added to .secrets.toml
   >>> settings.secret
   'test_secret'  # This should match the value you added to .secrets.toml
   ```
1. If the config variables are loading correctly, try running the integration tests: `pytest tests/integration_tests`
1. All tests should pass with an output that looks something like this:
   ```
   ======================== test session starts ==============================
   collected 5 items
   tests/integration_tests/sharepoint/test_list.py .....                [100%]

   ======================== 5 passed in 1.86s ================================
   ```

## Usage

### Contract Management Report

The Contract Management Report allows the DGS Fiscal team and contract managers in other divisions to monitor the burn rate and expiration of active Master Blanket Purchase Orders with DGS vendors. It involves exporting the list of Master Blanket POs, Purchase Order Releases, and the associated vendors from CitiBuy and uploading them to SharePoint.

To run this workflow execute the command `dgs_fiscal contract_management` from the command line, which should print the following steps to the terminal as the workflow executes:

```bash
$ dgs_fiscal contract_management
Starting the contract management workflow
Getting data from Citibuy and Sharepoint
Updating the vendor list
Updating the contract list
Updating the PO list
Workflow ran successfully
```

### Aging Report

The Aging Report is a report that the DGS Fiscal team uses to monitor and inform priority vendors of the status of their outstanding invoices in the accounts payable process. This report depends on integrating data from multiple information systems involved in the AP process, including Integrify, CoreIntegrator, and CitiBuy. In order to simplify the process of generating that report, this workflow extracts data on invoices and receipts from CitiBuy and uploads them to SharePoint.

To run this workflow, execute the command `dgs_fiscal aging_report` from the command line, which should print the following steps to the terminal as the workflow executes:

```bash
$ dgs_fiscal aging_report
Starting the aging report workflow
Exporting invoice and receipt data from CitiBuy
Uploading the exported data to SharePoint
Workflow ran successfully
```

### Prompt Payment

The Prompt Payment Report is a standard report from CoreIntegrator that shows the set of invoices that have been received by BAPS but need to be receipted by the DGS Fiscal team. This workflow involves scraping the most recent Prompt Payment Report from CoreIntegrator, then reconciling it with the previous version of the report in SharePoint, during this reconciliation process receipted and paid invoices are dropped from the report, new invoices are added, and comments on the remaining invoices are carried over to the new report, which is then re-uploaded to SharePoint.

The command to run this workflow is still in development.

## Vision and Roadmap

The vision for this project is to create a single repository

- Adding all invoices that get processed through Integrify to to a SharePoint list that will become the single source of truth.
- Scraping information about these invoices from each of the systems involved in processing invoice payments, namely:
  - Integrify
  - CitiBuy
  - CoreIntegrator
- Updating the invoices in the SharePoint list with information scraped from each of the sites listed above.
- Map the SharePoint list to a PowerBI Dashboard so that the members of the DGS Fiscal Office can report on summary statistics about outstanding invoices.

For a more detailed breakdown of the feature roadmap and other development priorities please reference the following links:

- [Feature Roadmap](https://github.com/department-of-general-services/priority-vendor-aging-report/projects/1)
- [Architecture Decisions](https://github.com/department-of-general-services/priority-vendor-aging-report/projects/2)
- [Bug Fixes](https://github.com/department-of-general-services/priority-vendor-aging-report/projects/3)
- [All Issues](https://github.com/department-of-general-services/priority-vendor-aging-report/issues)

## Contributing

Contributions are always welcome! We encourage contributions in the form of discussion on issues in this repo and pull requests for improvements to documentation and code.

See [CONTRIBUTING.md](CONTRIBUTING.md) for ways to get started.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Maintainers

- [@widal001](https://github.com/widal001)

## Acknowledgements

- [Python Packaging Authority Sample Project](https://github.com/pypa/sampleproject)
- [Best README Template](https://github.com/othneildrew/Best-README-Template)
