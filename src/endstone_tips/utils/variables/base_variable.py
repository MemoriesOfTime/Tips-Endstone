from abc import ABC, abstractmethod


class BaseVariable(ABC):

    def __init__(self):
        self.__string: str = ""
        self.player = None
        self.variable = []
        pass

    @abstractmethod
    def on_update(self):
        """
        更新变量
        :return: None
        """
        pass

    def add_variable(self, key: str, value):
        self.variable.append({key: str(value)})
        pass

    @property
    def string(self) -> str:
        return self.__string_replace(self.player)

    @string.setter
    def string(self, string: str):
        self.__string = string
        pass

    def __string_replace(self, player):
        s = self.__string
        for i in self.variable:
            for key, value in i.items():
                s = s.replace(key, value)
        return s