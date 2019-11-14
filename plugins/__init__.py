
from abc import ABC, abstractmethod

class PluginResult:
    pass

class Plugin(ABC):

    @abstractmethod
    def close(self) -> PluginResult:
        pass