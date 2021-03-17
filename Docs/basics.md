
# Python Basics



## Comments

You can declare inline comments with `#`.
For a block-comment, use `'''`:

```python
# This is a inline comment
a = 5 # can also be placed after code

'''
This is a block comment
'''
```



## Math symbols

Symbol | Meaning
--- | ---
`+ - * /` | as usual
`//` | floor division (division without remiander: `17 // 3 = 5`)
`%` | mod operator (calculates remainder: `17 % 3 = 2`)
`**` | power calculation (`2 ** 3 = 8`)



## Comparative Operators

Operator | Meaning
--- | ---
`<` | smaller than
`>` | greater than
`<=` | smaller or equals
`>=` | greater or equals
`==` | equals
`!=` | not equals



## Declare Variables

Variables are declared without a type. Python automatically recognizes the type.

```python
a = 5   # This is an integer
b = 5.1   # This is a float
c = 'Hello World!'   # This is a string
```

You can also declare multiple variables at once (altough this is bad style).

```python
a, b = 10, 3
```

Booleans will aways begin with a __capital__ letter.

```python
True
False
```



## Strings

Strings are declare with either `'` or `"`.

```python
mystring = 'Hello World'
mystring = "Hello World"
```

All letters are counted towards a string, except `\`. This is Pythons escape character.
For example, to issue a new line in a string, use `\n`.
To include escape characters, use an `r` for `raw` in front of the string.

```python
print('This string has an \n escape charater.')
print(r'C:\User\Public\')
```

Two strings in one line will be merged.

```python
print('PY' 'THON')   # --> 'PYTHON'
```

You can use math symbols to merge strings.
This also works with variables.

```python
print(2 * 'Hello' + 'World')   # --> 'Hello Hello World'
print(var1 + 'Hello')   # --> 'Var1Hello`
print(var1, 'Hello')   # --> 'Var1 Hello'
```

### Sections of a String

Strings can be divided into pieces (same as lists).

```python
word = 'Python'
print(word[0], word[3])   # --> 'P h'
```

The same works with negative numbers. In this case you start counting from the right of the string.

```python
print(word[-1], word[-3])   # --> 'n h'
```

If you want a whole section instead of one symbol, just declare the range in the square brackets.
You can also omit one of the limits, so all of the remainig string will be displayed.
__Note:__ The right limit is __included__, whereas the left limit is __excluded__.

```python
print(word[0:3])   # --> 'Pyt'
print(word[2:])   # --> 'thon'
print(word[:2] + word[2:])   # --> 'Python' (the whole string)
```

The same works with negative limitations, but the reading direction stays left-to-right this time.

```python
print(word[-2:])   # --> 'on'
print(word[:-2])   # --> 'Pyth'
```

If the interval range is invalid, Python reads the string to the end. If the left limitation is too large, the output is empty.
However, no error will be output for both.

You can determine the length of a string with `len()`.

```python
prtint(len(word))   # --> 6
```



## Lists

A list is what other languages refer to as an array.
A list gets implemented with square brackets `[]`.
It can contain integers, floats or strings.

```python
mylist = [1, 3, 5]
mylist = ['Hello', 'World', 1, 3.1]
```

Segments of lists can be addressed and read the same way you can with strings.
Adding elements to an existing list is quite easy:

```python
mylist += [7, 9, 11]
mylist.insert(2, 'Python')   # state the index first, then the value
```

To edit single values of a list, use the index of the value and set a new one.

```python
lmylist[3] = 'This is a new value now!'
```

The same can be done with a range of values.
__Note:__ the right limitation is __exclusive__.

```python
mylist[2:4] = [20, 21]
```

A list can be emptied with `mylist = mylist[:]`.

You can get the length of a list with the `len()` function.

```python
print(len(mylist))
```



### Nested Lists

List can be nested with other lists, so one list can contain multiple lists.

```python
list1 = [1, 3, 5]
list2 = ['Hello', 'World']
list3 = [list1, list2]   # list3 contains list1 and list2
```

The output can be addressed like this:

Command | Output
--- | ---
`print(list3)` | `[[1, 3, 5], ['Hello', 'World']]`
`print(list3[0]` |  `[1, 3, 5]`
`print(list3[0][1]` | `3`



### Sorting Lists

The `sort()`-function allows to sort lists.
__Note:__ This way the initial list gets overridden. If you want to keep the original (usorted list), see below.

```python
mylist = [3, 1, 7, 5]
mylist.sort()   # This overrides the initial list
```

To avoid overriding the initial list, use the `sorted()`-function.

```python
sorted_list = sorted(mylist)
```

To reverse the sort order, set `reverse=True`.


```python
mylist.sort(reverse=True)
sorted_list = sorted(mylist, reverse=True)
```



## Loops

Loops are not defined with curly brackets like in C or Java, instead they are managed with intendations.

### While

```python
while a < 10:
	print(a)
	a += 1
```



### If

Python uses `elif` instead of else if in other languages.

```python
if x < 0:
	print('x is smaller than zero')
elif x == 0:
	print('x is exactly zero')
else:
	print('x is greater than zero`)
```



### For

In Python, for-Loops are mainly used to iterate over lists or strings.

```python
words = ['cat', 'window', 'dishwasher']

for x in words:
	print(x, len(x))
```

The output is as follows:

```python
cat 3
window 6
dishwasher 10
```



## Range

The `range()`-function generates a sequence of integers.
The schema of the `range()`-function is `range(start, stop, step)`.
The `stop` value is always __exclusive__.

```python
range(5)          # generates the values from 0 to 4
range(0, 11)      # generates the values from 0 to 10
range(4, 11, 2)   # generates every other value from 4 to 10 (4, 6, 8 and 10)
```
