---
title: makePoints
---

# makePoints

## Description

Creates a list of points from a given equation.

## Overloads

### Overload 1

Creates a list of points from a given equation.

```ts
makePoints(xt: string, yt: string, zt: string, t: string, numberOfPoints: number): array
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `xt` | `string` | The equation to create the points from. |
| `yt` | `string` | The equation to create the points from. |
| `zt` | `string` | The equation to create the points from. |
| `t` | `string` | The constraint on t. Can be '&gt;=', '&lt;=', '&gt;', '&lt;', '==', '!='. User can use 'OR' or 'AND' to combine multiple constraints but use them with parentheses. |
| `numberOfPoints` | `number` | The number of points to create. |

#### Returns

[`array`](../objects/array)

#### Notes

None.

## Notes

None.
