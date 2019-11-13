
from abc import ABC, abstractmethod

class PluginResult:
    pass

class Plugin(ABC):

    @abstractmethod
    def __init__(self, path: str, src: str):
        pass

    @abstractmethod
    def close(self) -> PluginResult:
        pass