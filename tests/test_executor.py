import pytest
import asyncio
from src.models.task import Task
from src.executor import AsyncExecutor
from src.handlers import UrgentTaskHandler, DefaultTaskHandler

pytestmark = pytest.mark.asyncio

async def test_handlers_routing():
    """Проверка, что обработчики правильно выбирают свои задачи (can_handle)"""
    urgent_task = Task(id=1, payload="Urgent Task", priority=20)
    normal_task = Task(id=2, payload="Normal Task", priority=5)

    urgent_handler = UrgentTaskHandler()
    default_handler = DefaultTaskHandler()

    assert await urgent_handler.can_handle(urgent_task) is True
    assert await urgent_handler.can_handle(normal_task) is False

    assert await default_handler.can_handle(normal_task) is True
    assert await default_handler.can_handle(urgent_task) is False


async def test_handlers_execution():
    """Проверка логики самих обработчиков (изменение статусов)"""
    urgent_task = Task(id=1, payload="Urgent", priority=20)
    normal_task = Task(id=2, payload="Normal", priority=5)
    
    urgent_handler = UrgentTaskHandler()
    await urgent_handler.handle(urgent_task)
    assert urgent_task.status == "Urgent Completed"

    default_handler = DefaultTaskHandler()
    await default_handler.handle(normal_task)
    assert normal_task.status == "Completed"

async def test_executor_add_handler():
    """Проверка добавления обработчиков в Исполнителя"""
    executor = AsyncExecutor()
    assert len(executor.handlers) == 0
    
    executor.add_handler(DefaultTaskHandler())
    assert len(executor.handlers) == 1

async def test_executor_full_processing():
    """Интеграционный тест: Исполнитель должен успешно обработать разные задачи"""
    executor = AsyncExecutor(workers_count=2)
    executor.add_handler(UrgentTaskHandler())
    executor.add_handler(DefaultTaskHandler())

    t1 = Task(id=1, payload="T1", priority=15)
    t2 = Task(id=2, payload="T2", priority=5)

    async with executor:
        await executor.submit(t1)
        await executor.submit(t2)

    assert t1.status == "Urgent Completed"
    assert t2.status == "Completed"

