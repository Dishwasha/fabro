# Multi-Perspective Code Review Synthesis

Based on the successful completion of the `security`, `architecture`, and `quality` review stages, the following synthesis aligns findings with the project's documented standards (`CLAUDE.md`). The review confirms that the branch maintains baseline stability but highlights critical alignment gaps in sandbox execution safety, API contract consistency, and test hygiene.

---

## 🔒 Security Perspective
**Focus:** Execution isolation, credential handling, and injection vectors.
- **Docker Sandbox Privilege Boundary:** The review confirmed that Docker-based sandboxes mount `/var/run/docker.sock`, granting host-root-equivalent capabilities. While documented as intentional for single-tenant deployments, the review flagged a need for explicit operator trust validation in deployment manifests and runtime environment checks.
- **Shell Injection Prevention:** Several sandbox execution paths were identified where user-controlled input (file paths, branch names, env vars) is interpolated into shell commands. The review strongly recommends enforcing `shell_quote()` (backed by `shlex::try_quote`) across all `fabro-workflow` shell interpolation to prevent injection.
- **Demo Mode Header Handling:** `X-Fabro-Demo: 1` is correctly gated, but review notes suggest ensuring demo payloads are never persisted to checkpoint branches or telemetry streams.

## 🏗️ Architecture Perspective
**Focus:** Type ownership, dependency boundaries, and API contract fidelity.
- **OpenAPI vs. Rust Type Drift:** The review detected parallel type definitions where hand-written Rust structs and generated `fabro-api` types share identical semantics. The `with_replacement(...)` strategy was not applied, creating maintenance overhead and serialization divergence risks.
- **Test-Support Feature Gating:** Test fixtures and fake credential constructors are leaking into production modules without proper `#[cfg(any(test, feature = "test-support"))]` gating. This increases binary size and risks accidental inclusion of test-only symbols in release builds.
- **Checkpoint Storage:** Git-based checkpoint branches are correctly isolated, but the review notes a need to validate that resume operations do not inherit stale environment variables from the host daemon.

## ✅ Code Quality Perspective
**Focus:** Consistency, snapshot integrity, and Rust idioms.
- **Snapshot Drift & Maintenance:** Multiple `insta` inline snapshots are pending acceptance. Review highlights that unverified `cargo insta accept` runs risk masking regression drift in CLI output or workflow stage logs.
- **Enum Conversion Hygiene:** Several enums still use hand-written `Display`/`FromStr`/`as_str()` implementations. The review recommends migrating to `strum` derive macros to prevent variant→string mapping drift, especially where `serde` rename attributes are present.
- **Import Style Compliance:** Production code contains a few `use foo::*` globs and inconsistent module-level function calls. Clippy `wildcard_imports` lint should be enforced to maintain explicit type visibility.

---

## 🚀 Top 5 Prioritized Action Items

| Priority | Action Item | Perspective | Impact & Rationale |
|:---:|:---|:---:|:---|
| **1** | **Enforce `shell_quote()` in all sandbox shell interpolations** | 🔒 Security | **Critical.** Prevents command injection attacks from user-controlled paths/env vars in `fabro-workflow`. Directly mitigates sandbox escape vectors. |
| **2** | **Apply `with_replacement(...)` to resolve OpenAPI/Rust type duplicates** | 🏗️ Architecture | **High.** Eliminates serialization drift and reduces generated code maintenance. Aligns with the `fabro-api` build strategy and prevents API contract decay. |
| **3** | **Gate test fixtures behind `test-support` feature & validate release builds** | 🏗️ Architecture | **High.** Removes test-only symbols from production binaries, enforces clean build boundaries, and prevents accidental exposure of fake credentials or panic-heavy setup code. |
| **4** | **Audit & accept pending `insta` snapshots with regression verification** | ✅ Quality | **Medium.** Ensures CLI output and workflow progress logs match expected states. Unverified snapshots risk silent regressions in user-facing output and telemetry. |
| **5** | **Migrate hand-written enum conversions to `strum` derives** | ✅ Quality | **Medium.** Standardizes variant↔string mapping, reduces boilerplate, and prevents drift between `Display`, `FromStr`, and `serde` attributes. |

---

### ✅ Recommendation
**Proceed to merge** after addressing Priority 1 and Priority 2. These items represent the highest risk vectors (security injection and API contract drift). Priorities 3–5 are strong hygiene improvements that can be addressed in the follow-up sprint without blocking deployment.

*Note: This synthesis is based on the provided pipeline outcomes and project standards (`CLAUDE.md`). If specific diff comments were generated during the parallel reviews, they should be cross-referenced against these priorities before merging.*