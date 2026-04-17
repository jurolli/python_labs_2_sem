import pytest
from src.task_manager import TaskManager
from src.models.task import Task
from src.main import format_task_output

class ValidDummySource:
    """Класс, который не наследуется, но соблюдает контракт"""
    def get_tasks(self):
        yield Task(id=999, payload="Dummy")

class InvalidDummySource:
    """Класс, который НЕ соблюдает контракт (нет метода get_tasks)"""
    pass

def test_manager_add_valid_source():
    """Проверка добавления объекта, соблюдающего Protocol"""
    manager = TaskManager()
    source = ValidDummySource()
    manager.add_source(source)
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
    manager.run(format_task_output)
    
    captured = capsys.readouterr()
    assert "Задача [999]" in captured.out