# Priority Vendor Aging Report

<details open="open">
<summary>Table of Contents</summary>

<!-- TOC -->

- [About this Project](#about-this-project)
  - [Made With](#made-with)
  - [Relevant Documents](#relevant-documents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [This Template](#this-template)
  - [{Use Case 1}](#use-case-1)
- [Contributing](#contributing)
- [License](#license)
- [Maintainers](#maintainers)
- [Acknowledgements](#acknowledgements)

<!-- /TOC -->

</details>

## About this Project

The Priority Vendor Aging Report is a weekly report that allows the DGS Fiscal team to track the status of the overdue invoices submitted by the agency's highest priority vendors. This project seeks to automate the process of updating that report with information aggregated from each of the systems that an invoice passes through during the requisition and fulfillment workflow.

### Made With

<!-- TODO: Replace this list with your most critical dependencies -->

- [tox](https://tox.readthedocs.io/en/latest/) - Automates and standardizes the creation of testing environments.
- [pytest](https://docs.pytest.org/en/6.2.x/) - Simplifies the design and execution of both unit and integration testing.
- [black](https://black.readthedocs.io/en/stable/) - Autoformats code for consistent styling.
- [flake8](https://flake8.pycqa.org/en/latest/) - Checks that code complies with PEP8 style guidelines.
- [pylint](https://www.pylint.org/) - Checks that code follows idiomatic best practices for Python.
- [pre-commit](https://pre-commit.com/) - Runs code quality checks before code is committed.

### Relevant Documents

- [Project Folder in SharePoint](https://bmore.sharepoint.com/:f:/r/sites/DGS-BPIO/Shared%20Documents/Projects/Fiscal%20-%20Priority%20Vendor%20Aging?csf=1&web=1&e=Y9q3gN) **Note:** Requires Baltimore City account access
- [Architecture Decision Records](docs/adrs)
- [Project Scoping Document](docs/project-scope.md)
- [Data Dictionary](docs/data-dictionary.md)

## Getting Started

### Prerequisites

- Python installed on your local machine, preferably a version between 3.7 and 3.9

In order to check which version of python you have installed, run the following in your command line, and the output should look something like this:

> **NOTE**: in all of the code blocks below, lines preceded with $ indicate commands you should enter in your command line (excluding the $ itself), while lines preceded with > indicate the expected output from the previous command.

```
$ python --version
> Python 3.9.0
```

If you receive an error message, or the version of python you have installed is not between 3.7 and 3.9, consider using a tool like [pyenv](https://github.com/pyenv/pyenv) (on Mac/Linux) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) (on Windows) to manage multiple python installations.

### Installation

1. [Clone the repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) on your local machine: `git clone https://github.com/department-of-general-services/priority-vendor-aging-report.git`
1. Change directory into the cloned project: `cd priority-vendor-aging-report`
1. Create a new virtual environment: `python -m venv env`
1. Activate the virtual environment
   - On Mac/Linux: `source env/bin/activate`
   - On Windows: `.\env\Scripts\activate`
1. Install this package in editable mode by running `pip install -e .` which makes changes made to scripts within this package available without re-installing it.
1. Install the other dependencies required to contribute to the project: `pip -r requirements.txt`
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
1. Create a file called `.secrets.toml` at the root of the project directory:
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
   report_id = "45678"
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
   tests/integration_tests/test_aging_report.py .....                   [100%]

   ======================== 5 passed in 1.86s ================================
   ```

## Usage

### Get all invoices

To retrieve a list of all of the invoices in the Priority Vendor Aging SharePoint list complete the following steps:

1. Initiate a new Python interpreter in your terminal: `python`
1. Import the `Client` class: `from aging_report.sharepoint import Client`
1. Instantiate the `Client` class: `client = Client()`
1. Get an instance of the `AgingReportList` class: `report = client.get_aging_report()`
1. Query the list of invoices: `invoices = report.get_invoices()`
1. Print the invoice fields:
```
for invoice in invoices:
    print(invoice.fields)
```

The full example looks like this:

```python
from aging_report.sharepoint import Client

client = Client()
report = client.get_aging_report()
invoices = report.get_invoices()
for i in invoices:
    print(invoice.fields)
```

## Vision and Roadmap

The vision for this project is to create a single source of truth for information about invoices throughout the fulfillment pipeline, so that the DGS Fiscal Office can more easily track and report on the status of outstanding invoices. This project aims to fulfill this vision by:

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
