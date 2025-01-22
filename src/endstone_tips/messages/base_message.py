from abc import ABC
from enum import Enum


class BaseMessage(ABC):

    def __init__(self, world: str, show: bool):
        self.world = world
        self.show = show
        pass



    pass


class MessageType(Enum):
    CHAT_MESSAGE = 1
