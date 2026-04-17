from typing import Protocol, Iterable, runtime_checkable
from src.models.task import Task

@runtime_checkable
class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]: ...
    """Любой класс с методом get_tasks(self), 
    который возвращает итерируемый Task считается TaskContract"""