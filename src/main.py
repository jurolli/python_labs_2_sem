from src.sources.api import ApiSource
from src.sources.file import FileSource
from src.sources.generated import GeneratorSource
from src.task_manager import TaskManager
from src.models.task import Task
from src.models.queue import TaskQueue
import asyncio
from src.executor import AsyncExecutor
from src.handlers import UrgentTaskHandler, DefaultTaskHandler

import logging

logging.basicConfig(
    level=logging.INFO,
    format='\n%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def format_task_output(task: Task):
    urgent_str = "!!!" if task.is_urgent else ""
    output = (
        f"  Задача [{task.id}] {urgent_str}\n"
        f"  Статус: {task.status}\n"
        f"  Создано: {task.created_at}\n"
        f"  Данные: {task.payload}\n"
    )
    print(output)




# для 4 лаболаторной

async def async_main(sync_queue):
    executor = AsyncExecutor(workers_count=2)

    executor.add_handler(UrgentTaskHandler())
    executor.add_handler(DefaultTaskHandler())

    async with executor:
        print("\nЗагрузка задач в асинхронную очередь")
        for task in sync_queue:
            await executor.submit(task)

def main():

    manager = TaskManager()
    gen = GeneratorSource(count=5)
    api = ApiSource()
    file = FileSource("tasks.json")

    manager.add_source(gen)
    manager.add_source(api)
    manager.add_source(file)

    manager.run(printt=format_task_output)

# для третьей лаболаторной работы
    # queue = TaskQueue(sources=manager.sources)

    # for task in queue:
    #     urgent = "!!!" if task.is_urgent else ""
    #     print(f"[{task.priority:2d}] Задача {task.id}: {task.payload} {urgent}")

    queue = TaskQueue(sources=manager.sources)

    asyncio.run(async_main(queue))



if __name__ == "__main__":
    main()

# export PYTHONPATH="${PYTHONPATH}:$(pwd)"