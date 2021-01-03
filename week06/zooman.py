"""
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')

定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
"""
from abc import ABCMeta, abstractmethod


class Zoo(object):
    def __init__(self, name):
        self.name = name

    def add_animal(self, animal):
        """将实例化的对象直接添加到动物园实例的属性字典中"""
        if not animal.__class__.__name__ in self.__dict__:
            self.__dict__[animal.__class__.__name__] = animal

class Animal(metaclass=ABCMeta):
    """"""

    def __init__(self, name, animal_type, bodily_from, character):
        self.name = name
        self._animal_type = animal_type
        self._bodily_from = bodily_from
        self._character = character


    @property
    def animal_type(self):
        """动物类型"""
        return self._animal_type

    @animal_type.setter
    def animal_type(self, value):
        if not value in ('食肉', '食草'):
            raise TypeError('动物只能是食肉或者食草')
        self._animal_type = value

    @property
    def bodily_from(self):
        return self._bodily_from

    @bodily_from.setter
    def bodily_from(self, value):
        if not value in ('大', '中', '小'):
            raise TypeError('动物体型只能是大,小,中')
        self._bodily_from = value

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        if not value in ('温顺', '残暴'):
            raise TypeError('动物性格只能是温顺或者残暴')
        self._character = value

    @property
    def is_beast(self):
        num = {
            '大型': 1,
            '中型': 2,
            '小型': 3}[self.bodily_from]

        if num >= 2 and self.animal_type is '食肉动物':
            return True
        return False

    @abstractmethod
    def sound(self):
        """叫声"""
        raise NotImplemented


class Cat(Animal):

    @property
    def sound(self):
        return '喵~'

    def as_pet(self):
        return self.is_beast

class Dog(Animal):

    @property
    def sound(self):
        return '汪~'

    def as_pet(self):
        return self.is_beast

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(cat1.sound)
    print(have_cat)
