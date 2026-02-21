---
title: removeVertex
---

# removeVertex

## Description

Removes a vertex by its coordinates.

## Overloads

### Overload 1

Removes a vertex by its coordinates.

```ts
removeVertex(x: number, y: number, z: number): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `x` | `number` | The x coordinate of the vertex. |
| `y` | `number` | The y coordinate of the vertex. |
| `z` | `number` | The z coordinate of the vertex. |

#### Returns

`void`

#### Notes

- Source variant description: "Removes a vertex by its variable name."
- Merged 2 source variants with the same signature.
- Additional source descriptions: "Removes a vertex by its variable name."

### Overload 2

Removes a previously defined vertex from the scene.

```ts
removeVertex(vertex: object): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | `object` | The vertex object to be removed. |

#### Returns

`void`

#### Notes

None.

### Overload 3

Removes a vertex by its identifier.

```ts
removeVertex(vertexId: string): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertexId` | `string` | The unique identifier of the vertex to be removed. |

#### Returns

`void`

#### Notes

None.

## Notes

- Normalized 4 source overload entries into 3 unique signature(s).
- Source variant description: "Removes a vertex by its variable name."
- Merged 2 source variants with the same signature.
- Additional source descriptions: "Removes a vertex by its variable name."
