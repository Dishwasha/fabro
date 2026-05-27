Based on the provided `CLAUDE.md` project guidelines, here is a structured, multi-perspective code review focused on naming conventions, dead code, test coverage gaps, and error handling. Findings are organized by perspective and formatted as actionable bullet points.

### 🔤 Naming Conventions
- **Test fixture vs production naming overlap**: Verify that shared test helpers avoid production-sounding names like `create_app_state`, `init_store`, or `build_client`. The guidelines require explicit prefixes (`test_app_state`, `test_store_bundle`, `test_auth_mode`) to prevent accidental production linkage.
- **Rust import style drift**: Check for glob imports (`use foo::*`) in production modules. The codebase enforces `use crate::type_name` for types and `use crate::module` for function calls (`module::function()`). Globs should be confined to test modules and preludes only.
- **Enum string/int mapping consistency**: Ensure any enum with fixed string or integer variants derives `strum` (`Display`, `EnumString`, `IntoStaticStr`) instead of hand-written `impl Display`/`FromStr`. Misaligned manual maps are a known drift risk.
- **API DTO vs internal type naming**: Flag any `ApiFoo` aliases or `foo_to_api`/`foo_from_api` adapters that exist solely to bridge accidental duplicate types. They should only exist when the API intentionally projects a different shape, and must carry an API-facing name that doesn't collide with internal concepts.
- **Shell interpolation naming**: Verify no ad-hoc quoting helpers exist. All shell command assembly must route through `shell_quote()` (backed by `shlex::try_quote`) to prevent injection in file paths, branch names, or env vars.

### 🧹 Dead Code & Build Hygiene
- **Test-support feature bleed**: Audit `Cargo.toml` files for `test-support` enabled in default features, release profiles, or production dependencies. It must only be activated via explicit `[dev-dependencies]` feature flags.
- **Hidden public APIs in production**: `#[doc(hidden)]` does not prevent compilation or linkage. Any test-only symbols leaking into normal builds (e.g., fake credentials, in-memory stores, panic-heavy setup) should be moved behind `#[cfg(any(test, feature = "test-support"))]`.
- **Stray generated API types**: Run workspace-wide searches for types that duplicate OpenAPI schemas but aren't referenced by `with_replacement(...)` in `fabro-api/build.rs`. Unused generated DTOs inflate compile time and maintenance surface.
- **Orphaned CLI subcommands**: Verify that removed or deprecated workflow stages/steps no longer expose CLI flags or route handlers. Dead handler code in `fabro-server` can linger if route registration and handler definitions are not co-refactored.
- **Build artifact contamination**: In release/debug builds compiled without `test-support`, confirm no test tokens, mock certs, or fixture JSONs are embedded in the final binary or SPA bundle.

### 🧪 Test Coverage Gaps & Testing Strategy
- **E2E live test gating**: Confirm that all `#[e2e_test(live("VAR"))]` tests are properly gated behind `--profile e2e --run-ignored only` and require `.env` credentials. Missing env vars should fail fast with clear setup instructions, not silently skip or panic.
- **Local HTTP client proxy misconfiguration**: Review test HTTP clients for `reqwest::Client::new()` or bare `Client::builder()`. macOS proxy discovery adds startup latency and can cause false timeouts. All local test clients must use `.no_proxy()` or the shared `fabro_test::test_http_client()` helper.
- **Snapshot drift risk**: Check for tests using `insta` without explicit pending snapshot verification. `cargo insta accept` without review can silently merge unrelated changes across crates.
- **Twin vs live test parity**: Dual-mode tests (`#[e2e_test(twin)]`) should have matching live counterparts for critical paths. Missing live coverage for AI agent tool-use, sandbox clone providers, or checkpoint resume logic creates blind spots in production reliability.
- **FD limit environment drift**: The macOS `ulimit -n 256` default breaks parallel `nextest` runs. Ensure CI and developer shell configs enforce `ulimit -n 4096` (or higher) before running the shared CLI test daemon.

### 🛡️ Error Handling & Resilience
- **Inconsistent error conversion paths**: Verify that `.map_err(...)` chains do not silently convert to `.to_string()` or `String` in API handlers. The error handling strategy requires preserving type fidelity until the serialization layer, where structured API errors should be rendered consistently.
- **Missing recovery paths for sandbox failures**: Docker/Daytona clone-based providers can fail on missing `DOCKER_HOST`, socket permissions, or non-GitHub origins. Ensure fallback errors distinguish between transient daemon issues and misconfigured run manifests, rather than panicking or returning opaque failures.
- **Checkpoint/resume error state handling**: Validate that workflow engine checkpoint failures (branch store, metadata branches, Git conflicts) surface as recoverable errors with clear resume instructions, not fatal aborts.
- **LLM client retry/middleware boundaries**: Check that retry middleware respects circuit breaker/backoff policies and does not swallow 429/5xx responses as generic `anyhow` errors. LLM providers require explicit rate-limit and quota handling.
- **Secrets scrubbing in subprocess/env**: Ensure that startup validation and subprocess execution paths strip or redact server-level secrets before inheritance/scrubbing, per `server-secrets-strategy.md`. Leaked secrets in logs or test harnesses are a critical gap.

### 🔍 Cross-Cutting Verification Steps (Recommended)
- Run `cargo +nightly-2026-04-14 clippy --workspace --all-targets -- -D warnings` to catch import style, dead code, and `strum` misalignments automatically.
- Execute `cargo build --workspace` without `test-support` to verify no test helpers leak into production binaries.
- Run `cargo nextest run --workspace --profile e2e --run-ignored only` with `ulimit -n 4096` to validate E2E test stability and proxy isolation.
- Audit `docs/public/api-reference/fabro-api.yaml` against `lib/crates/fabro-api/build.rs` `with_replacement(...)` calls to eliminate duplicate API types.

These findings align with the project's explicit architectural, testing, and API contract guidelines. Addressing them will reduce maintenance friction, eliminate silent failure modes, and enforce consistency across the Rust/TypeScript boundary.