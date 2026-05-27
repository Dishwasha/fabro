# Simplify `GraphDirection` and `GraphOutputFormat` with strum

## Problem

`lib/crates/fabro-cli/src/args.rs` has two enums that use clap's `ValueEnum` derive (which requires `Display` and `FromStr`) but hand-write their `Display` implementation:

```rust
#[derive(Debug, Clone, Copy, ValueEnum)]
pub(crate) enum GraphDirection {
    Lr,
    Tb,
}

impl fmt::Display for GraphDirection {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Lr => write!(f, "LR"),
            Self::Tb => write!(f, "TB"),
        }
    }
}

#[derive(Debug, Clone, Copy, ValueEnum)]
pub(crate) enum GraphOutputFormat {
    Svg,
}

impl fmt::Display for GraphOutputFormat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Svg => write!(f, "svg"),
        }
    }
}
```

Per the AGENTS.md guidelines, enums where a variant maps to a fixed string should use `strum` derives instead of hand-written `impl Display`, `impl FromStr`, `as_str()`, or `fn all()`. Hand-written variant→string maps drift across the three impls on every rename.

## Solution

Replace the hand-written `impl fmt::Display` blocks with strum derives:

- `GraphDirection`: Add `strum::Display` and `strum::EnumString` derives + `#[strum(serialize_all = "UPPERCASE")]` to produce "LR" / "TB".
- `GraphOutputFormat`: Add `strum::Display` and `strum::EnumString` derives + `#[strum(serialize_all = "lowercase")]` to produce "svg".

The `ValueEnum` derive from clap still works because strum's `Display` and `EnumString` satisfy clap's trait bounds.

## Files to change

1. **`lib/crates/fabro-cli/Cargo.toml`** — Add `strum.workspace = true` dependency.

2. **`lib/crates/fabro-cli/src/args.rs`** — Replace two hand-written `impl fmt::Display` blocks with strum derives. Also remove the now-unused `use std::fmt;` import.

## Steps

1. Add `strum.workspace = true` to `lib/crates/fabro-cli/Cargo.toml` dependencies.

2. Edit `lib/crates/fabro-cli/src/args.rs`:
   - Add `strum::Display` and `strum::EnumString` to the derives on `GraphDirection`
   - Add `#[strum(serialize_all = "UPPERCASE")]` to `GraphDirection`
   - Remove the `impl fmt::Display for GraphDirection` block
   - Add `strum::Display` and `strum::EnumString` to the derives on `GraphOutputFormat`
   - Add `#[strum(serialize_all = "lowercase")]` to `GraphOutputFormat`
   - Remove the `impl fmt::Display for GraphOutputFormat` block
   - Remove the `use std::fmt;` import (only used by these two impl blocks)

3. Run `cargo build -p fabro-cli` to verify compilation.

4. Run `cargo nextest run -p fabro-cli` to verify tests pass.

## Expected behavior

- `--direction lr` and `--direction tb` continue to work (strum's `EnumString` + `serialize_all = "UPPERCASE"` handles case-insensitive parsing by default).
- `--format svg` continues to work.
- `--help` output shows `LR` and `TB` for `--direction`, and `svg` for `--format` (clap's ValueEnum uses Display).
- Zero behavior changes — this is a pure code-quality simplification.
