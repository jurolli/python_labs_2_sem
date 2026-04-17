
from datetime import datetime
from src.models.descriptors import NonEmptyStr, IntDescriptor
from src.common.exeptions import *

class Task:
    id = IntDescriptor(min_val=1, max_val=1000)
    priority = IntDescriptor(min_val=1, max_val=30)
    payload = NonEmptyStr()
    status = NonEmptyStr()

    def __init__(self, id: int, payload: str, priority: int = 1, status: str = 'New'):
        self.id = id
        self.payload = payload
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> str:
        """для получения даты (только для чтения)"""
        return self._created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def is_urgent(self) -> bool:
        """срочная ли задача"""
        return self.priority > 10

    def __repr__(self):
        return f"Task(id={self.id}, priority={self.priority}, status='{self.status}')"

    def __add__(self, other):
        """Для лабы 3 сложение задач"""
        if not isinstance(other, Task):
            raise TypeError("Складывать можно только задачи")
        
        new_payload = f"{self.payload} & {other.payload}"
        new_priority = max(self.priority, other.priority)

        return Task(id=1000, payload=new_payload, priority=new_priority, status="Combined")

    def __radd__(self, other):
        """сложение справа, чтоб срабатывало 0 + Task = Task"""
        if other == 0:
            return self
        return self.__add__(other)