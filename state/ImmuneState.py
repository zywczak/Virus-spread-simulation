from state.IState import *

class ImmuneState(IState):
    def get_color(self):
        return "blue"