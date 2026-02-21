---
title: In-Built Functions
---

# In-Built Functions
These functions follow Python behavior exactly.

## Quick Reference

| Name | Signature | Returns |
| --- | --- | --- |
| `filter` | `filter(function, iterable)` | An iterator of items where `function(item)` is truthy |
| `range` | `range(stop)` / `range(start, stop[, step])` | An immutable sequence of integers |
| `sort` | `list.sort(*, key=None, reverse=False)` | `None` (sorts the list in place) |
| `lambda` | `lambda args: expression` | An anonymous function |

## `filter`

### Definition
`filter(function, iterable)` builds an iterator from the elements of `iterable` for which `function(element)` is true.

If `function` is `None`, it removes falsy values.

### Example
```python
numbers = [0, 1, 2, 3, 4, 5]
evens = list(filter(lambda n: n % 2 == 0, numbers))
# [0, 2, 4]
```

## `range`

### Definition
`range` creates an immutable sequence of numbers.

- `range(stop)` -> starts at `0`, steps by `1`, stops before `stop`
- `range(start, stop)` -> starts at `start`, steps by `1`, stops before `stop`
- `range(start, stop, step)` -> starts at `start`, steps by `step`, stops before `stop`

`step` cannot be `0`.

### Example
```python
list(range(5))         # [0, 1, 2, 3, 4]
list(range(2, 10, 2))  # [2, 4, 6, 8]
list(range(5, 0, -1))  # [5, 4, 3, 2, 1]
```

## `sort`

### Definition
In Python, `sort` is a list method:

`list.sort(*, key=None, reverse=False)`

- Sorts the list in place
- Returns `None`
- Uses stable sorting (equal elements keep original order)
- `key` is a function used to extract a comparison key from each element

### Example
```python
users = [{"name": "Noah", "age": 30}, {"name": "Ava", "age": 22}]
users.sort(key=lambda user: user["age"])
# [{"name": "Ava", "age": 22}, {"name": "Noah", "age": 30}]
```

## `lambda`

### Definition
`lambda` creates a small anonymous function using a single expression:

`lambda parameters: expression`

- Can take any number of parameters
- Must contain exactly one expression (not statements)
- Returns the value of that expression

### Example
```python
square = lambda x: x * x
square(6)  # 36
```

You will often see `lambda` used with `filter`, `sort(key=...)`, and similar APIs.

### With multiple arguments
```python
add = lambda a, b: a + b
add(3, 5)  # 8

greet = lambda name, greeting: f"{greeting}, {name}!"
greet("Ava", "Hello")  # "Hello, Ava!"
```
