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

## Usage

### {Use Case 1}

{1-2 sentence summary of this use case}

1. {Step 1 to complete use case}
1. {Step 2 to complete use case}
1. ... <!-- number of steps and use cases may vary -->

## Vision and Roadmap

The vision for this template is to simplify the process of creating open source python projects with high quality codebase and mechanisms that promote smart and collaborative project governance. This project aims to fulfill this vision by:

- Adopting a common python package file structure
- Implementing basic linting and code quality checks
- Reinforcing compliance with those code quality checks using CI/CD
- Providing templates for things like documentation, issues, and pull requests
- Offering pythonic implementation examples of common data structures and scripting tasks like:
  - Creating classes, methods, and functions
  - Setting up unit and integration testing
  - Reading and writing to files

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
