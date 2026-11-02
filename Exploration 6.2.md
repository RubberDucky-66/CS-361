Joshua Samuel     
CS 361

# Exploration 6.2: Dependency Injection

1. 
```python
class Frotz:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    # [a bunch of functions that use .left and .right]

left_obj = Left()
right_obj = Right()

f = Frotz(left_obj, right_obj)
```

2. Issues with tightly coupled code include testing difficulties since it is harder to isolate classes. The code becomes harder to reuse when classes are bound to specific implementations, for example maybe we have a special version of Left() we may want to implement. If multiple classes use a third party dependency and it changes, someone will have to visit each and every class that uses it. 