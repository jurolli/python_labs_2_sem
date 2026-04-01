from typing import Iterable
from src.models.task import Task

class ApiSource:
    """Имитирует получение данных из API"""
    def get_tasks(self) -> Iterable[Task]:
        yield Task(id=100, description="Task from API", priority=12)