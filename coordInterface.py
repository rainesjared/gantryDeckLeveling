from abc import ABC, abstractmethod

class coordInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def probePoints(self):
        pass

    @abstractmethod
    def calculate_rotations(self):
        pass

    @abstractmethod
    def transformPoint(self, p):
        pass
