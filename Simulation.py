
# coding: utf-8

# In[18]:


import random
import numpy as np
import matplotlib.pyplot as plt
import pygame
import pygame.gfxdraw


#Particle class. Takes in paramters, the number of dimension (D)
#The particle will have D parameters for position, and D parameters for velocity
#Initialize all the particles. Also decide their environment.

class Person:
    '''
        dim = Defines dimensions of our city.
        flag = determines wether our person is susceptible(0), infected(1) or removed(2)
    '''
    '''
        We're assuming the limits of our city to be from 0 to 1. Also, we assume symmetry across different dimensions
    '''
    def __init__(self, dim = 2, flag = 0):
        self.dim = dim
        self.flag = flag
        self.infection_time = 0
        self.post_incubation = -1

        self.initialize_position()
        #self.initialize_velocity(dim)

    def initialize_position(self):
        self.position = []
        for i in range(self.dim):
            self.position.append(random.random())#can have different methods of initialization.
            #Need to take care of initial initialisatioin, too figure out how people start out.
            #Option1: They start out randomly in the city
            #Option2: They start of in clusters as families
            #Option3: They start out in a cluster in the center, like the jama masjid meet up.


class create_mycity:
    '''
        S : Number of susceptible people to create, flag = 0
        I : Number of infected peopled to create, flag = 1
        R : Number of recovered people to create, flag = 2
    '''
    def __init__(self, S, I, R, infection_distance = 0.01, motion_constant = 0.1, recovery_time = 10, incubation = 14, death_time = 5):
        self.S = S
        self.I = I
        self.R = R
        self.population = S + I + R
        # self.n_S = S
        # self.n_I = I
        # self.n_R = R
        self.infection_distance = infection_distance
        self.motion_constant = motion_constant
        self.recovery_time = recovery_time
        self.incubation_period = incubation
        self.death_time = death_time

    def create_population(self, dim = 2):
        self.dim = dim
        self.people = []
        for i in range(S):
            self.people.append(Person(dim = self.dim, flag = 0))
        for i in range(I):
            self.people.append(Person(dim = self.dim, flag = 1))
        for i in range(R):
            self.people.append(Person(dim = self.dim, flag = 2))

############ CHECKING INTERACTING PEOPLE #############
    def check_interaction(self):
        for i in range(self.population-1):
            for j in range(i+1, self.population):
                if self.people_distance(i, j) < self.infection_distance and self.is_infected(i, j)== True:
                    print('infecting')
                    self.infect_people(i, j)

    def people_distance(self, i, j):
        person1 = self.people[i]
        person2 = self.people[j]
        return np.sum((np.array(person1.position) - np.array(person2.position))**2)**0.5

    def is_infected(self, i, j):
        person1 = self.people[i]
        person2 = self.people[j]
        if person1.flag == 1 or person2.flag == 1:
            return True
        else:
            return False

    def infect_people(self, i, j):
        if self.people[i].flag == 1 and self.people[j].flag == 1:#if both were infected, timer starts again
            self.people[i].infection_time = 0
            self.people[j].infection_time = 0
        elif self.people[i].flag == 1:
            self.people[j].flag = 1
            self.people[j].infection_time = 0
        elif self.people[j].flag == 1:
            self.people[i].flag = 1
            self.people[i].infection_time = 0

################ FIND HOW MANY PEOPLE ARE INFECTED ##############
    def find_infection(self):
        # self.n_S = 0
        # self.n_I = 0
        # self.n_R = 0
        S = I = R = 0
        for i in range(self.population):
            if self.people[i].flag == 0:
                S += 1
            elif self.people[i].flag == 1:
                I += 1
            else:
                R += 1
        return (S, I, R)

