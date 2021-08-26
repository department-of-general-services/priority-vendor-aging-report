# Graph API Library: Python O365

- **Status:** Accepted
- **Last Modified:**: 2021-08-26
- **Related Issue:** #7

## Context and Problem Statement

Now that we have access to credentials for a daemon app registered on our Microsoft tenant, we need to select a specific library that will allow us to authenticate with Microsoft and utilize the Graph API. There are a number of official Microsoft libraries that only manage authentication, as well as some third-party libraries that manage both authentication and Graph API calls directly.

As a result, we need to choose a single library that we want to facilitate use of the Graph API for this project.

## Decision Drivers <!-- RECOMMENDED -->

- Number of Graph API services supported
- Clarity and completeness of documentation
- Level of support and active maintenance
- Usability and simplicity of the package's API

## Considered Options

- [MSAL Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [Azure Identity Client](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)
- [Python-O365](https://github.com/O365/python-o365)

## Decision Outcome

We've chosen to utilize Python-O365 in this project because it provides a robust set of classes and methods for all of the main Graph API endpoints we'll need for this project and allows us to avoid having to write and maintain our own package for interacting with SharePoint via the Graph API.

### Positive Consequences

- Removes the need to build and maintain our own internal package for interacting with Graph API.
- Provides a very simple interface for working with SharePoint lists, drives, and files.
- Moderate adoption by the open source community (~900 stars on GitHub)

### Negative Consequences

- Doesn't yet have documentation for the SharePoint module, which requires reading through the source code to understand the package API.
- Not as actively maintained as the other packages, most recent contributions were from May.
- Not an official Micrososft library, which means that it isn't directly maintained by Microsoft developers and that it's vulnerable to deprecation.

## Pros and Cons of the Options

### [MSAL Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)

- **Pro**
  - An official package of Microsoft recommended in their docs
  - Actively maintained, last commit was made in the last week.
  - Serves as the foundation for the Azure Identity library
- **Cons**
  - Not widely used on its own (~300 stars on GitHub)
  - Very small feature set, using this library would require us to build out all of the functionality for using Graph API directly
  - Documentation is sparse and not always accurate.

### [Azure Identity Client](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)

{example | description | pointer to more information | …} <!-- OPTIONAL -->

- **Pro**
  - Strong adoption amongst the open source community (~2.1k stars on GitHub)
  - Actively maintained, last commit was made in the last week.
  - An official package of Microsoft recommended in their docs.
  - Slightly simpler package API than MSAL.
- **Cons**
  - Very small feature set, using this library would require us to build out all of the functionality for using Graph API directly.
