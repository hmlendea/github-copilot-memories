---
description: "Template for PRIVACY.md data-handling documents."
applyTo: "PRIVACY.md"
---
This is the `PRIVACY.md` template that shall be utilised.
---

<!-- BEGIN PRIVACY TEMPLATE IMMUTABLE -->

# Privacy and Personal Data

[[[Brief summary of the document scope, covered application, deployment model, and personal-data handling approach.]]]

**Information reviewed:** [[YYYY-MM-DD]]

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. Do not include emojis here. -->

## 🔎 What This Document Covers

This document describes how [[Project or service name]] at [[Repository URL or service URL]] handles personal data. It covers the application behaviour and verified integrations described below. Where the software is self-hosted, the instance operator may have separate responsibilities described below.

<!-- Only when users or organisations can deploy and operate their own instance. -->
## 🏠 Self-Hosted Deployments

[[Explain whether this document covers the project maintainers, self-hosted instance operators, or both. State that operators control their instance's configuration, local storage, logs, backups, access controls, retention, and request handling unless the project directly controls those functions.]]

[[Describe any data sent from a self-hosted instance to project maintainers or external services, including telemetry, update checks, crash reports, email, authentication, reverse-proxy, object-storage, or monitoring integrations. State how operators can disable each optional flow when that control exists.]]

## 📥 Data We Handle

### Data Provided to the Application

- [[Category of data provided by users, administrators, or connected systems, or state that no personal data is requested.]]

### Data Generated or Collected by the Application

- [[Category of server, application, access, audit, telemetry, crash, or update-check data generated or collected by the application; or state that no personal data is generated or collected automatically.]]

### Data Received from Integrations

- [[Category and verified source, or state that no personal data is received from integrations or third parties.]]

## 🧭 Processing and Use

The application processes the data described above for these verified functions:
- [[Application function or processing activity]] — [[Data category involved]]
- [[Application function or processing activity]] — [[Data category involved]]

## 🗄️ Storage, Retention, and Deletion

[[Describe where each relevant data category is stored, including local databases, files, logs, caches, backups, or configured storage services. Describe verified retention and deletion behaviour. For self-hosted deployments, identify whether the project or the instance operator controls storage, deletion, and backups.]]

## 🔗 External Processing and Integrations

[[List verified external services, recipients, or integrations that process or receive data, including their purpose and the data flow. State when the application has no built-in external data transfer.]]

| Service or integration | Purpose | Data involved | Configuration or documentation |
|-----------------------|---------|---------------|--------------------------------|
| [[Service or integration name]] | [[Purpose]] | [[Data category]] | [[Verified configuration or documentation URL]] |

<!-- Only when users or operators have documented controls or request procedures. -->
## ⚙️ User Controls and Requests

The following documented controls or request procedures are available:
- [[Control or request procedure]] — [[How to use it]]

<!-- Only when data may be transferred across national or regional borders. -->
## 🌍 International Transfers

[[Describe verified countries or regions to which the application or configured integrations send data. State when deployment location is controlled by the instance operator.]]

<!-- Only when the service is directed to children or age restrictions apply. -->
## 🧒 Children

[[Describe verified age-related behaviour and any application controls for child accounts or data. Do not state an age threshold that has not been confirmed.]]

## 🛡️ Data Protection and Security

[[Describe verified technical and operational safeguards without exposing sensitive implementation details. For self-hosted deployments, identify the operator's responsibilities for updates, secrets, access controls, backups, network exposure, and log protection. Do not promise absolute security.]]

## 🔄 Document Changes

Update this document when application data flows, storage, integrations, or deployment responsibilities change. The current version is published at [[Document URL or repository path]].

## 📬 Contact

For questions about application data handling, contact the project maintainers. For a self-hosted instance, contact the instance operator, unless the project explicitly handles the request. Include [[Information needed to identify the deployment or data flow, if any]]; do not send passwords, access tokens, or other secrets.

<!-- END PRIVACY TEMPLATE IMMUTABLE -->
