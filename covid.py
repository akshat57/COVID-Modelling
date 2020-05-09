import random
import numpy as np

class Person:
    '''
        dim = Defines dimensions of our city.
        flag = determines wether our person is susceptible(0), infected(1) or removed(2)
    '''
    '''
        We're assuming the limits of our city to be from 0 to 1. Also, we assume symmetry across different dimensions
    '''
    def __init__(self, dim = 2, flag = 0, position = (-1,-1), speed=0.05):
        self.dim = dim
        self.flag = flag
        self.infection_time = 0
        
        
        if position[0] < 0:
            self.initialize_position()

        self.speed = speed
        self.initialize_velocity()
        self.random_walk_p = 0.2
        
    def initialize_position(self):
        self.position = []
        for i in range(self.dim):
            self.position.append(random.random())#can have different methods of initialization. 
            #Need to take care of initial initialisatioin, too figure out how people start out.
            #Option1: They start out randomly in the city
            #Option2: They start of in clusters as families
            #Option3: They start out in a cluster in the center, like the jama masjid meet up.
            
    def initialize_velocity(self):
        self.velocity = []
        for i in range(self.dim):
            self.velocity.append(self.speed*random.random())

    def update_position(self):
        if random.random() > self.random_walk_p: 
            self.initialize_velocity()
        for i in range(self.dim):
            self.position[i] = (self.position[i]+self.velocity[i])%1

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
        
        for i in range(self.S):
            self.people.append(Person(dim = self.dim, flag = 0, speed=self.motion_constant))
        
        for i in range(self.I):
            self.people.append(Person(dim = self.dim, flag = 1, speed=self.motion_constant))
        
        for i in range(self.R):
            self.people.append(Person(dim = self.dim, flag = 2, speed=self.motion_constant))
        

        
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
        if self.people[i].flag == 1 and self.people[j].flag == 1:
            #if both were infected, timer starts again
            self.people[i].infection_time = 0
            self.people[j].infection_time = 0
            
        elif self.people[i].flag == 1:
            if self.people[j].flag == 2:
                return
            self.people[j].flag = 1
            self.people[j].infection_time = 0
            
        elif self.people[j].flag == 1:
            if self.people[i].flag == 2:
                return
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
            self.people[i].update_position()
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


