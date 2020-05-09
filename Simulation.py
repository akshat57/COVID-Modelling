
# coding: utf-8

# In[18]:


import random
import numpy as np
import matplotlib.pyplot as plt
import pygame
import pygame.gfxdraw


# In[19]:


#Particle class. Takes in paramters, the number of dimension (D)
#The particle will have D parameters for position, and D parameters for velocity
#Initialize all the particles. Also decide their environment.


# In[20]:


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
            


# In[21]:


class create_mycity:
    '''
        S : Number of susceptible people to create, flag = 0
        I : Number of infected peopled to create, flag = 1
        R : Number of recovered people to create, flag = 2
    '''
    def __init__(self, S, I, R, infection_distance = 0.01, motion_constant = 0.1, recovery_time = 5):
        self.S = S
        self.I = I
        self.R = R
        self.population = S + I + R
        self.n_S = S
        self.n_I = I
        self.n_R = R
        
        self.infection_distance = infection_distance
        self.motion_constant = motion_constant
        self.recovery_time = recovery_time
        
        
    
    
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
        self.n_S = 0
        self.n_I = 0
        self.n_R = 0
    
        for i in range(self.population):
            if self.people[i].flag == 0:
                self.n_S += 1
            elif self.people[i].flag == 1:
                self.n_I += 1
            else:
                self.n_R += 1
        

################### MAKE PEOPLE MOVE AROUND #############
    def move_around(self):
        for i in range(self.population):
            self.new_position(i)
            self.increment_infection_time(i)
        
        
    def new_position(self, i):
        
        for d in range(self.dim):
            new_position = self.people[i].position[d] + (-1)**random.randint(0,1) * random.random()*self.motion_constant
            new_position = new_position % 1
            self.people[i].position[d] = new_position
        
    def increment_infection_time(self, i):
        if self.people[i].flag == 1:
            self.people[i].infection_time +=1
        
        
################### RECOVER PEOPLE #############
    def recover_people(self):
        for i in range(self.population):
            if self.people[i].flag == 1 and self.people[i].infection_time > self.recovery_time:
                self.people[i].flag = 2




# In[22]:


def initialize_animation():
    pygame.init()
    screen = pygame.display.set_mode((screen_size , screen_size))
    pygame.display.set_caption('Elastic Collision Particle Simulation')
    
    return screen


# In[23]:


def create_animation(screen, people, radius, screen_size):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill([255, 255, 255])
    display(screen, people, infection_distance, screen_size)
    pygame.display.flip()
    
    


# In[24]:


def display(screen, people, radius, screen_size):
    
    radius = int(radius * screen_size)
    for person in people:
        if person.flag == 0:
            color = [0,0,255]
        elif person.flag == 1:
            color = [255,0,0]
        else:
            color = [0,255,0]
            
            
        x_position = int(person.position[0] * screen_size)
        y_position = int(person.position[1] * screen_size)
        
        pygame.gfxdraw.filled_circle(screen, x_position, y_position , radius, color)


# In[25]:


#We create an environment of D dimensions, with range of position values between 0-1. We also take periodic boundary conditions.


# In[26]:


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
recovery_constant = 50

N = S + I + R

screen_size = 600


# In[27]:


screen = initialize_animation()

my_city = create_mycity(S, I, R, infection_distance, motion_constant, recovery_constant)
my_city.create_population(dim)
n_S = [S]
n_I = [I]
n_R = [R]

for i in range(1000):
    if i % 100 == 0:
        print('t = ', i)
    my_city.check_interaction()#Make people interact
    my_city.find_infection()#Check how many people are infected
    my_city.move_around()
    my_city.recover_people()
    n_S.append(my_city.n_S)
    n_I.append(my_city.n_I)
    n_R.append(my_city.n_R)
    
    #animation
    create_animation(screen, my_city.people, infection_distance, screen_size)
    
pygame.display.quit()
pygame.quit()

    


# In[1]:


#plt.plot(n_S)
#plt.plot(n_I)
#plt.plot(n_R)
#plt.legend(['susceptible', 'infected', 'removed'])


# In[223]:


pygame.init()

