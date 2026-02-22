---
title: drawArc
---

# drawArc

## Description

Draws an arc between two points in 3D space.

## Overloads

### Overload 1

Draws an arc between two points in 3D space.

```ts
drawArc(start: object | string, end: object | string, radius: number): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `start` | `object` \| `string` | The starting point of the arc, specified as a vertex object or its variable name. |
| `end` | `object` \| `string` | The ending point of the arc, specified as a vertex object or its variable name. |
| `radius` | `number` | The radius of the arc. |

#### Returns

[`sketch`](../objects/sketch)

#### Notes

None.

### Overload 2

Draws an arc given a center point, radius, start angle, and end angle.

```ts
drawArc(center: object | string, radius: number, startAngle: number, endAngle: number): sketch
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `center` | `object` \| `string` | The center point of the arc, specified as a vertex object or its variable name. |
| `radius` | `number` | The radius of the arc. |
| `startAngle` | `number` | The starting angle of the arc in degrees. |
| `endAngle` | `number` | The ending angle of the arc in degrees. |

#### Returns

[`sketch`](../objects/sketch)

#### Notes

None.

## Notes

None.
