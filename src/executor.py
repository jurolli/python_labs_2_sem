import asyncio
import logging
from src.models.task import Task
from src.models.contract import AsyncHandlerContract

logger = logging.getLogger(__name__)

class AsyncExecutor:
    def __init__(self, workers_count: int = 3):
        self.queue = asyncio.Queue()
        self.workers_count = workers_count
        self.handlers = []
        self._tasks = [] 

    def add_handler(self, handler: AsyncHandlerContract):
        """Добавляем обработчик в список"""
        self.handlers.append(handler)

    async def submit(self, task: Task):
        """Положить задачу в очередь"""
        await self.queue.put(task)

    async def _worker(self, name: str):
        while True:
            task = await self.queue.get()

            try:
                handled = False
                for handler in self.handlers:
                    if await handler.can_handle(task):
                        await handler.handle(task)
                        handled = True
                        break
                
                if not handled:
                    logger.warning(f"Нет обработчика для задачи {task.id}")

            except Exception as e:
                logger.error(f"Воркер {name} нашел ошибку: {e}")
            
            finally:
                self.queue.task_done()

    async def __aenter__(self):
        """Запускается при входе в `async with`"""
        logger.info("Запуск Исполнителя")
        for i in range(self.workers_count):
            worker = asyncio.create_task(self._worker(f"Worker-{i}"))
            self._tasks.append(worker)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Запускается при выходе из `async with`"""
        await self.queue.join()
        
        for worker in self._tasks:
            worker.cancel()
        
        logger.info("Исполнитель завершил работу")