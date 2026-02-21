---
title: addHelperAxis
---

# addHelperAxis

## Description

Adds a visual helper axis through a point along a direction vector.

## Overloads

### Overload 1

Adds a visual helper axis through a point along a direction vector.

```ts
addHelperAxis(vertex: object | string, normal: object | string): unknown
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | `object` \| `string` | Point the helper axis passes through. Accepts vertex object/command result or variable name. |
| `normal` | `object` \| `string` | Axis direction vector. Accepts vector object/command result or variable name. |

#### Returns

`unknown`

#### Notes

- Output type is missing in source; defaulted to `unknown`.

### Overload 2

Adds a helper axis with explicit length and styling.

```ts
addHelperAxis(vertex: object | string, normal: object | string, length: number, color: number): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertex` | `object` \| `string` | Point the helper axis passes through. |
| `normal` | `object` \| `string` | Axis direction vector. |
| `length` | `number` | Total visual length of the helper axis. |
| `color` | `number` | Optional RGB hex color (e.g. 0xff0000). |

#### Returns

`void`

#### Notes

None.

## Notes

- Output type is missing in source; defaulted to `unknown`.
