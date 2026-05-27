Based on the provided architecture, build/dev guidelines, and crate structure, here is a multi-perspective security review focused on hardcoded secrets, injection risks, and unsafe dependencies. Findings are derived from architectural patterns, documented practices, and known risk surfaces in this system type.

### 🔐 Hardcoded Secrets & Credential Management
- **Test fixture leakage risk**: The codebase explicitly warns against exposing fake credentials or test environment shims in production builds, but if `#[cfg(any(test, feature = "test-support"))]` gating fails or dev-dependencies accidentally pull in `test-support` defaults, hardcoded tokens could ship in release binaries.
- **Demo mode bypass surface**: `X-Fabro-Demo: 1` header enables demo mode. If demo routes skip authentication, skip rate limiting, or load hardcoded fallback credentials, this becomes an unauthenticated attack vector in production if headers are spoofed or headers are stripped by reverse proxies.
- **GitHub App credential storage**: JWT signing and installation token flows require app ID, private key, and webhook secret. If these are baked into `defaults.toml`, CI pipeline variables, or example configs without strict runtime env enforcement, they risk exposure in version control or logs.
- **LLM provider key defaults**: `fabro-llm` supports multiple providers. Any fallback keys or example values in configuration files must be scrubbed before release; LLM keys should never be compiled into binaries or exposed via `tracing` logs.
- **Subprocess env inheritance**: Server-secrets strategy notes subprocess env inheritance/scrubbing. If parent secrets (API keys, tokens) are inherited by workflow subprocesses without explicit stripping, compromised stages could exfiltrate them.

### 💉 Injection Risks
- **Workflow shell command execution**: Though `shell_quote()` backed by `shlex::try_quote` is mandated, Graphviz workflow definitions executed by `fabro-workflow` remain a high-risk surface. Malicious or unvalidated workflow graphs could still trigger command injection via poorly delimited arguments, here-docs, or environment variable expansion.
- **Docker socket privilege escalation**: `/var/run/docker.sock` is mounted as host-root-equivalent. A compromised workflow, malicious LLM agent output, or flawed sandbox provider code can spin privileged containers, escape to the host, or manipulate host Docker state. Read-only socket mounts, seccomp/AppArmor profiles, and network namespace isolation are missing from the documented runtime.
- **AI agent tool abuse**: `fabro-agent` exposes Bash, Read, Write, Edit, Glob, Grep, and WebFetch tools. Prompt injection, adversarial LLM reasoning, or workflow stage logic can trigger destructive file edits, credential harvesting, or outbound exfiltration via `WebFetch`. Tool allowlisting, command regex validation, and outbound egress filtering are critical gaps.
- **Git checkpoint credential persistence**: `fabro-checkpoint` uses Git branches and metadata commits. If API tokens, SSH keys, or env secrets are accidentally written to checkpoint files or committed to `.git/objects`, they become permanently versioned and recoverable via `git log` or `git show`.
- **SSE event injection**: Server-sent event streams could be vulnerable to event message injection if user-provided workflow output or LLM responses are interpolated into SSE frames without strict newline/capitalization sanitization (`data:`, `event:`, blank line boundaries).

### 📦 Dependencies & Configuration Security
- **`reqwest` proxy bypass in production**: Test clients use `.no_proxy()` to avoid macOS proxy discovery overhead. If this pattern leaks into production HTTP clients (e.g., LLM calls, GitHub API, Slack webhooks), it bypasses corporate proxy/PAC security controls, SSL inspection, and egress filtering.
- **`anyhow` error verbosity**: The error-handling strategy notes `anyhow`/`thiserror` usage. Broad `.map_err(|e| format!("{:#}", e))` or direct `Error::msg(e.to_string())` can leak stack traces, internal IPs, or environment variables into API responses or logs. Consistent application of `fabro-util::redact` is required before serialization.
- **OpenAPI-generated client trust boundaries**: `progenitor` and `openapi-generator` auto-create Rust and TypeScript HTTP clients. If generated clients lack explicit timeout configs, TLS 1.2+ enforcement, or strict header sanitization, they become silent attack surfaces for SSRF, slowloris, or header injection.
- **Docker build pipeline hardening**: `cargo dev docker-build` uses `cargo-zigbuild` but the provided context doesn't specify multi-stage builds, non-root user execution, image vulnerability scanning, or base image pinning. Unscanned or outdated base images increase supply chain risk.
- **Mintlify dev container risk**: `mintlify dev` runs `node:22-slim` in Docker with volume mounts to `/docs`. While dev-only, unvetted community Dockerfiles or outdated Node LTS images can introduce known CVEs if pulled or cached without digest pinning.

### 🌐 API, Frontend & Data Flow
- **React XSS surface**: The React 19 frontend renders workflow output, agent responses, and SSE streams. Dynamic content must be strictly sanitized or escaped; raw HTML injection from untrusted workflow nodes or LLM outputs could lead to stored/executed XSS.
- **State-changing GET requests**: If the Axum router exposes mutation endpoints via `GET` (e.g., run triggers, model changes), they bypass CSRF protections and may be triggered by malicious links or image tags. All state mutations must use `POST`/`PATCH`/`DELETE` with token validation.
- **Webhook signature validation**: GitHub App and Slack integrations must verify HMAC signatures and timestamp nonces. Missing or lax validation enables request forgery, workflow manipulation, or rate-limit bypass.

### 🔍 Recommended Validation Steps
- Run `cargo audit` and `bun audit` (or `npm audit`) across all crates and packages to flag known CVEs in direct/transitive dependencies.
- Add `tracing`/`serde` log sanitization checks to CI: ensure no `KEY`, `SECRET`, `TOKEN`, or credential-like patterns leak into debug logs or API error payloads.
- Enforce `deny(warnings)` and `deny(unused_imports)` in CI to catch accidental test-helper leaks.
- Add Dockerfile linting (`hadolint`) and image scanning (`trivy`/`grype`) to the release pipeline.
- Implement strict workflow graph schema validation at parse time (allowlist stage types, reject arbitrary command strings, enforce sandbox boundaries).
- Audit all `reqwest::Client::new()` or `Client::builder()` instantiations in production code to ensure TLS 1.2+, timeouts, and proxy defaults are explicitly set (not `.no_proxy()`).