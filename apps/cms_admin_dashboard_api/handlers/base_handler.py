import asyncio
from typing import Any
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, *args, **kwargs): ...

    def __call__(self, *args, **kwargs) -> Any:
        return self.handle(*args, **kwargs)


class BaseAsyncHandler(BaseHandler):
    def __call__(self, *args, **kwargs) -> Any:
        result = self.handle(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return result
        return result
