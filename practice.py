from abc import ABC, abstractmethod

class Shape(ABC):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def details(self):
        pass


class User(Shape):
    def details(self):
        print(self.name,self.age)
    def info(self):
        print(self.age)

u = User("nazmul", 23)
u.details()