import pytest
from src.models.task import Task
from src.models.queue import TaskQueue

class DummySource:
    """Вспомогательный источник задач для тестирования очереди"""
    def __init__(self, tasks):
        self.tasks = tasks
    
    def get_tasks(self):
        return self.tasks

def test_queue_priority_ordering_and_fifo():
    """
    Проверка:
    1. Задачи отдаются в порядке убывания приоритета.
    2. При равном приоритете сохраняется FIFO (кто первый добавлен, тот первый вышел).
    """
    t1 = Task(id=1, payload="A", priority=5)
    t2 = Task(id=2, payload="B", priority=15)
    t3 = Task(id=3, payload="C", priority=15)
    t4 = Task(id=4, payload="D", priority=1)

    source = DummySource([t1, t2, t3, t4])
    queue = TaskQueue([source])
    
    result = list(queue)
    
    assert len(result) == 4
    assert result[0] == t2
    assert result[1] == t3 
    assert result[2] == t1 
    assert result[3] == t4  

def test_queue_multiple_iterations():
    """Проверка повторного обхода очереди"""
    source = DummySource([Task(id=1, payload="A", priority=5)])
    queue = TaskQueue([source])
    
    iter1 = list(queue)
    iter2 = list(queue)
    
    assert len(iter1) == 1
    assert len(iter2) == 1
    assert iter1[0].id == iter2[0].id

def test_queue_filter_by_status():
    """Проверка ленивой фильтрации по статусу"""
    source = DummySource([
        Task(id=1, payload="A", priority=10, status="New"),
        Task(id=2, payload="B", priority=20, status="In Progress"),
        Task(id=3, payload="C", priority=5, status="New")
    ])
    queue = TaskQueue([source])
    
    filtered = list(queue.filter_by_status("New"))
    
    assert len(filtered) == 2
    assert filtered[0].id == 1
    assert filtered[1].id == 3

def test_queue_filter_by_priority():
    """Проверка ленивой фильтрации по приоритету"""
    source = DummySource([
        Task(id=1, payload="A", priority=5),
        Task(id=2, payload="B", priority=15),
        Task(id=3, payload="C", priority=25)
    ])
    queue = TaskQueue([source])
    
    filtered = list(queue.filter_by_priority(15))
    
    assert len(filtered) == 2
    assert filtered[0].priority == 25
    assert filtered[1].priority == 15

def test_queue_sum_integration():
    """Проверка работы встроенной функции sum() на объекте TaskQueue"""
    source = DummySource([
        Task(id=1, payload="TaskA", priority=5),
        Task(id=2, payload="TaskB", priority=20)
    ])
    queue = TaskQueue([source])
    
    combined = sum(queue)
    
    assert combined.id == 1000
    assert "TaskA" in combined.payload
    assert "TaskB" in combined.payload
    assert combined.priority == 20

def test_custom_heap_empty_pop():
    """Проверка исключения при извлечении из пустой кучи напрямую"""
    with pytest.raises(IndexError, match="пустой"):
        TaskQueue._heap_pop([])