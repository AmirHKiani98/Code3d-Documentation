---
title: sketch
---

# sketch

## Description

A 2D sketch with a list of vertices and edges.

## Properties

| Name | Type | Description |
| --- | --- | --- |
| `edges` | `array` of `edge` | No description provided. |
| `vertices` | `array` of [`vertex`](./vertex) | No description provided. |

## Methods Summary

| Method | Returns | Description |
| --- | --- | --- |
| `addEdge` | [`sketch`](./sketch) | Adds an edge to the sketch. |
| `addVertex` | [`sketch`](./sketch) | Adds a vertex to the sketch. |
| `close` | [`sketch`](./sketch) | Closes the sketch. |
| `copy` | [`sketch`](./sketch) | Creates a copy of the sketch. |
| `remove` | `void` | Removes the sketch. |
| `removeEdge` | [`sketch`](./sketch) | Removes an edge from the sketch. |
| `removeVertex` | [`sketch`](./sketch) | Removes a vertex from the sketch. |
| `transform` | [`sketch`](./sketch) | Transforms the sketch by a matrix. |

## Methods

### addEdge

Adds an edge to the sketch.

#### Signature

```ts
addEdge(edge: edge): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `edge` | `edge` | The edge to add to the sketch. |

#### Returns

[`sketch`](./sketch)

#### Notes

- Method `addEdge` parameter `edge` contains unresolved type reference `edge`.

### addVertex

Adds a vertex to the sketch.

#### Signature

```ts
addVertex(vertex: vertex): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | [`vertex`](./vertex) | The vertex to add to the sketch. |

#### Returns

[`sketch`](./sketch)

#### Notes

None.

### close

Closes the sketch.

#### Signature

```ts
close(): sketch
```

#### Parameters

None.

#### Returns

[`sketch`](./sketch)

#### Notes

None.

### copy

Creates a copy of the sketch.

#### Signature

```ts
copy(byVector: vector): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `byVector` | [`vector`](./vector) | The vector to copy the sketch by. |

#### Returns

[`sketch`](./sketch)

#### Notes

None.

### remove

Removes the sketch.

#### Signature

```ts
remove(): void
```

#### Parameters

None.

#### Returns

`void`

#### Notes

None.

### removeEdge

Removes an edge from the sketch.

#### Signature

```ts
removeEdge(edge: edge): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `edge` | `edge` | The edge to remove from the sketch. |

#### Returns

[`sketch`](./sketch)

#### Notes

- Method `removeEdge` parameter `edge` contains unresolved type reference `edge`.

### removeVertex

Removes a vertex from the sketch.

#### Signature

```ts
removeVertex(vertex: vertex): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | [`vertex`](./vertex) | The vertex to remove from the sketch. |

#### Returns

[`sketch`](./sketch)

#### Notes

None.

### transform

Transforms the sketch by a matrix.

#### Signature

```ts
transform(transformer: vector): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `transformer` | [`vector`](./vector) | The vector to transform the sketch by. |

#### Returns

[`sketch`](./sketch)

#### Notes

None.

## Notes

- Property `edges` contains unresolved type reference `edge`.
- Property `edges` is missing a description in source; defaulted to "No description provided."
- Property `vertices` is missing a description in source; defaulted to "No description provided."
