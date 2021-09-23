# Priority Vendor Aging Report

- **Version:** 0.2.1
- **Status:** Final
- **Last Modified:** 2021-09-23

<details open="closed">
<summary>Table of Contents</summary>

<!-- TOC -->

- [Priority Vendor Aging Report](#priority-vendor-aging-report)
  - [Overview](#overview)
    - [Problem Statement](#problem-statement)
    - [Objectives](#objectives)
    - [Background](#background)
      - [_Invoice Fulfillment Workflow_](#_invoice-fulfillment-workflow_)
      - [_Priority Vendor Aging Report Workflow_](#_priority-vendor-aging-report-workflow_)
      - [_Pain Points with the Current Workflow_](#_pain-points-with-the-current-workflow_)
  - [User Stories](#user-stories)
    - [Fiscal Admin Team Member](#fiscal-admin-team-member)
    - [Fiscal Leadership](#fiscal-leadership)
    - [Priority Vendor](#priority-vendor)
  - [Feasibility Assessment](#feasibility-assessment)
    - [Feasibility Criteria](#feasibility-criteria)
    - [Practicality Criteria](#practicality-criteria)
  - [Deliverable Summary](#deliverable-summary)
    - [Feasibility Assessment](#feasibility-assessment-1)
    - [Priority Vendor Submission Form](#priority-vendor-submission-form)
    - [Priority Vendor Aging Automation Workflow](#priority-vendor-aging-automation-workflow)
    - [Priority Vendor Aging Dashboard](#priority-vendor-aging-dashboard)

<!-- /TOC -->

</details>

## Overview

### Problem Statement

When payments to vendors for outstanding invoices are significantly delayed, those vendors often contact the DGS Fiscal team asking about the status of their invoice. Because each invoice passes through multiple technical systems during the fulfillment process, a member of the Fiscal team has to manually search for information about each priority invoice across all those systems and compile it in a single Excel workbook. This current process is time intensive, error prone, and makes it difficult to understand exactly where an invoice is stuck and what needs to be done to move it forward.

_As a result, the DGS Fiscal team needs a more efficient means of identifying all of the priority invoices that are overdue, reflecting where in the fulfillment process they are stuck, and understanding what actions need to be taken to move them forward in that process._

### Objectives

- Create a single point of entry for vendors to flag priority invoices that are overdue, which immediately adds each invoice to the Priority Vendor Aging Report.
- Automate as many of the steps as possible involved in generating and updating information about the invoices on the Priority Vendor Aging report
- Deliver a dashboard based on the Priority Vendor Aging report that allows the DGS Fiscal team to gain insight into major bottlenecks in the invoice fulfillment process.
- Create a mechanism for communicating updates to vendors about the status of invoices that are overdue.

### Background

#### _Invoice Fulfillment Workflow_

The process for remitting payment to vendors for invoices they submit involves coordinating actions amongst several agencies and individuals. A detailed breakdown of the process – including the system in which these steps occur, the actions that are taken, and the set of stakeholders involved at that step – can be found in the Appendix, but the following summary highlights the key stages and systems involved.

1. **Outlook:** Vendor sends invoice to DGS
   1. Integrify: Invoice is prepared for CitiBuy processing
   1. Invoice is uploaded to Integrify
   1. Invoice is assigned to analyst for CitiBuy processing
1. **CitiBuy:** Generate Purchase Order and receipting
   1. Requisition is submitted and approved in CitiBuy
   1. CitiBuy PO is generated and sent to vendor
   1. PO invoice receipting is completed
1. **CoreIntegrator:** BAPS executes payment to vendor

#### _Priority Vendor Aging Report Workflow_

The current process for creating and updating the Priority Vendor Aging Report involves a lot of manual steps completed by a member of the DGS Fiscal admin team. The core tasks involved in this process are outlined below:

1. A member of the DGS Fiscal admin team sends vendors a template of information that vendors need to fill out for their report to be added to the Priority Vendor Aging Report.
1. When invoice payments are overdue, the vendor fills out that template and submits it to a member of the DGS Fiscal admin team via email.
1. A member of the DGS Fiscal admin team searches for this invoice in each of the systems involved in the invoice fulfillment workflow to understand at what stage and why this invoice is stuck in that process.
1. That information gets added to a shared Excel workbook known as the Priority Vendor Aging Report in SharePoint.
1. Steps 4 and 5 are repeated for every invoice on the Priority Vendor Aging Report on a bi-weekly basis.

#### _Pain Points with the Current Workflow_

There are several challenges with the current process for creating and maintaining the Priority Vendor Aging Report. A summary of those headaches can be found below:

- Because the process is so manual and involves searching for information in several different technical systems, maintaining this report consumes a significant amount of the DGS Fiscal admin team member’s time each month.
- Similarly, because the information is being transferred and consolidated manually from all of these different locations, the likelihood of accidentally introducing an error or overwriting the existing information is quite high.
- Because the report takes so long to update, the limited frequency of updates made to the report mean that the information within it quickly becomes out of date.
- Because the spreadsheet doesn’t easily allow for historic information about each invoice to be captured and displayed in the report, it’s difficult to access summary statistics about invoices on the report over the course of several weeks or months.

## User Stories

### Fiscal Admin Team Member

Tonay Davis is a member of the DGS Fiscal team who is responsible for soliciting the list of high priority invoices from vendors, searching for information about those invoices across all of the systems involved in the invoice fulfillment process, and compiling that information in the Priority Vendor Aging Report.

**User Needs**

- As a Fiscal admin team member, I want vendors to be able to add their overdue invoices directly to the Priority Vendor Aging Report (after a brief approval), so that I don’t have to spend time copying and pasting information about each invoice from my email or from SharePoint.
- As a Fiscal Staff Member, I want the status of each invoice in the Priority Vendor Aging report to be updated automatically, so that can spend more time troubleshooting stalled invoices and don’t risk transferring information incorrectly.

### Fiscal Leadership

Matt Rappaport is a member of Fiscal Leadership who uses the Priority Vendor Aging Report to understand the current backlog of overdue invoices and troubleshoot specific bottlenecks to getting the highest priority invoices fulfilled.

**User Needs**

- As a member of Fiscal Leadership, I want Fiscal team staff to spend less time manually updating reports, so that they can help troubleshoot issues with the invoice fulfillment process.
- As a member of Fiscal Leadership, I want the Priority Vendor Aging Report to capture not only where an invoice is stuck but also why it’s stuck, so that I can take the necessary steps to move that invoice forward.
- As a member of Fiscal Leadership, I want to be able to view summary statistics about all of the invoices on the Priority Vendor Aging report, so that I can understand things like:
  - How many invoices in total are overdue?
  - Where are the bottlenecks in the invoice fulfillment process?
  - How long does an invoice spend on the Priority Vendor Aging report?
  - What’s the total sum of all overdue invoice payments?

### Priority Vendor

Acme Co. is a priority vendor who has a long-standing relationship with DGS. They often need to contact a member of the DGS Fiscal team to receive updates about their outstanding invoices.

**User Needs**

- As a priority vendor, I want to be able to quickly flag multiple overdue invoices for the DGS Fiscal team, so that they can ensure that those invoices get paid more quickly.
- As a priority vendor, I want to receive updates about my overdue invoices, so that I don’t have to consistently reach out to the DGS Fiscal team to get status updates.

## Feasibility Assessment

### Feasibility Criteria

In order for this project to be feasible the following conditions must be met:

- **System Access:** BPIO must be able to programmatically access each of the systems involved in the fulfillment process, including:
  - Integrify
  - CitiBuy
  - CoreIntegrator
  - SharePoint
- **Sample Data:** DGS Fiscal must be able to provide access to samples of the current versions of the tools and reports used in this process, including:
  - Vendor uploads of overdue invoice templates
  - Priority Vendor Aging Report
- **Stakeholder Input:** BPIO must be able to meet with the set of stakeholders outlined below in order to sufficiently scope and test the usability of the deliverables for this project.

### Practicality Criteria

If the project is feasible, the following conditions must also be met in order for it to be worth pursuing:

- **ROI:** The projected amount of time saved by this solution over the course of three quarters must exceed the amount of time invested by BPIO to develop it.
- **Maintenance Cost:** The amount of time BPIO needs to invest in ongoing maintenance of this solution must not exceed 15 hours per quarter.
- **Non-Duplication:** There must not be an alternative tool or process available that will satisfy all of the objectives outlined above with a greater ROI.

## Deliverable Summary

### Feasibility Assessment

- **Status:** Complete

Conduct a feasibility assessment of this project to validate the riskiest assumptions and key constraints listed in the Feasibility and Practicality sections above. The intended outcome is to refine this discovery document and to finalize the charter for the next deliverable based on the findings of the assessment. If the results of the assessment suggest that a meaningful ROI is either infeasible or impractical, even with a reduced project scope, then we may decide not to pursue the project.

### Priority Vendor Submission Form

- **Status:** Stalled

Create a public-facing form for vendors to submit the information that DGS Fiscal needs to begin tracking the status of that invoice. This form should add that invoice to a SharePoint list or another shared workbook that will replace the current Priority Vendor Aging Excel workbook.

### Priority Vendor Aging Automation Workflow

- **Status:** In Progress

Create an automation script that regularly scrapes information about each of the invoices in the Priority Vendor Aging Report from the various systems that are a part of the invoice fulfillment workflow, then updates the report with that information.

### Priority Vendor Aging Dashboard

- **Status:** Backlog

Create a dashboard that provides members of the DGS Fiscal team with real-time descriptive statistics about the invoices in the Priority Vendor Aging Report, and that allows them to identify and target critical bottlenecks in the invoice fulfillment process.
