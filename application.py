import random
import pygame
import pygame_gui
from pygame.locals import *
from objects.Person import *
from state.IState import *
from objects.Memento import *
from objects.CareTaker import *
from state.ImmuneState import *
from state.HealthyState import *
from state.NoSymptomsState import *
from state.SymptonsState import *

class Symulation():

    def __init__(self, dimensions, size):
        pygame.init()
        height = dimensions[1]
        width = dimensions[0]
        self.win = pygame.display.set_mode((width, height + 50))
        pygame.display.set_caption("Virus spread simulation")
        self.manager = pygame_gui.UIManager((width, height + 50))
        self.button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width/3, height + 10), (100, 30)),
            text='zapis', manager=self.manager
        )

        self.button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width/2, height + 10), (100, 30)),
            text='odczyt', manager=self.manager
        )

        self.dimensions = dimensions
        self.population_list = []

        for i in range(size):
            x = random.randrange(0, self.dimensions[0])
            y = random.randrange(0, self.dimensions[1])

            self.population_list.append(Person(HealtyState(), x, y))

        self.target_fps = 25
        self.clock = pygame.time.Clock()
        self.run = True
        self.caretaker = CareTaker()
        self.time_since_last_update = 0

    def save_memento(self):
        memento = Memento(self.dimensions, self.population_list)
        self.caretaker.add_state(memento)

    def load_memento(self):
        if self.caretaker.has_states():
            memento = self.caretaker.get_last_state()
            self.dimensions = memento.dimensions
            self.population_list = copy.deepcopy(memento.list)

    def Run(self):
        while self.run:
            self.handle_events()

            time_delta = self.clock.tick(25)
            self.time_since_last_update += time_delta

            while self.time_since_last_update >= 1000:
                self.time_since_last_update -= 1000
                self.symulation()
           
            self.manager.update(time_delta)
            self.draw_ui()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button1.rect.collidepoint(event.pos):
                        self.save_memento()

                    if self.button2.rect.collidepoint(event.pos):
                        self.load_memento()

            self.manager.process_events(event)

    def draw_ui(self):
        self.win.fill((255, 255, 255))
        for person in self.population_list:
            self.move(person)
            self.update_position(person)
        
        pygame.draw.rect(
            self.win, (0, 0, 0),
            pygame.Rect(0, self.dimensions[1], self.dimensions[0], 100)
        )

        self.manager.draw_ui(self.win)
        pygame.display.flip()

    def update_position(self, person0):
        color = person0.get_state()
        position = person0.get_components()
        radius = 5
        pygame.draw.circle(self.win, color, (int(position[0]), int(position[1])), radius)

    def move(self, person):
        position = person.get_components()
        
        if random.random() < 0.01:
            person.change_direction()

        x = position[0] + person.get_direction_x() * random.uniform(0, 5) / 5
        y = position[1] + person.get_direction_y() * random.uniform(0, 5) / 5

        if x < 0 or y < 0 or x > self.dimensions[0] or y > self.dimensions[1]:
            if x > self.dimensions[0]:
                if random.random() < 0.5:
                    x = -x
                else:
                    x = 0
            elif x < 0:
                if random.random() < 0.5:
                    x = -x
                else:
                    x = self.dimensions[0]
            elif y > self.dimensions[1]:
                if random.random() < 0.5:
                    y = -y
                else:
                    y = 0
            elif y < 0:
                if random.random() < 0.5:
                    y = -y
                else:
                    y = self.dimensions[1]
                
            if random.random() < 0.1:
                state = random.choice([NoSymptomsState(), SymptomsState()])
            else:
                state = HealtyState()

            person.set_state(state)
            person.set_sick_time(0)
            person.set_time_near_symptoms(0)
            person.set_time_near_nosymptoms(0)
    
        person.set_coordinate(x, y)

    def check_distance(self):
        for i in range(len(self.population_list)):
            for j in range(i + 1, len(self.population_list)):
                person1 = self.population_list[i]
                person2 = self.population_list[j]

                distance = person1.abs(person2.get_components())

                if distance < 20:
                    if person1.get_state() == "green":
                        if person2.get_state() == "red":
                            person1.increase_time_near_symptoms()
                        elif person2.get_state() == "yellow":
                            person1.increase_time_near_nosymptoms()

                    elif person2.get_state() == "green":
                        if person2.get_state() == "red":
                            person2.increase_time_near_symptoms()
                        elif person2.get_state() == "yellow":
                            person2.increase_time_near_nosymptoms()

    def check_state(self, person):
        if person.get_state() == "red" or person.get_state() == "yellow":
            person.increase_sick_time()

            if person.get_sick_time() > random.randrange(25, 30):
                person.set_state(ImmuneState())

        if person.get_state() == "green":
            if person.get_time_near_symptoms() >= 3:
                person.set_state(random.choice([NoSymptomsState(), SymptomsState()]))
            elif person.get_time_near_nosymptoms() >= 3:
                if random.random() <= 0.5:
                    person.set_state(random.choice([NoSymptomsState(), SymptomsState()]))

    def symulation(self):
        self.check_distance()
        for person in self.population_list:
            self.check_state(person)
      
if __name__ == "__main__":
    simulation = Symulation([500, 500], 200)
    simulation.Run()
    pygame.quit()