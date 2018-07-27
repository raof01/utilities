from functools import wraps


def logging(func):
    """
    Simplest decorator
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper():
        print('before calling {0}'.format(func.__name__))
        func()
        print('after calling {0}'.format(func.__name__))

    return wrapper


def logging_args(func):
    """
    Decorator for functions with parameters
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(arg1, arg2):
        print('before calling {0}'.format(func.__name__))
        func(arg1, arg2)
        print('after calling {0}'.format(func.__name__))

    return wrapper


def logging_ret(func):
    """
    Decorator for functions producing return value
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper():
        print('before calling {0}'.format(func.__name__))
        ret = func()
        print('after calling {0}'.format(func.__name__))
        return ret

    return wrapper


def logging_with_level(level):
    """
    Decorator for functions with parameters and producing return value
    :param level:
    :return:
    """
    def inner(func):
        @wraps(func)
        def wrapper(arg):
            print('level {0}: before calling {1}'.format(level, func.__name__))
            ret = func(arg)
            print('level {0}: after calling {1}'.format(level, func.__name__))
            return ret
        return  wrapper
    return inner


@logging
def my_func():
    print('in {0}'.format(my_func.__name__))


@logging_args
def my_func1(arg1, arg2):
    print('in {0}: {1}, {2}'.format(my_func1.__name__, arg1, arg2))


@logging_ret
def my_func2():
    print('in {0}: '.format(my_func1.__name__))
    return 1


@logging_with_level(2)
def my_func3(arg):
    print('in {0}: arg = {1}'.format(my_func3.__name__, arg))
    return arg * arg


if __name__ == '__main__':
    my_func()
    my_func1(1, 2)
    print('{0}() = {1}'.format(my_func2.__name__, my_func2()))
    print('{0}() = {1}'.format(my_func3.__name__, my_func3(4)))
