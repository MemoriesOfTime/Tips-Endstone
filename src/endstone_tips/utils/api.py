from endstone import Player

from endstone_tips.utils.variables.base_variable import BaseVariable

variables = []

def str_replace(string: str, player: Player):
    for i in variables:
        for key, value in i.items():
            variable: BaseVariable = value()
            variable.string = string
            variable.player = player
            variable.on_update()
            string = variable.string
    return string

def register_variable(name, variable: type[BaseVariable]):
    variables.append({name: variable})
    pass