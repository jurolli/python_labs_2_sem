from typing import Protocol, Iterable, runtime_checkable
from src.models.task import Task

@runtime_checkable
class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]: ...
    """Любой класс методом get_tasks(self), 
    который возвращающает итерируемый Task считается TaskContract"""