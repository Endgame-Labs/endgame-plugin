# Security Policy

## Reporting A Vulnerability

Do not open a public issue for suspected vulnerabilities, credential exposure,
or authorization bypasses.

Report security issues privately through GitHub private vulnerability reporting
if it is enabled for this repository. Otherwise, email `support@endgame.io` with
the subject `Security: endgame-plugin`.

Include:

- The affected plugin version or commit.
- Steps to reproduce or a proof of concept.
- The expected impact.
- Any relevant Claude surface, operating system, and client version.
- Known mitigations or workarounds.

Do not include live credentials, access tokens, or customer data. We will
coordinate reproduction, remediation, and disclosure through the private
reporting channel.

## Scope

Security-sensitive areas in this repository include:

- OAuth and MCP connector configuration.
- Credential and customer-data exposure.
- Plugin permission boundaries.
- Marketplace source and package integrity.
- Skill behavior that could cause unauthorized access or disclosure.

## Supported Versions

Security fixes target the latest published plugin version. Upgrade to the
latest version before reporting an issue that may already have been addressed.
