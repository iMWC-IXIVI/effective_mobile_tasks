from exceptions import DescriptorValueError


class StringField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.data.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise DescriptorValueError('Значение поля должна быть строка')
        instance.data[self.name] = value


class IntegerField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.data.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise DescriptorValueError('Значение поля должно быть целое число')
        instance.data[self.name] = value
