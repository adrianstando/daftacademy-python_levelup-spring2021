import re
from types import FunctionType


# ZADANIE 1
def greetings(func):
    def function(*args):
        txt = func()
        txt_split = txt.split(*args)
        txt_format = [x.lower() for x in txt_split]
        for i in range(len(txt_format)):
            tmp = txt_format[i]
            txt_format[i] = tmp[0].upper() + tmp[1:]

        txt_out = "Hello"
        for x in txt_format:
            txt_out += " "
            txt_out += x

        return txt_out

    return function


# ZADANIE 2
def is_palindrome(func):
    def function(*args):
        word = func(*args)
        regex = re.compile('[^a-zA-ZĄąĘęŃńŻżŹźÓó0-9]')
        txt = regex.sub('', word.lower())
        if txt == txt[::-1]:
            word = word + " - is palindrome"
        else:
            word = word + " - is not palindrome"
        return word

    return function


# ZADANIE 3
def format_output(*args):
    def real_decorator(func):
        def function(*args1):
            dictionary = dict(func(*args1))

            # checking conditions
            dictionary_keys = dictionary.keys()
            for x in args:
                if "__" in x:
                    names = x.split("__")
                    for y in names:
                        if y not in dictionary_keys:
                            raise ValueError
                elif x not in dictionary_keys:
                    raise ValueError

            dictionary_out = {}
            for x in args:
                if "__" in x:
                    names = x.split("__")
                    txt = ""
                    for y in names:
                        if txt == "":
                            txt += dictionary.get(y)
                        else:
                            txt += " "
                            txt += dictionary.get(y)
                    dictionary_out[x] = txt
                else:
                    dictionary_out[x] = dictionary.get(x)

            return dictionary_out

        return function

    return real_decorator


# ZADANIE 4
def add_class_method(clazz):
    def decorator(func):
        setattr(clazz, func.__name__, func)
        return func

    return decorator


def add_instance_method(clazz):
    def decorator(func):

        def func1(self):
            return func()

        setattr(clazz, func.__name__, func1)
        return func

    return decorator


# ------------------PRZYKŁADY------------------

# ZADANIE 1
@greetings
def name_surname():
    return "jan nowak"


# ZADANIE 2
@is_palindrome
def sentence():
    return "annA"


# ZADANIE 3
@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa",
    }


@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa",
    }


# ZADANIE 4
class A:
    pass


@add_class_method(A)
def foo():
    return "Hello!"


@add_instance_method(A)
def bar():
    return "Hello again!"


if __name__ == "__main__":
    print(name_surname())
    print(sentence())
    print(first_func())

    try:
        second_func()
    except ValueError:
        print("Value Error catched!")

    print([x for x, y in A.__dict__.items() if type(y) == FunctionType])
    print(A.foo())

    print([x for x, y in A.__dict__.items() if type(y) == FunctionType])
    print(A().bar())
