
from datetime import datetime
from src.models.descriptors import NonEmptyStr, IntDescriptor
from src.common.exeptions import *

class Task:
    id = IntDescriptor(min_val=1, max_val=1500)
    priority = IntDescriptor(min_val=1, max_val=15)
    description = NonEmptyStr()
    status = NonEmptyStr()

    def __init__(self, id: int, description: str, priority: int = 1, payload=None, status: str = 'New'):
        self.id = id
        if payload is not None:
            self.description = payload
        else:
            self.description = description
        self.priority = priority
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> str:
        """Публичный API для получения даты (только для чтения)"""
        return self._created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def is_urgent(self) -> bool:
        """Вычисляемое свойство: готовность/срочность"""
        return self.priority > 10

    def __repr__(self):
        return f"Task(id={self.id}, priority={self.priority}, status='{self.status}')"