---
title: axis
---

# axis

## Description

An axis in 3D space.

## Properties

| Name | Type | Description |
| --- | --- | --- |
| `direction` | [`vector`](./vector) | No description provided. |

## Methods Summary

| Method | Returns | Description |
| --- | --- | --- |
| `distanceToPoint` | `number` | Returns the distance from a point to the axis. |
| `projectPoint` | [`vertex`](./vertex) | Projects a point onto the axis. |

## Methods

### distanceToPoint

Returns the distance from a point to the axis.

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

Projects a point onto the axis.

#### Signature

```ts
projectPoint(point: vertex): vertex
```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `point` | [`vertex`](./vertex) | The point to project onto the axis. |

#### Returns

[`vertex`](./vertex)

#### Notes

None.

## Notes

- Property `direction` is missing a description in source; defaulted to "No description provided."
