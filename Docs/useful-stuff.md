# Useful stuff

## List comprehension

Used to generate lists and dictionaries with less code

```python
numbers =[i for i in range(11)] 
squares = [i**2 for i in numbers]
print(numbers)
print(squares)
```



## Lamda functions

Used to create inline functions. Useful when no full-sized function is needed.

```python
x = lambda a, b: a * b
print(x(4, 5))
```

Test if a value is above a certain threshold

```python
check_value = lambda x: x > 1
check_value(0.7)	#returns False
check_value(1.3)	#returns True
```



## Assign multiple variables to the same value

Assigns all three variables `a`, `b` and `c` to the value 5.

```python
a = b = c = 5
```



## Assign values from a ordered list

All items of a list can be assigned to variables, if there are the same amount of variables.
In this example all list elements get assigned to the provided variables, from left to right, respectively.

```python
colors = ['red', 'blue', 'green', 'yellow']
firetruck, water, flower, sun, = colors

print(firetruck, water, flower, sun)
```

After executing this snippet, the variables have the following values.

```python
firetruck = 'red'
water = 'blue'
leaf = 'green'
flower = 'yellow'
```

