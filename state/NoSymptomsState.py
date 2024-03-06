from state.IState import *

class NoSymptomsState(IState):
    def get_color(self):
        return "yellow"