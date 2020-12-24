import datetime

from reusepatterns.singletones import SingletonByName


# Заметка, можно применить стратегию если добавить стратегию логирования
class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text)


# декоратор
def debug(func):
    def inner(*args, **kwargs):
        start = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        result = func(*args, **kwargs)
        end = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print('DEBUG-------->', func.__name__, end, '-', start)
        return result

    return inner


def fake(func):
    def inner(*args, **kwargs):
        print('Hello from fake')
        result = func(*args, **kwargs)

        return result

    return inner