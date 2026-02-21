---
title: revolve
---

# revolve

## Description

Creates a 3D shape by revolving a 2D shape around an axis.

## Overloads

### Overload 1

Creates a 3D shape by revolving a 2D shape around an axis.

```ts
revolve(area: object | string, axis: object | string, height: number, angle: number): body
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `area` | `object` \| `string` | The 2D area to be revolved, specified as a closed sketch or its variable name. |
| `axis` | `object` \| `string` | The axis to revolve the area around, specified as a vector object or its variable name. |
| `height` | `number` | The height of the revolved body. |
| `angle` | `number` | Sweep angle in degrees. Positive/negative values are allowed. Default: 360. |

#### Returns

[`body`](../objects/body)

#### Notes

None.

## Notes

None.
