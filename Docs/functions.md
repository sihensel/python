
# Functions

A function executes code only when it is called.
A function can be passed data and it can return data (just like any mathematical function).



## Definition

```python
def my_function():
	#code here
```

A function gets called by its name.

```python
my_function()
```



## Passing Parameters

You can pass any amount of parameters to a function.

```python
def my_function(number_1, number_2):
	return number_1 * number_2
```

Then, you call the function by it's name and its parameters.

```python
my_function(2, 3)
```

The return value of a function can be storen in a variable.

```python
return_value = my_function(2, 3)
```

In this case, the return\_value would be 6.



### Default Parameters

In the above example, if we don't state all parameters, we get an error.
To avoid this, we can declare default values. So if we don't state a value for a parameter, it gets its default value and we don't get an error. If we declare a value, the default value gets overwritten.

```python
def vacation(duration, country='Norway'):
	return('I\'m going to', country, 'for', duration)
```

Note that non-default values have to be declared before default values and still have to be stated when calling the function.

```python
vacation('1 week', 'Sweden')
vacation('1 week')
```

The returns would be:
`I'm going to Sweden for 1 week` and `I'm going to Norway for 1 week`.

In the same way, lists can be passed to a function.



## Lamda-Functions
