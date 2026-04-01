import pytest
from src.task_manager import TaskManager
from src.models.task import Task

class ValidDummySource:
    """Класс, который не наследуется, но соблюдает контракт"""
    def get_tasks(self):
        yield Task(id=999, description="Dummy")

class InvalidDummySource:
    """Класс, который НЕ соблюдает контракт (нет метода get_tasks)"""
    pass

def test_manager_add_valid_source():
    """Проверка добавления объекта, соблюдающего Protocol"""
    manager = TaskManager()
    source = ValidDummySource()
    manager.add_source(source) # Не должно вызвать ошибку
    assert len(manager.sources) == 1

def test_manager_add_invalid_source():
    """Проверка ошибки при нарушении контракта"""
    manager = TaskManager()
    with pytest.raises(TypeError) as exc:
        manager.add_source(InvalidDummySource())
    assert "не соответствует контракту" in str(exc.value)

def test_manager_run(capsys):
    """Проверка интеграции: запуск менеджера и вывод в консоль"""
    manager = TaskManager()
    manager.add_source(ValidDummySource())
    manager.run()
    
    captured = capsys.readouterr()
    assert "Задача [999]" in captured.out