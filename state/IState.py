from abc import ABC, abstractmethod

class IState(ABC):
    @abstractmethod
    def get_color(self):
        pass