---
title: Types
sidebar_position: 2
---

# Available types

Use these types in variable declarations:

```ts
define myPlane: Plane
define myBody: Body
define pointA: Vertex
define direction: Vector
define profile: Sketch
```

## Quick Reference

| Type | Description |
| --- | --- |
| `Plane` | A plane in 3D space, defined by a normal and a point. |
| `Body` | A 3D solid object with sketches/sides. |
| `Vertex` | A 3D point (`x`, `y`, `z`). |
| `Vector` | A 3D direction/displacement (`x`, `y`, `z`). |
| `Sketch` | A 2D sketch made from vertices and edges. |

## Plane

A `Plane` represents an infinite 3D plane.

- Common properties: `normal: Vector`, `point: Vertex`
- Common methods: `distanceToPoint(point)`, `distanceToPlane(plane)`, `projectPoint(point)`

## Body

A `Body` represents a 3D shape.

- Common properties: `sketches`, `sides`
- Common methods: `area()`, `volume()`, helper methods such as `addVertices()` and `addEdges()`

## Vertex

A `Vertex` is a point in 3D coordinates.

- Fields: `x`, `y`, `z` (numbers)
- Common methods: `transform(vector)`, `length()`, `copy(...)`

## Vector

A `Vector` represents direction and magnitude in 3D.

- Fields: `x`, `y`, `z` (numbers)
- Common methods: `magnitude()`, `normalize()`

## Sketch

A `Sketch` is a 2D construct made of vertices and edges.

- Common properties: `vertices`, `edges`
- Common methods: `addVertex(vertex)`, `addEdge(edge)`, `close()`, `transform(vector)`, `copy(byVector)`
