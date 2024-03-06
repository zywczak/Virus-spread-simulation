from vector.Vector2D import *
import random

class Person():

    def __init__(self, state, x, y):
        self._state = state
        self._vector = Vector2D(x, y)
        self._sick_time = 0
        self._time_near_nosymptoms = 0
        self._time_near_symptoms = 0
        self.direction_x = random.choice([-1, 0, 1])
        self.direction_y = random.choice([-1, 0, 1])

    def get_direction_x(self):
        return self.direction_x
    
    def get_direction_y(self):
        return self.direction_y
    
    def change_direction(self):
        self.direction_x = random.choice([-1, 0, 1])
        self.direction_y = random.choice([-1, 0, 1])

    def opposite_direction_y(self):
        self.direction_y = -self.direction_y
    
    def opposite_direction_x(self):
        self.direction_x = -self.direction_x

    def set_coordinate(self, x, y):
        self._vector.set_components(x, y)

    def get_components(self):
        return self._vector.get_components()

    def set_state(self, state):
        self._state = state
    
    def get_state(self):
        return self._state.get_color()
    
    def set_sick_time(self, time):
        self._sick_time = time

    def increase_sick_time(self):
        self._sick_time = self._sick_time+1

    def get_sick_time(self):
        return self._sick_time

    def set_time_near_symptoms(self, time):
        self._time_near_symptoms = time

    def set_time_near_nosymptoms(self, time):
        self._time_near_nosymptoms = time

    def get_time_near_symptoms(self):
        return self._time_near_symptoms
    
    def get_time_near_nosymptoms(self):
        return self._time_near_nosymptoms
    
    def increase_time_near_symptoms(self):
        self._time_near_symptoms += 1

    def increase_time_near_nosymptoms(self):
        self._time_near_nosymptoms += 1

    def abs(self,component):
        return self._vector.abs(component)

    def cdot(self, other_vector):
        return self._vector.cdot(other_vector)