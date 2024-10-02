from abc import ABC, abstractmethod


class BaseTask(ABC):

    @abstractmethod
    def on_update(self):
        pass