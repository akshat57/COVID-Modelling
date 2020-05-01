import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from covid import *


'''
    dim : dimensions of the city
    N : number of people in the city
    S : number of susceptible people at time 0
    I : number of infected people at time 0
    R : number of recovered people at time 0
'''
dim = 2
S = 140 #(blue)
I = 50 #(red)
R = 0 #(green)
infection_distance = 0.005
motion_constant = 0.05

recovery_constant = 10
death_constant = 5
incubation = 20

N = S + I + R


my_city = create_mycity(S, I, R, infection_distance, motion_constant, recovery_constant, incubation, death_constant)
my_city.create_population(dim)
n_S = [S]
n_I = [I]
n_R = [R]

color =['b', 'r', 'g']
x_positions = [person.position[0] for person in my_city.people ]
y_positions = [person.position[1] for person in my_city.people ]
colors = [color[person.flag] for person in my_city.people]

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

scat = ax.scatter(x_positions, y_positions,
                  lw=0.5, c= colors,facecolors='none')


def update(frame_number):
    if frame_number % 10 == 0:
        print('t = ', frame_number)
    my_city.check_interaction()#Make people interact
    my_city.find_infection()#Check how many people are infected
    my_city.move_around()
    my_city.remove_people()
    n_S.append(my_city.n_S)
    n_I.append(my_city.n_I)
    n_R.append(my_city.n_R)

    # Update the scatter collection, with the new colors, sizes and positions.
    color =['b', 'r', 'g', 'k']

    scat.set_color([color[person.flag] for person in my_city.people])
    scat.set_offsets([person.position for person in my_city.people])



animation = FuncAnimation(fig, update, frames=500, repeat=False, interval=500)
plt.show()

fig2 = plt.figure(figsize=(7, 7))
plt.plot(n_S, 'b')
plt.plot(n_I, 'r')
plt.plot(n_R, 'g')
# p
plt.show()
