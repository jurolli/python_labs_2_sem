from src.sources.api import ApiSource
from src.sources.file import FileSource
from src.sources.generated import GeneratorSource
from src.task_manager import TaskManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    manager = TaskManager()
    gen = GeneratorSource(count=5)
    api = ApiSource()
    file = FileSource("tasks.json")

    manager.add_source(gen)
    manager.add_source(api)
    manager.add_source(file)

    manager.run()

    try:
        manager.add_source('Lvf reejhrt sdfg')
    except TypeError as e:
        print(f"\nОшибка проверки контракта: {e}")


if __name__ == "__main__":
    main()