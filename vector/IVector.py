from abc import ABC, abstractmethod

class IVector(ABC):
    @abstractmethod
    def abs(self):
        pass

    @abstractmethod
    def cdot(self):
        pass

    @abstractmethod
    def get_components(self):
        pass

    @abstractmethod
    def set_components(self, x, y):
        pass