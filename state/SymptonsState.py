from state.IState import *

class SymptomsState(IState):
    def get_color(self):
        return "red"