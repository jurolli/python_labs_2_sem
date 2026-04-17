
class TaskManagerException(Exception):
    """Базовая ошибка"""
    pass

class InvalidSource(TaskManagerException):
    """Ошибка ресурса"""
    pass

class ValidationError(TaskManagerException):
    """Ошибка валидации данных"""
    pass

class FileSourceError(InvalidSource):
    """Ошибка файловых источников"""
    pass