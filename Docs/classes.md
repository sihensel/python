# Classes

## Class definition

A class needs a class name.
The constructor is defined with the `__init__` function.
`self` is a reference the the object itself. It could be named differently, but everyone agrees to name it `self`, it also makes the most sense.
An object is created with the class name and assigned to a variable. When an object gets created, the `__init__` function gets executed.

```python
class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

myPerson = person('Paul', 25)

print(myPerson.name)
print(myPerson.age)
```



## Inheritance

Classes can inherit from one another. All methods and variables from the upper class are available in the lower class.
To implement inheritance, specify the father class in brackets.

```python
class employee(person):
    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary
        
myEmployee = employee('Paul', 25, 65.000)
```

In this example, our class inherits from the previously created class `person`.  Since the variables `name` and `age` are already available because of the inheritance, we don't need to specify them again. We can call the constructor of the upper class with the `super` method and the needed input parameters.
In this case we create a new employee called Paul at the age of 25 with a salary of 65.000 $.



## Abstract classes

First, you have to import the `abc` module, and have your class inherit from ABC (Abstract Base Class)

```python
# ABC = Abstract Base Class
from abc import ABC, abstractmethod

class parent(ABC):

    @abstractmethod
    def test_method(self):
        pass

class child(parent):
    def test_method(self, text):
        self.text = text

test1 = child()
test1.test_method("HELLO")

print(test1.text)
```

