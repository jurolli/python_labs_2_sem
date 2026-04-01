import pytest
from src.models.task import Task
from src.common.exeptions import ValidationError

def test_task_creation_valid():
    """Проверка создания корректной задачи"""
    task = Task(id=1, description="Тестовая задача", priority=5)
    assert task.id == 1
    assert task.description == "Тестовая задача"
    assert task.priority == 5
    assert task.status == "New"
    assert hasattr(task, "created_at")

def test_task_invalid_id():
    """Проверка валидации ID (должен быть > 0)"""
    with pytest.raises(ValidationError):
        Task(id=0, description="Ошибка")

def test_task_invalid_priority():
    """Проверка границ приоритета (1-15)"""
    with pytest.raises(ValidationError):
        Task(id=1, description="Ошибка", priority=20)

def test_task_empty_description():
    """Проверка на пустую строку в описании"""
    with pytest.raises(ValidationError):
        Task(id=1, description="  ")

def test_task_urgent_property():
    """Проверка вычисляемого свойства is_urgent"""
    normal_task = Task(id=1, description="Обычная", priority=5)
    urgent_task = Task(id=2, description="Срочная", priority=12)
    assert normal_task.is_urgent is False
    assert urgent_task.is_urgent is True