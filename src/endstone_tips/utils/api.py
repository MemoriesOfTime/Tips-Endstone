from endstone import Player

from endstone_tips.utils.variables.base_variable import BaseVariable

variables = []

def str_replace(string: str, player: Player):
    for i in variables:
        for key, value in i.items():
            try:
                variable: BaseVariable = value()
                variable.string = string
                variable.player = player
                variable.on_update()
                string = variable.string
            except Exception as err:
                print(f"变量调用错误：{err}")
    return string

def register_variable(name, variable: type[BaseVariable]):
    variables.append({name: variable})
    pass