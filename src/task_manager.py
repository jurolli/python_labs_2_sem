from src.models.task import Task
from src.models.contract import TaskContract
from typing import List, Any
import logging

class TaskManager:
    """Класс, работающий с источниками, соблюдающими контракт"""
    def __init__(self):
        self.sources: List[TaskContract] = []

    def add_source(self, source: Any) -> None:
        if not isinstance(source, TaskContract):
            logging.error(f"Объект {type(source).__name__} не прошел проверку контракта")
            raise TypeError(f"Объект {type(source).__name__} не соответствует контракту")

        self.sources.append(source)
        logging.info(f"Источник {type(source).__name__} успешно добавлен")

    def run(self):
        for source in self.sources:
            print(f"Ресурс {type(source).__name__}")
            print(f"\nОбработка источника: {type(source).__name__}")
            for task in source.get_tasks():
                urgent_str = "[СРОЧНО]" if task.is_urgent else ""
                print(f"Задача [{task.id}]")
                print(f"{task} {urgent_str}")
                print(f"    Описание: {task.description}")
                print(f"    Создано: {task.created_at}")