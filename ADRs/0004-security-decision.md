# ADR-0004: Security decision

## Decision
Treat untrusted input → planner → tool selection → authorization → tool execution inputs as untrusted. Enforce boundary validation, least privilege, resource limits, safe telemetry and fail-closed authorization.

## Why
AI workflows cross trust boundaries and can amplify adversarial or malformed input.

## Alternatives considered
Trusting internal callers, logging raw payloads and fail-open authorization were rejected.

## Trade-offs
Redaction and strict limits may reduce debugging detail; correlation IDs and error categories preserve diagnosis.

## Consequences
Security claims remain limited to implemented evidence.