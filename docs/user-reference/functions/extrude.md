---
title: extrude
---

# extrude

## Description

Extrudes a closed area or side profile to create a 3D body.

## Overloads

### Overload 1

Extrudes a closed area or side profile to create a 3D body.

```ts
extrude(area: object | string, height: number, type: string, newBody: boolean, direction: vector): body
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `area` | `object` \| `string` | Closed area or side to extrude (shape/side object, id, or name). |
| `height` | `number` | Extrusion distance. |
| `type` | `string` | The type of extrusion to apply to the area. Can be 'one-sided', 'two-sided', or 'symmetric'. |
| `newBody` | `boolean` | Whether to create a new body (currently always creates a new body). |
| `direction` | [`vector`](../objects/vector) | Direction vector the shape extrudes toward, specified as a vector object/id/name. Uses pure translation (no twist/rotation/scale); only orientation is used (e.g. (100,0,0) == (1,0,0)). Extrusion length is controlled by height. Direction must have a non-zero component along the area normal. Defaults to the area normal when omitted. |

#### Returns

[`body`](../objects/body)

#### Notes

None.

### Overload 2

Extrudes an existing side (face profile) to create a new body.

```ts
extrude(sideId: object | string, height: number, type: string, newBody: boolean, direction: vector): body
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `sideId` | `object` \| `string` | Side object/id/name to extrude. |
| `height` | `number` | Extrusion distance. |
| `type` | `string` | The type of extrusion to apply to the area. Can be 'one-sided', 'two-sided', or 'symmetric'. |
| `newBody` | `boolean` | Whether to create a new body (currently always creates a new body). |
| `direction` | [`vector`](../objects/vector) | Direction vector the side profile extrudes toward, specified as a vector object/id/name. Uses pure translation (no twist/rotation/scale); only orientation is used (e.g. (100,0,0) == (1,0,0)). Extrusion length is controlled by height. Direction must have a non-zero component along the profile normal. Defaults to the side normal when omitted. |

#### Returns

[`body`](../objects/body)

#### Notes

None.

## Notes

None.
