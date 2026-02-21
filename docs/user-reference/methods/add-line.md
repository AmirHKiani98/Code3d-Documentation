---
title: addLine
---

# addLine

## Description

Draws a line between two vertices in 3D space.

## Overloads

### Overload 1

Draws a line between two vertices in 3D space.

```ts
addLine(startVertex: object, endVertex: object): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `startVertex` | `object` | The starting vertex of the line. |
| `endVertex` | `object` | The ending vertex of the line. |

#### Returns

[`sketch`](../objects/sketch)

#### Notes

None.

### Overload 2

Draws a line between two vertices identified by their IDs.

```ts
addLine(reference: object | string, start: object | string, angle: number, length: number): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `reference` | `object` \| `string` | The line reference object or its variable name. The line should exist in the scene. |
| `start` | `object` \| `string` | A point on the line, specified as a vertex object or its variable name. The point should exist on the line. If the point is on the line but doesn't exist on the scene, it will be created automatically. |
| `angle` | `number` | The angle in degrees from the line's direction to the desired direction. |
| `length` | `number` | The length of the new line segment to be drawn from the specified point. |

#### Returns

[`sketch`](../objects/sketch)

#### Notes

None.

## Notes

None.
