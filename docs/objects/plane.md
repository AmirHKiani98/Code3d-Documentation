---
title: plane
---

# plane

## Description

A plane in 3D space.

## Properties

| Name | Type | Description |
| --- | --- | --- |
| `normal` | [`vector`](./vector) | No description provided. |
| `point` | [`vertex`](./vertex) | No description provided. |

## Methods Summary

| Method | Returns | Description |
| --- | --- | --- |
| `distanceToPlane` | `number` | Returns the distance between two planes. |
| `distanceToPoint` | `number` | Returns the distance from a point to the plane. |
| `projectPoint` | [`vertex`](./vertex) | Projects a point onto the plane. |

## Methods

### distanceToPlane

Returns the distance between two planes.

#### Signature

```ts
distanceToPlane(plane: plane): number
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `plane` | [`plane`](./plane) | The plane to measure the distance to. |

#### Returns

`number`

#### Notes

None.

### distanceToPoint

Returns the distance from a point to the plane.

#### Signature

```ts
distanceToPoint(point: vertex): number
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `point` | [`vertex`](./vertex) | The point to measure the distance to. |

#### Returns

`number`

#### Notes

None.

### projectPoint

Projects a point onto the plane.

#### Signature

```ts
projectPoint(point: vertex): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `point` | [`vertex`](./vertex) | The point to project onto the plane. |

#### Returns

[`vertex`](./vertex)

#### Notes

None.

## Notes

- Property `normal` is missing a description in source; defaulted to "No description provided."
- Property `point` is missing a description in source; defaulted to "No description provided."
