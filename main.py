import pygame
import thorpy
from specimen import Specimen
from time import sleep
import matplotlib.pyplot as plt

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

#simulation parameters
population=[]
population_size=1000
simulation_length=100
simulate_flag=True

#custom pygame event responsible for starting simulation
run_sim_event = pygame.event.Event(pygame.USEREVENT+1)

#initialize simulation
def run_sim():
    print("Running simulation")
    pygame.event.post(run_sim_event)

#set simulation parameters
def set_params():
    population_size=slider_size.get_value()
    simulation_length=slider_length.get_value()

#create simulated population
def create_pop():
    for i in range(population_size):
        temp=Specimen()
        temp.setCoordinates(screen_x=700,screen_y=700)
        temp.setSpeed()
        population.append(temp)
        del(temp)

pygame.init()
pygame.display.set_caption("Disease sim")
screen = pygame.display.set_mode([700, 700])
screen.fill(WHITE)

#menu
#sliders
slider_size = thorpy.SliderX(500, (1000, 1500), "Initial population(default 1000)")
slider_length = thorpy.SliderX(400, (100,500), "Simulation length(default 100)")
#buttons
run_sim_button = thorpy.make_button("Run simulation",func=run_sim)
set_params_button = thorpy.make_button("Set parameters values",func=set_params)
quit_button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
#main menu
box=thorpy.Box(elements=[slider_size,
                         slider_length,
                         set_params_button,
                         run_sim_button,
                         quit_button])
menu=thorpy.Menu(box)
box.set_topleft((0,0))
box.blit()
box.update()
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT+1:
            #create population according to set parameters
            create_pop()
            screen.fill(WHITE)
            for i in range(simulation_length):
                screen.fill(WHITE)
                #draw population
                for p in population:
                    if p.state=='C':
                        #sick specimen as red pixel
                        pygame.draw.circle(screen,RED,(p.x,p.y),1)
                    elif p.state=='Z':
                        #infected specimen as yellow pixel
                        pygame.draw.circle(screen,YELLOW,(p.x,p.y),1)
                    elif p.state=='ZD':
                        #recowering specimen as orange pixel
                        pygame.draw.circle(screen,ORANGE,(p.x,p.y),1)
                    elif p.state=='ZZ':
                        #healthy specimen as green pixel
                        pygame.draw.circle(screen,GREEN,(p.x,p.y),1)
                pygame.display.update()
                #for next turn
                for p in population:
                    #check if move will result in hitting wall
                    p.checkWall(700,700)
                    #move specimen
                    p.move()
                    #check if move resulted in any interactions
                    children=p.checkContact(population)
                    #add potential children to population
                    if len(children)>0:
                        for c in children:
                            population.append(c)
                    #increment age of specimen and ammend parameters as required
                    p.getOlder()
                for p in population:
                    #remove dead specimen from population
                    if p.alive==False:
                        population.remove(p)
                    #clean history of interactions
                    p.clean()
                #wait for 0.25s to make each turn visible
                sleep(0.25)
            simulate_flag=False
        else:
            #print menu
            screen.fill(WHITE)
            box.blit()
            box.update()
            menu.react(event)
            pygame.display.update()

pygame.quit()