################### MAKE PEOPLE MOVE AROUND #############
    def move_around(self):
        for i in range(self.population):
            self.new_position(i)
            self.increment_infection_time(i)

    def new_position(self, i):
        for d in range(self.dim):
            person = self.people[i]
            if (person.flag == 3 and person.post_incubation == 0) or (person.flag == 2 and person.post_incubation == 0):
            # if person.flag == 3 or person.flag == 2:
                # print('done moving')
                continue
            else:
                new_position = person.position[d] + (-1)**random.randint(0,1) * random.random()*self.motion_constant
                new_position = new_position % 1
                person.position[d] = new_position

    def increment_infection_time(self, i):
        if self.people[i].flag == 1:
            self.people[i].infection_time +=1
        elif self.people[i].flag == 2 or self.people[i].flag == 3:
            if self.people[i].post_incubation > 0:
                # print(self.people[i].post_incubation)
                self.people[i].post_incubation -= 1

################### RECOVER PEOPLE #############
# adds the probability of have recovered or have died
    def remove_people(self):
        for i in range(self.population):
            if self.people[i].flag == 1 and self.people[i].infection_time > self.incubation_period:
                asym_p = .5
                asym = np.random.binomial(1, asym_p)
                if asym:
                    # print('this person is asymptomatic')
                    self.people[i].infection_time = 0
                else:
                    p = .65  # probability of recovery = recovery rate = ~79%
                    s = np.random.binomial(1, p)
                    if s == 1:
                        # recovered
                        self.people[i].flag = 2
                        if self.people[i].post_incubation == -1:
                            self.people[i].post_incubation = self.recovery_time
                    else:
                        # dead
                        self.people[i].flag = 3
                        if self.people[i].post_incubation == -1:
                            self.people[i].post_incubation = self.death_time

def initialize_animation():
    pygame.init()
    screen = pygame.display.set_mode((screen_size , screen_size))
    pygame.display.set_caption('Elastic Collision Particle Simulation')

    return screen


def create_animation(screen, people, radius, screen_size):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill([255, 255, 255])
    display(screen, people, infection_distance, screen_size)
    pygame.display.flip()


def display(screen, people, radius, screen_size):

    radius = int(radius * screen_size)
    for person in people:
        x_position = int(person.position[0] * screen_size)
        y_position = int(person.position[1] * screen_size)

        if person.flag == 0:
            color = [0,0,255]
        elif person.flag == 1:
            color = [255,0,0]
        elif person.flag == 2:
            color = [0,255,0]
            if person.post_incubation == 0:
                pygame.gfxdraw.circle(screen, x_position, y_position , radius+2, color)
                continue
        else:
            color = [50,50,50]
            if person.post_incubation == 0:
                pygame.gfxdraw.circle(screen, x_position, y_position , radius+2, color)
                continue

        pygame.gfxdraw.filled_circle(screen, x_position, y_position , radius, color)

#We create an environment of D dimensions, with range of position values between 0-1. We also take periodic boundary conditions.



'''
    dim : dimensions of the city
    N : number of people in the city
    S : number of susceptible people at time 0
    I : number of infected people at time 0
    R : number of recovered people at time 0
'''
dim = 2
S = 150 #(blue)
I = 50 #(red)
R = 0 #(green)
infection_distance = 0.005
motion_constant = 0.05
recovery_constant = 10
death_constant = 4
incubation = 10
N = S + I + R

screen_size = 600


screen = initialize_animation()

my_city = create_mycity(S, I, R, infection_distance, motion_constant, recovery_constant, incubation, death_constant)
my_city.create_population(dim)
# n_S = [S]
# n_I = [I]
# n_R = [R]

for i in range(1000):
    if i % 100 == 0:
        print('t = ', i)
    my_city.check_interaction()#Make people interact
    (S, I, R) = my_city.find_infection()#Check how many people are infected
    my_city.move_around()
    my_city.remove_people()
    # n_S.append(my_city.n_S)
    # n_I.append(my_city.n_I)
    # n_R.append(my_city.n_R)

    #animation
    create_animation(screen, my_city.people, infection_distance, screen_size)

    # if no body is infectious anymore
    # if I == 0:
    #     # print('Complete T: %i, KL: %.4f, NLLloss: %.4f, PPL (Upper Bound): %.2f' % (i, )
    #     print('No more infectious when t = ' + str(i))
    #     pygame.display.quit()
    #     pygame.quit()
    #     break
pygame.display.quit()
pygame.quit()
pygame.init()
