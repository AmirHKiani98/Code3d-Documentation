---
title: removeVector
---

# removeVector

## Description

Removes a vector by its coordinates.

## Overloads

### Overload 1

Removes a vector by its coordinates.

```ts
removeVector(x: number, y: number, z: number): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `x` | `number` | The x component of the vector. |
| `y` | `number` | The y component of the vector. |
| `z` | `number` | The z component of the vector. |

#### Returns

`void`

#### Notes

- Source variant description: "Removes a vector by its variable name."
- Merged 2 source variants with the same signature.
- Additional source descriptions: "Removes a vector by its variable name."

### Overload 2

Removes a previously defined vector from the scene.

```ts
removeVector(vector: object | string): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vector` | `object` \| `string` | The vector object to be removed. Can be the vector itself or its variable name. |

#### Returns

`void`

#### Notes

None.

### Overload 3

Removes a vector by its identifier.

```ts
removeVector(vectorId: string): void
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vectorId` | `string` | The unique identifier of the vector to be removed. |

#### Returns

`void`

#### Notes

None.

## Notes

- Normalized 4 source overload entries into 3 unique signature(s).
- Source variant description: "Removes a vector by its variable name."
- Merged 2 source variants with the same signature.
- Additional source descriptions: "Removes a vector by its variable name."
