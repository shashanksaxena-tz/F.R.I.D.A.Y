from abc import ABC, abstractmethod

class Integration(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
