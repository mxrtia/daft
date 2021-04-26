import unittest

#Ex1
from file import greetings


class ExampleTest(unittest.TestCase):
    @greetings
    def show_greetings(self):
        return "joe doe"

    def test_result(self):
        self.assertEqual(self.show_greetings(), "Hello Joe Doe")


if __name__ == "__main__":
    unittest.main()

#Ex2
from file import is_palindrome


class ExampleTest(unittest.TestCase):
    @is_palindrome
    def show_sentence(self):
        return "annA"

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")


if __name__ == "__main__":
    unittest.main()

#Ex3
from file import format_output


class ExampleTest(unittest.TestCase):
    @format_output("first_name")
    def show_dict(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def test_result(self):
        self.assertEqual(self.show_dict(), {"first_name": "Jan"})


if __name__ == "__main__":
    unittest.main()
    
#Ex4    
from file import add_class_method, add_instance_method

class A:
    pass

class Dummy:
    def method(self):
        return "instance method called"

    @add_class_method
    def classmethod(cls):
        return "class method called"

    @add_instance_method
    def staticmethod():
        return "static method called"


@add_class_method(Dummy)
def foo():
    return "Hello!"

@add_instance_method(Dummy)
def bar():
    return "Hello again!"

print(Dummy.foo())
print(Dummy().bar())

class ExampleClass:
    pass


@add_class_method(ExampleClass)
def cls_method():
    return "Hello!"


@add_instance_method(ExampleClass)
def inst_method():
    return "Hello!"


class ExampleTest(unittest.TestCase):
    def test_result(self):
        self.assertEqual(ExampleClass.cls_method(), cls_method())
        self.assertEqual(ExampleClass().inst_method(), inst_method())


if __name__ == "__main__":
    unittest.main()