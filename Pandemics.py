# Created by Mixalhs Karapapas

print("Wait...simulation is loading")

import random
import math
from tkinter import *
from matplotlib import pyplot as plt
import os
import time
import threading


# 0 -> Susceptible
# 1 -> Infected
# 2 -> Immune
# 3 -> Dead

PROBABILITY_OF_GETTING_INFECTED = 0.2
PROBABILITY_OF_DYING = 0.011
PROBABILITY_OF_BEEING_IMMUNED = 0.02
VEL_DIMINISH_RATE = 0.2
CONFORMED_PEOPLE_RATE = 0.7


class House:
    def __init__(self):
        self.people_in_the_house = []

    def add_person(self, person):
        self.people_in_the_house.append(person)
        return True

    def remove_person(self, person):
        if person in self.people_in_the_house:
            self.people_in_the_house.remove(person)
            return True
        return False

class Person:
    def __init__(self, x, y, vx, vy, initial_state, house):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = initial_state
        self.maxInfDis = 5
        self.chance_of_getting_infected = PROBABILITY_OF_GETTING_INFECTED
        self.house = house
        self.in_rq = 0

    def update(self, can_width, can_height):        
        if self.x < can_width:
            self.x += self.vx

        if self.y < can_height:
            self.y += self.vy

        if self.x >= can_width:
            self.vx *= -1
        
        if self.y >= can_height:
            self.vy *= -1

    def move_in_the_house(self):
        self.house.add_person(self)
        self.chance_of_getting_infected -= self.chance_of_getting_infected * 0.5
    
    def move_out_of_the_house(self):
        self.house.remove_person(self)
        self.chance_of_getting_infected = PROBABILITY_OF_GETTING_INFECTED
        
    def self_protection_measures_enabled(self):
        self.chance_of_getting_infected -= self.chance_of_getting_infected * 0.3
    
    def self_protection_measures_disabled(self):
        self.chance_of_getting_infected = PROBABILITY_OF_GETTING_INFECTED

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.day = 0
        self.people = []
        self.num_of_infected = 0
        self.num_of_susceptible = 0
        self.num_of_immune = 0
        self.num_of_dead = 0

        self.hisOfDays = []
        self.hisOfHealthy = []
        self.hisOfInf = []
        self.hisOfImmune = []
        self.hisOfDead = []

        self.is_res_quarantine_enabled = False
        self.is_quarantine_enabled = False
        self.is_quarantine_fi_enabled = False

        self.is_self_pm_enabled = False
        self.is_pm_enabled = False

    def add_people(self, number_of_susceptible, number_of_infectious):
        for _ in range(number_of_susceptible):
            x = random.randint(1, self.width)
            y = random.randint(1, self.height)
            vx = 0.3 + 2.7 * random.random()
            vy = 0.3 + 2.7 * random.random()
            self.people.append(Person(x, y, vx, vy, 0, House()))

        for _ in range(number_of_infectious):
           x = random.randint(1, self.width)
           y = random.randint(1, self.height)
           vx = 0.3 + 2.7 * random.random()
           vy = 0.3 + 2.7 * random.random()
           self.people.append(Person(x, y, vx, vy, 1, House()))

        self.num_of_infected = number_of_infectious
        self.num_of_susceptible = number_of_susceptible

    def quarantine(self):
        if self.is_quarantine_enabled == False:
            for person in self.people:
                if random.random() <= CONFORMED_PEOPLE_RATE:
                    person.vx = 0
                    person.vy = 0
        self.is_quarantine_enabled = True

    def quarantine_fi(self):
        if self.is_quarantine_fi_enabled == False:
            for person in self.people:
                if person.state == 1 and random.random() <= CONFORMED_PEOPLE_RATE:
                    person.move_in_the_house()
                    person.in_rq = 1
        self.is_quarantine_fi_enabled = True


    def restricted_quarantine(self):
        if self.is_res_quarantine_enabled == False:
            for person in self.people:
                if random.random() <= CONFORMED_PEOPLE_RATE:
                    person.move_in_the_house()
                    person.in_rq = 1
        self.is_res_quarantine_enabled = True

    def protection_measures(self):
        if self.is_pm_enabled == False:
            for person in self.people:
                if random.random() <= CONFORMED_PEOPLE_RATE:
                    person.vx = person.vx * VEL_DIMINISH_RATE
                    person.vy = person.vy * VEL_DIMINISH_RATE
        self.is_self_pm_enabled = True

    def self_protection_measures(self):
        if self.is_self_pm_enabled == False:
            for person in self.people:
                if random.random() <= CONFORMED_PEOPLE_RATE:
                    person.self_protection_measures_enabled()
        self.is_self_pm_enabled = True

    def update(self):

        for person in self.people:
            person.update(self.width, self.height)
            if person.state == 1:
                infected_person = person

                # Is he going to dye???
                if random.random() <= PROBABILITY_OF_DYING:
                    infected_person.state = 3
                    self.people.remove(infected_person)
                    self.num_of_infected -= 1
                    self.num_of_dead += 1

                # Is he going to gain immunity???
                if random.random() <= PROBABILITY_OF_BEEING_IMMUNED:
                    infected_person.state = 2
                    self.num_of_infected -= 1
                    self.num_of_immune += 1

                for sus_person in self.people:
                    if sus_person.state == 0 and sus_person.in_rq == 0:
                        d = math.sqrt((infected_person.x - sus_person.x) ** 2 + (infected_person.y - sus_person.y) ** 2)
                        if d <= infected_person.maxInfDis:
                            if random.random() <= sus_person.chance_of_getting_infected:
                                sus_person.state = 1
                                self.num_of_infected += 1
                                self.num_of_susceptible -= 1
        self.day += 1
        self.hisOfDays.append(self.day)
        self.hisOfHealthy.append(self.num_of_susceptible)
        self.hisOfInf.append(self.num_of_infected)
        self.hisOfImmune.append(self.num_of_immune)
        self.hisOfDead.append(self.num_of_dead)


