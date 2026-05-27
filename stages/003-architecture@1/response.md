Based on the provided CLAUDE.md and workspace layout, here is an architectural assessment focused on separation of concerns, dependency structure, and modularity:

### Separation of Concerns
- **Layered boundaries are explicit**: User-facing entry points (`fabro-cli`, `fabro-server`, `fabro-web`) are decoupled from core orchestration logic (`fabro-workflow`, `fabro-agent`, `fabro-checkpoint`), preventing UI/command concerns from leaking into the engine.
- **Contract-driven API boundary**: The OpenAPI spec is the single source of truth; `fabro-api` uses `build.rs` + `progenitor` to auto-generate types, while `with_replacement(...)` explicitly prevents accidental duplication between wire DTOs and internal domain types.
- **Cross-cutting concerns are governed by policy**: Dedicated strategy docs (`logging-strategy.md`, `error-handling-strategy.md`, `server-secrets-strategy.md`, `migrations-strategy.md`) enforce consistent implementation patterns without scattering concerns into business crates.
- **Test infrastructure is strictly gated**: Test-only fixtures, fake credentials, and in-memory stores are confined behind the `test-support` feature flag, ensuring production builds remain free of test dependencies and secret leakage.

### Dependency Structure
- **Workspace-monorepo layout**: `lib/crates/` (Rust), `apps/` (frontend), and `lib/packages/` (TS clients) form a unified Cargo workspace, enabling shared dependency resolution, unified test runners (`cargo nextest run --workspace`), and incremental compilation.
- **Unidirectional code generation flow**: `fabro-api.yaml` → `fabro-api` (Rust) & `fabro-api-client` (TS) → `fabro-server` & `fabro-web`. This prevents circular dependencies and keeps the wire contract stable across language boundaries.
- **Trait-based pluggable providers**: `Sandbox` (local/Docker/Daytona), LLM providers, and event emitters use abstract interfaces, allowing runtime/environment swaps without modifying core orchestration or server code.
- **Encapsulated integrations**: Third-party or external services (`fabro-github`, `fabro-slack`, `fabro-mcp`, `fabro-telemetry`, `fabro-devcontainer`) are isolated in dedicated crates, limiting blast radius when auth flows, rate limits, or SDKs change.

### Modularity
- **High compile-time isolation**: Each Rust crate is independently buildable and testable, supporting parallel CI execution, targeted PR reviews, and reduced merge conflicts.
- **Strict internal module discipline**: Import conventions (`module::function()` for functions, named imports for types, no production globs) and `strum` derivation for enums prevent internal coupling drift and make refactoring predictable.
- **Encapsulated tooling & release pipelines**: Dev commands (`cargo dev docker-build`, `cargo dev build`, `cargo dev release`) encapsulate CI/CD, Docker staging, and SPA asset bundling outside the main source tree, keeping product code focused on business logic.
- **Checkpoint & resume as independent subsystems**: State serialization and branch management are extracted into `fabro-checkpoint`, allowing the workflow engine to remain stateless and focused on execution topology rather than persistence.
- **Potential risk areas to monitor**:
  - `fabro-server` may accumulate route handlers and middleware over time; without explicit route-splitting or plugin-based routing, it risks becoming a monolith.
  - Heavy reliance on `build.rs` and progenitor generation requires strict discipline to avoid hidden compile-time coupling or schema drift if OpenAPI changes are not co-reviewed with Rust/TS consumers.
  - Parallel branch failures (`parallel.results: 3x failed`) suggest integration or environment boundaries may be tight; ensuring test harnesses and sandbox providers are truly isolated (e.g., socket/daemon mocking, network stubbing) will improve modularity in CI.