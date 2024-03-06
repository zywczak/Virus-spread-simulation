from state.IState import *

class HealtyState(IState):
    def get_color(self):
        return "green"