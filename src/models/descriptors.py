from typing import Any
from src.common.exeptions import *

class IntDescriptor:
    """Data descriptor для проверки целых чисел в диапазоне"""
    def __init__(self, min_val: int | None, max_val: int | None):
        self.min_val = min_val
        self.max_val = max_val
        self._name = None

    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None: 
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValidationError(f"{self._name} должен быть целым числом")
        if self.min_val is not None and value < self.min_val:
            raise ValidationError(f"{self._name} не может быть меньше {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValidationError(f"{self._name} не может быть больше {self.max_val}")
        setattr(instance, self._name, value)

class NonEmptyStr:
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None: 
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if not isinstance(value, str) or value.strip() == '':
            raise ValidationError(f"Поле {self._name} должно быть непустой строкой")
        setattr(instance, self._name, value.strip())