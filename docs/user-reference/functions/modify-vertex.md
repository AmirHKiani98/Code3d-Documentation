---
title: modifyVertex
---

# modifyVertex

## Description

Modifies a vertex's position. All dependents (edges, sketches, closed shapes, bodies, pattern instances) update recursively.

## Overloads

### Overload 1

Modifies a vertex's position. All dependents (edges, sketches, closed shapes, bodies, pattern instances) update recursively.

```ts
modifyVertex(vertex: object | string, newVertex: vertex): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | `object` \| `string` | The vertex to modify, by ID (e.g. vertex_3f91abf6) or variable reference. |
| `newVertex` | [`vertex`](../objects/vertex) | The new position as vertex(x,y,z) or coordinates. |

#### Returns

[`vertex`](../objects/vertex)

#### Notes

None.

### Overload 2

Modifies a vertex's position. All dependents update recursively.

```ts
modifyVertex(vertexId: string, x: number, y: number, z: number): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertexId` | `string` | The vertex ID to modify. |
| `x` | `number` | New x coordinate. |
| `y` | `number` | New y coordinate. |
| `z` | `number` | New z coordinate. |

#### Returns

[`vertex`](../objects/vertex)

#### Notes

None.

## Notes

None.
