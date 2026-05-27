The simplification is complete. Here's the summary:

## Changes Made

**3 files changed, 6 insertions(+), 20 deletions(-)** — net reduction of 14 lines.

### `lib/crates/fabro-cli/Cargo.toml`
- Added `strum.workspace = true` dependency

### `lib/crates/fabro-cli/src/args.rs`
- Removed `use std::fmt;` import (was only used by the two `Display` impls)
- **`GraphDirection`**: Replaced hand-written `impl Display` with `strum::Display` + `strum::EnumString` derives and `#[strum(serialize_all = "UPPERCASE")]` — produces "LR" / "TB"
- **`GraphOutputFormat`**: Replaced hand-written `impl Display` with `strum::Display` + `strum::EnumString` derives and `#[strum(serialize_all = "lowercase")]` — produces "svg"
- Removed 16 lines of hand-written `impl fmt::Display` blocks

### Verification
- ✅ `cargo check -p fabro-cli` — compilation succeeds
- ✅ `cargo nextest run -p fabro-cli` — all 920 tests pass
- ✅ `--direction lr` / `--direction tb` — parsing works
- ✅ `--format svg` — parsing works
- ✅ `--help` — displays correct values

This follows the AGENTS.md guideline: *"For any enum where a variant maps to a fixed string, derive it with `strum` instead of hand-writing `impl Display`, `impl FromStr`, `as_str()`, `fn all()`, or `const ALL: &[Self]`. Hand-written variant→string maps drift across the three impls on every rename."*