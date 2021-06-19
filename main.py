import pygame
import thorpy
from specimen import Specimen

WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED = (255,   0,   0)
YELLOW = (255,255,0)
ORANGE = (255,140,0)

#simulation parameters
population=[]
population_size=100
simulation_length=100

#custom pygame event responsible for starting simulation
run_sim_event = pygame.event.Event(pygame.USEREVENT+1)

#initialize simulation
def run_sim():
    print("Running simulation")
    pygame.event.post(run_sim_event)

def set_params():
    population_size=slider_size.get_value()
    simulation_length=slider_length.get_value()

pygame.init()
pygame.display.set_caption("Disease sim")
screen = pygame.display.set_mode([700, 700])
screen.fill(WHITE)

#menu
#sliders
slider_size = thorpy.SliderX(400, (100, 500), "Initial population")
slider_length = thorpy.SliderX(400, (100,500), "Simulation length")
#buttons
run_sim_button = thorpy.make_button("Run simulation",func=run_sim)
set_params_button = thorpy.make_button("Set parameters values",func=set_params)
quit_button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
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
            pass
        else:
            screen.fill(WHITE)
            box.blit()
            box.update()
            pygame.display.update()
        menu.react(event)
        pygame.display.update()