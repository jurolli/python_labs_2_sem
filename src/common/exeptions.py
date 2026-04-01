
class TaskManagerException(Exception):
    """Базовая ошибка"""
    pass

class InvalidSource(TaskManagerException):
    """Ошибка ресурса"""
    def __init__(self, protocol: str) -> None:
        super().__init__('Ресурс не подходит по протоколу')

class ValidationError(TaskManagerException):
    """Ошибка валидации данных"""
    pass

class FileSourceError(InvalidSource):
    """Ошибка файловых источников"""
    pass