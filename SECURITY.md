# Security Policy

## Supported versions

Security fixes are applied to the latest released `1.x` version.

| Version | Supported |
|---|---|
| Latest `1.x` | Yes |
| Older versions | No |

## Reporting a vulnerability

Use GitHub Private Vulnerability Reporting for this repository when it is enabled.

Do not include secrets, credentials, private repository names, source inventories, or customer information in a public issue.

If Private Vulnerability Reporting is unavailable, contact the repository owner through the [ltytp GitHub profile](https://github.com/ltytp) without disclosing vulnerability details publicly, and request a private reporting channel.

## Security boundaries

- The diagnostic scanner is read-only toward the target repository.
- Discovered scripts, skills, agents, CI definitions, and infrastructure code are not executed.
- Import requires package checksum validation, source fingerprint matching, a selected Golden Work Item, and ordered approval.
- Generated diagnostic packages, system inventories, graph seeds, session state, and import receipts must not be committed to this public repository.
- Users are responsible for applying their organization's repository, network, data-retention, and AI-service policies.
