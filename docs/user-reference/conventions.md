---
title: Conventions
sidebar_position: 2
---

# Conventions

## Reference Semantics

- Parameters typed as `object | string` generally accept an object reference, object id, or variable name.
- Parameters documented as coordinates (`x`, `y`, `z`) are numeric axis-aligned values.

## Type Notation

- Union types are shown as `typeA | typeB`.
- `array<...>` indicates an array item type.
- `unknown` indicates missing type data in source and is added by normalization.

## Units and Coordinates

- Coordinates are 3D values where applicable.
- Unit behavior is controlled by `setUnit` where supported by the runtime.

## Overloads

- Overload sections are ordered by source order after duplicate signatures are merged.
- When duplicates are merged, source variants are listed in Notes.
