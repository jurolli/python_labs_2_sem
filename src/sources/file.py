from typing import Iterable, Any
from src.models.task import Task
import os
import json
from src.common.exeptions import *
import logging

class FileSource:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self.file_path = file_path

    def read_json(self) -> Any:
        """Чтение задачи из файла"""
        logging.info(f"Попытка чтения задач из файла: {self.file_path}")
        if not os.path.exists(self._file_path):
            logging.error(f"Файл {self.file_path} не найден!")
            raise FileSourceError(f"Файл не найден: {self._file_path}")
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise FileSourceError(f"Ошибка парсинга JSON в файле {self._file_path}: {e}")
        except Exception as e:
            raise FileSourceError(f"Непредвиденная ошибка при чтении файла: {e}")
        return data

    def get_tasks(self) -> Iterable[Task]:
        data = self.read_json()
        if not isinstance(data, list):
            raise ValidationError(f"Корневой элемент в {self._file_path} должен быть списком")
        
        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValidationError(f"Элемент под индексом {index} не является объектом")
        
            if 'id' not in item or 'payload' not in item:
                raise ValidationError(f"Ошибка в элементе {index}: отсутствуют обязательные поля 'id' или 'payload'")
            
            yield Task(
                id=item["id"],
                payload=item["payload"],
                priority=item.get("priority", 1),
                status=item.get("status", "New"),
            )
