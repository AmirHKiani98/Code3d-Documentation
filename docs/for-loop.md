---
title: For-Loop
sidebar_position: 4
---


# For-Loops
A for loop is a programming control flow statement used to execute a block of code repeatedly a specific, known number of times.

## Syntax
`for` is the iterator that we use for looping over an array. It's almost identical to `for` conditional statement in python

## Counted loop
```code
for object in objects:
    ...
```

* 12 is the count
* `-> i`: binds the index (0..11 by default)

Want 1-based?
```code
for i in range(12)
    ...
```
We talk about `range` in-built function. It's similar as python

## Key/value loop
```code
for id, object in objects
    ...
```
This only and only will be useful if objects is a `list` of objects such as [(item11, item12), (item21, item22), ...]

## list loop
```code
for object in objects:
    ...
```

## Breaking the loop
```code
for object in objects:
    ...
    for objects in objects2:
        ...
        break
```
This will break the second `for` and not the first one

## Continue
```code
for object in objects:
    ...
    for objects in objects2:
        ...
        continue
```
This will continue the second `for` and does not run whatever comes after that line in the second `for`


