from descriptors import StringField, IntegerField


class Model:
    def __init__(self, **kwargs):
        self.data = {}

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Person(Model):
    name = StringField()
    age = IntegerField()


person = Person(name='Andrey', age=1998)
print(person.data)
print(person.age)
print(person.name)
