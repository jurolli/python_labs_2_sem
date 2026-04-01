from typing import Iterable
from src.models.task import Task

class GeneratorSource:
    """Генерирует задачи"""
    def __init__(self, count: int = 1):
        self.task_count = count
        if count < 0:
            raise ValueError('Не верное количество задач')

    def get_tasks(self) -> Iterable[Task]:
        for i in range(1, self.task_count + 1):
            yield Task(id=i, description=f"Generated task {i}")