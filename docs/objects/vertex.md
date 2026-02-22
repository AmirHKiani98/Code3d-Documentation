---
title: vertex
---

# vertex

## Description

A 3D point with x, y, and z components.

## Properties

| Name | Type | Description |
| --- | --- | --- |
| `x` | `number` | No description provided. |
| `y` | `number` | No description provided. |
| `z` | `number` | No description provided. |

## Methods Summary

| Method | Returns | Description |
| --- | --- | --- |
| `copy` | [`vertex`](./vertex) | Creates a copy of the vertex. |
| `length` | `number` | Returns the length of the vertex from the origin. |
| `transform` | [`vertex`](./vertex) | Transforms the vertex by a matrix. |

## Methods

### copy

Creates a copy of the vertex.

#### Signature

```ts
copy(toPoint: vertex, byVector: vector): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `toPoint` | [`vertex`](./vertex) | The vertex to copy the vertex to. |
| `byVector` | [`vector`](./vector) | The vector to copy the vertex by. |

#### Returns

[`vertex`](./vertex)

#### Notes

None.

### length

Returns the length of the vertex from the origin.

#### Signature

```ts
length(): number
```

#### Parameters

None.

#### Returns

`number`

#### Notes

None.

### transform

Transforms the vertex by a matrix.

#### Signature

```ts
transform(transformer: vector): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `transformer` | [`vector`](./vector) | The vector to transform the vertex by. |

#### Returns

[`vertex`](./vertex)

#### Notes

None.

## Notes

- Property `x` is missing a description in source; defaulted to "No description provided."
- Property `y` is missing a description in source; defaulted to "No description provided."
- Property `z` is missing a description in source; defaulted to "No description provided."
