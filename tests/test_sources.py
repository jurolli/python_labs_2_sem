import pytest
import json
from src.sources.generated import GeneratorSource
from src.sources.api import ApiSource
from src.sources.file import FileSource
from src.common.exeptions import FileSourceError

def test_generator_source():
    """Проверка генератора задач"""
    count = 3
    source = GeneratorSource(count=count)
    tasks = list(source.get_tasks())
    assert len(tasks) == count
    assert tasks[0].id == 1

def test_api_source():
    """Проверка API заглушки"""
    source = ApiSource()
    tasks = list(source.get_tasks())
    assert len(tasks) > 0
    assert tasks[0].payload == "Task from API"

def test_file_source_valid(tmp_path):
    """Проверка чтения корректного JSON файла"""
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "tasks.json"
    # Создаем тестовый файл
    data = [{"id": 1, "payload": "File task", "priority": 5}]
    f.write_text(json.dumps(data))
    
    # В твоем FileSource поле в JSON называется 'payload', 
    # а в Task мы добавили 'description'. 
    # Нужно убедиться, что Source правильно мапит поля.
    source = FileSource(str(f))
    tasks = list(source.get_tasks())
    assert len(tasks) == 1
    assert tasks[0].id == 1

def test_file_source_not_found():
    """Проверка ошибки, если файла нет"""
    source = FileSource("non_existent.json")
    with pytest.raises(FileSourceError):
        list(source.get_tasks())