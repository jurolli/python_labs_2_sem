from typing import Any, Iterable, Iterator, List, Any
from src.models.task import Task
from src.models.contract import TaskContract
import itertools


class TaskQueue:

    def __init__(self, sources: Iterable[TaskContract]):
        self.sources = list(sources)

    @staticmethod
    def _heap_up(heap: List[Any], index: int) -> None:
        """Проталкивает минимальный элемент в начало (на верх)"""
        parent = (index - 1) // 2

        while index > 0 and heap[index] < heap[parent]:
            heap[parent], heap[index] = heap[index], heap[parent]
            index = parent
            parent = (index - 1) // 2

    @staticmethod
    def _heap_down(heap: List[Any], index: int) -> None:
        n = len(heap)

        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right

        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            TaskQueue._heap_down(heap, smallest) 

    @staticmethod
    def _heap_push(heap: List[Any], item: Any) -> None:
        """Добавляет элемент в кучу"""
        heap.append(item)
        TaskQueue._heap_up(heap, len(heap) - 1)
    
    @staticmethod
    def _heap_pop(heap: List[Any]) -> Any:
        """Извлекает и возвращает наименьший элемент из кучи"""
        if not heap:
            raise IndexError("Извлечение из пустой кучи")

        last = heap.pop()

        if heap:
            result = heap[0]
            heap[0] = last
            TaskQueue._heap_down(heap, 0)
            return result
        return last

    def __iter__(self)  -> Iterator[Task]:

        heap = []

        counter = itertools.count()

        for source in self.sources:
            for task in source.get_tasks():
                 self._heap_push(heap, (-task.priority, next(counter), task))

        while heap:
            yield self._heap_pop(heap)[2]

    def filter_by_status(self, status: str) -> Iterator[Task]:
        return (task for task in self if task.status == status)

    def filter_by_priority(self, min_priority: int) -> Iterator[Task]:
        return (task for task in self if task.priority >= min_priority)