class InitialPanel:
    def __init__(self, canvas):
        self.root = Tk()
        self.maincolor = "cyan"
        self.canvas = canvas
        self.root.title("Pandemic Simulator")
        self.root.geometry("600x450")
        self.root.configure(bg = self.maincolor)
        self.root.resizable(width = False, height = False)

        Label(self.root, text = "Susceptible people:", font = "20px", bg = self.maincolor).place(x = 0, y = 0)
        self.initial_susc_people = Entry(self.root, font = "20px")
        self.initial_susc_people.place(x = 180, y = 0)

        Label(self.root, text = "Infected people:", font = "20px", bg = self.maincolor).place(x = 0, y = 40)
        self.initial_infected_people = Entry(self.root, font = "20px")
        self.initial_infected_people.place(x = 165, y = 40)

        self.start_button = Button(self.root, text = "Go!", font = "20px", command = self.start_the_program)
        self.start_button.place(x = 5, y = 80)

        self.protection_measures_button = Button(self.root, text = "Protection Measures", font = "20px", state = "disabled", command = threading.Thread(target = self.canvas.protection_measures).start())
        self.protection_measures_button.place(x = 65, y = 80)
        
        self.self_protection_measures_button = Button(self.root, text = "Self Protection Measures", font = "20px", state = "disabled", command = threading.Thread(target = self.canvas.self_protection_measures).start())
        self.self_protection_measures_button.place(x = 275, y = 80)
        
        self.quarantine_button = Button(self.root, text = "Quarantine", font = "20px", state = "disabled", command = threading.Thread(target = self.canvas.quarantine).start())
        self.quarantine_button.place(x = 5, y = 140)
        
        self.quarantine_for_infected_people_button = Button(self.root, text = "Quarantine for infected people", font = "20px", state = "disabled", command = threading.Thread(target = self.canvas.quarantine_fi).start())
        self.quarantine_for_infected_people_button.place(x = 130, y = 140)
        
        self.restricted_quarantine_button = Button(self.root, text = "Restricted quarantine!",font = "20px", state = "disabled", command = threading.Thread(target = self.canvas.restricted_quarantine).start())
        self.restricted_quarantine_button.place(x = 5, y = 200)
        
        self.root.mainloop()

    def start_the_program(self):
        threading.Thread(target = self.start).start()

    def start(self):
        
        self.protection_measures_button.configure(state = "active")
        self.self_protection_measures_button.configure(state = "active")
        self.quarantine_button.configure(state = "active")
        self.quarantine_for_infected_people_button.configure(state = "active")
        self.restricted_quarantine_button.configure(state = "active")
        self.start_button.configure(state = "disabled")

        healthy = int(self.initial_susc_people.get())
        infected = int(self.initial_infected_people.get())
        self.canvas.add_people(healthy, infected)
        day = 0

        while True:
            if self.canvas.num_of_infected <= 0:
                self.canvas.num_of_infected = 0

            if self.canvas.num_of_infected == 0:
                self.protection_measures_button.configure(state = "disabled")
                self.self_protection_measures_button.configure(state = "disabled")
                self.quarantine_button.configure(state = "disabled")
                self.quarantine_for_infected_people_button.configure(state = "disabled")
                self.restricted_quarantine_button.configure(state = "disabled")
                self.start_button.configure(state = "active")
                break

            print(f"----- DAY {day} -----")
            print(f"Susceptible people: {self.canvas.num_of_susceptible}")
            print(f"Infected people: {self.canvas.num_of_infected}")
            print(f"Immune people: {self.canvas.num_of_immune}")
            print(f"Dead people: {self.canvas.num_of_dead}")

            self.canvas.update()
            day += 1
            time.sleep(0.1)
            os.system("cls")

        self.root.destroy()
os.system("cls")
print("Done!")
canvas = Canvas(300, 300)
initial_panel = InitialPanel(canvas)

plt.plot(canvas.hisOfDays, canvas.hisOfHealthy, color = "blue", linewidth = 2, label = "Susceptible")
plt.plot(canvas.hisOfDays, canvas.hisOfInf, color = "orange", linewidth = 2, label = "Infected")
plt.plot(canvas.hisOfDays, canvas.hisOfImmune, color = "green", linewidth = 2, label = "Immune")
plt.plot(canvas.hisOfDays, canvas.hisOfDead, color = "red", linewidth = 2, label = "Dead")

plt.xlabel("Days")
plt.ylabel("Number of people")

plt.title("Graph of the pandemia")

plt.legend()

plt.show()