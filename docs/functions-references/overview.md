---
title: Overview
sidebar_position: 1
---

# Functions-References

This section documents the building blocks used when defining user functions.

## What This Section Covers

- [Variables](./variable): how to declare function-level variables with `define`.
- [Types](./types): available domain types like `Plane`, `Body`, `Vertex`, `Vector`, and `Sketch`.
- [Mathematical Operations](./mathematical-operations): arithmetic operators and numeric expressions.
- [For-Loops](./for-loop): iterate over sequences and collections.
- [While-Loops](./while): run repeated logic while a condition remains true.
- [In-Built Functions](./in-builts): Python-style built-ins such as `filter`, `range`, `sort`, and `lambda`.

## Typical Flow

1. Define variables and assign their types.
2. Use control flow (`for` / `while`) to iterate.
3. Apply built-ins and mathematical operations to compute results.

## Minimal Example

```python
define p: Plane
define path: Sketch
define offset: Vector

for vertex in path.vertices:
    # use math + in-built functions inside the loop
    ...
```
