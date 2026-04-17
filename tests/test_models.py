import pytest
from src.models.task import Task
from src.common.exeptions import ValidationError

def test_task_creation_valid():
    """Проверка создания корректной задачи"""
    task = Task(id=1, payload="Тестовая задача", priority=5)
    assert task.id == 1
    assert task.payload == "Тестовая задача"
    assert task.priority == 5
    assert task.status == "New"
    assert hasattr(task, "created_at")

def test_task_invalid_id():
    """Проверка валидации ID (должен быть > 0)"""
    with pytest.raises(ValidationError):
        Task(id=0, payload="Ошибка")

def test_task_invalid_priority():
    """Проверка границ приоритета (1-30)"""
    with pytest.raises(ValidationError):
        Task(id=1, payload="Ошибка", priority=50)

def test_task_empty_payload():
    """Проверка на пустую строку в описании"""
    with pytest.raises(ValidationError):
        Task(id=1, payload="  ")

def test_task_urgent_property():
    """Проверка вычисляемого свойства is_urgent"""
    normal_task = Task(id=1, payload="Обычная", priority=5)
    urgent_task = Task(id=2, payload="Срочная", priority=12)
    assert normal_task.is_urgent is False
    assert urgent_task.is_urgent is True

def test_task_addition():
    """Проверка сложения двух задач (__add__)"""
    task1 = Task(id=1, payload="Task 1", priority=5)
    task2 = Task(id=2, payload="Task 2", priority=15)
    
    combined = task1 + task2
    
    assert combined.id == 1000
    assert combined.payload == "Task 1 & Task 2"
    assert combined.priority == 15 
    assert combined.status == "Combined"

def test_task_radd():
    """Проверка сложения с нулем для встроенной функции sum() (__radd__)"""
    task = Task(id=1, payload="Task 1", priority=5)
    
    result = 0 + task
    assert result is task