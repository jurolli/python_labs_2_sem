from src.models.task import Task
from src.models.contract import TaskContract
from typing import List, Any
import logging

logger = logging.getLogger(__name__)

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

    def run(self, printt):
        for source in self.sources:
            logger.info(f"Начало получения данных из: {type(source).__name__}")
            count = 0
            for task in source.get_tasks():
                count += 1
                logger.info(f"Извлечена задача ID {task.id} из {type(source).__name__}")
            if printt:
                printt(task)
            logger.info(f"Источник {type(source).__name__} обработан. Всего задач: {count}")

