---
title: pattern
---

# pattern

## Description

Creates a pattern by repeating a body or sketch.

## Overloads

### Overload 1

Creates a pattern by repeating a body or sketch.

```ts
pattern(item: string, direction: vector, spacing: number, repetitions: number): array
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `item` | `string` | The body id to repeat. |
| `direction` | [`vector`](../objects/vector) | The direction to repeat the body or sketch, specified as a vector object or its variable name. |
| `spacing` | `number` | The spacing between the repetitions of the body. |
| `repetitions` | `number` | The number of repetitions to repeat the body. |

#### Returns

[`array`](../objects/array)

#### Notes

None.

### Overload 2

Creates a pattern by repeating a body or sketch.

```ts
pattern(item: string, direction: vector, totalDistance: number, repetitions: number): array
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `item` | `string` | The body id to repeat. |
| `direction` | [`vector`](../objects/vector) | The direction to repeat the body or sketch, specified as a vector object or its variable name. |
| `totalDistance` | `number` | The total distance to repeat the body. |
| `repetitions` | `number` | The number of repetitions to repeat the body. |

#### Returns

[`array`](../objects/array)

#### Notes

None.

### Overload 3

Creates a circular pattern around a center. Orbit radius is derived from the source item's current distance to center, and each repeated item rotates with the orbit.

```ts
pattern(item: string, center: vertex, repetitions: number): array
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `item` | `string` | The body id to repeat. |
| `center` | [`vertex`](../objects/vertex) | Center of orbit, specified as a vertex object or its variable name. |
| `repetitions` | `number` | Number of repeated instances (the source item is the starting reference on the orbit). |

#### Returns

[`array`](../objects/array)

#### Notes

None.

## Notes

None.
