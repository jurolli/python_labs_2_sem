import asyncio
import logging
from src.models.task import Task

logger = logging.getLogger(__name__)

class UrgentTaskHandler:
    """Берет только срочные задачи"""
    async def can_handle(self, task: Task) -> bool:
        return task.is_urgent

    async def handle(self, task: Task) -> None:
        logger.info(f"[URGENT] Началась обработка срочной задачи {task.id}")
        await asyncio.sleep(1)  # Имитируем работу 
        task.status = "Urgent Completed"
        logger.info(f"[URGENT] Задача {task.id} завершена")

    
class DefaultTaskHandler:
    """Берет все остальные задачи"""
    async def can_handle(self, task: Task) -> bool:
        return not task.is_urgent

    async def handle(self, task: Task) -> None:
        logger.info(f"[DEFAULT] Обработка обычной задачи {task.id}")
        await asyncio.sleep(0.5)

        task.status = "Completed"
        logger.info(f"[DEFAULT] Задача {task.id} завершена")