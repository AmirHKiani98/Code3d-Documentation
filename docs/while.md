---
title: While-Loop
sidebar_position: 5
---

# While-Loops
A while loop is a control flow statement that repeatedly executes a block of code as long as a given condition is true.

## Syntax
The basic form checks a condition before each iteration:
```python
while condition:
    ...
```

## Counted loop (using a counter)
Use an explicit counter when you need a specific number of iterations:
```python
i = 0
while i < 12:
    ...
    i += 1
```
- This runs 12 times with i from 0..11 by default.  
- Want 1-based? Initialize `i = 1` and use `i <= 12` (or `i < 13`).

## Conditional loop
While loops are ideal when the number of iterations depends on a condition (e.g., waiting for user input or an event):
```python
ready = False
while not ready:
    ready = check_ready()
```

## Infinite loop
Create a loop that runs until explicitly stopped:
```python
while True:
    ...
    if should_stop:
        break
```

## Breaking the loop
Use break to exit the nearest enclosing while:
```python
while condition1:
    ...
    while condition2:
        ...
        break   # breaks only the inner while
```

## Continue
Continue skips the rest of the current iteration and proceeds to re-evaluate the while condition:
```python
while condition:
    ...
    if skip_this_iteration:
        continue
    # code here runs only when not skipped
```

## else clause (optional)
Some languages (like Python) support while...else: the else block runs if the loop ends normally (not via break):
```python
i = 0
while i < 3:
    i += 1
else:
    # runs because loop terminated normally
    ...
```
- If a break occurs, the else block is skipped.