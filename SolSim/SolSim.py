import pygame as pg
import numpy as np
import time

pg.init()

# Constants
DISPLAY_WITH = 1080
DISPLAY_HEIGHT = 720
KM_PER_PIXLE = 1e9
OFFSETX = 0
OFFSETY = 0

#Images
menu_background = pg.image.load('menu_background.png')
wasd = pg.image.load('wasd.png')
deathstar = pg.image.load('deathstar.png')
destruction_cursor = pg.image.load('target.png')
planet_wrench = pg.image.load('planet_wrench.png')

# FPS
FPS = 61
fpsClock = pg.time.Clock()

# Create Window
screen = pg.display.set_mode((DISPLAY_WITH, DISPLAY_HEIGHT))
pg.display.set_caption("SolSim 2D")
icon = pg.image.load('solar_icon.png')
pg.display.set_icon(icon)

# Planet Class
class Planet:
    # Technical
    def _coordinates_to_screen(self, coordinates):
        screen = [int((coordinates[0] /KM_PER_PIXLE) + (DISPLAY_WITH/2) + OFFSETX),
                  int((coordinates[1] /KM_PER_PIXLE) + (DISPLAY_HEIGHT/2) + OFFSETY)]
        return screen

    def __init__(self, image, name, position, velocity, mass, size_px):
        self.image = pg.image.load(image)
        self.name = name
        # distance from sun in meter
        self.position = np.array(position, dtype='float64')
        self.mass = mass  # kilogramms
        self.velocity = np.array(velocity, dtype='float64')  # m/s
        self.size_px = size_px
        self.past_positions = []
        self.past_positions_coordinates = []

    # Positions the planet on the map
    def draw(self):
        screenpos = self._coordinates_to_screen(self.position)
        screenpos[0] -= int(self.size_px/2)
        screenpos[1] -= int(self.size_px/2)
        screen.blit(self.image, screenpos)

    # Show planet names on the map
    def show_names(self):
        font = pg.font.Font('freesansbold.ttf', 8)
        x = self.position[0] / KM_PER_PIXLE
        y = self.position[1] / KM_PER_PIXLE
        score = font.render(self.name, True, (255, 255, 255))
        screen.blit(score, ((x + (self.size_px/2) + 2 + (DISPLAY_WITH/2) + OFFSETX),
                            (y + (self.size_px/2) + 2 + (DISPLAY_HEIGHT/2)+ OFFSETY)))

    def calculate_orbit(self):
        if len(self.past_positions) > 1:
            last_position = self.past_positions[-1]
            if np.linalg.norm(last_position - self.position) > 5 * KM_PER_PIXLE:
                self.past_positions.append(self.position.copy())
                x = self.position.copy()
                x = self._coordinates_to_screen(x)
                self.past_positions_coordinates.append(x)
        else:
            self.past_positions.append(self.position.copy())

    def show_orbit(self):
        if len(self.past_positions_coordinates) > 1:
            pg.draw.lines(screen, (176, 176, 176), False, self.past_positions_coordinates)

    def recalculate_orbit(self):
        self.past_positions_coordinates = [self._coordinates_to_screen(p) for p in self.past_positions]


# Planet Data
sun = Planet('sun.png', 'Sun', (0, 0), (0, 0), 1.989e30, 49)
mercury = Planet('mercury.png', 'Mercury', (5.8e10, 0), (0, 47000), 3.301e23, 7)
venus = Planet('venus.png', 'Venus', (1.082e11, 0), (0, 35020), 4.867e24, 7)
earth = Planet('earth.png', 'Earth', (1.49e11, 0), (0, 29780), 5.97e24, 7)
mars = Planet('mars.png', 'Mars', (2.28e11, 0), (0, 24000), 6.4e23, 7)
jupiter = Planet('jupiter.png', 'Jupiter', (7.78e11, 0), (0, 13070), 1.8e27, 11)
saturn = Planet('saturn.png', 'Saturn', (1.4e12, 0), (0, 9680), 5.6e26, 11)
uranus = Planet('uranus.png', 'Uranus', (2.9e12, 0), (0, 6800), 8.7e25, 11)
neptun = Planet('neptun.png', 'Neptun', (4.5e12, 0), (0, 5430), 1.024e26, 11)

planet_list = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptun]

# Mechanics
def distance(objecta, objectb):
    dist = np.linalg.norm(objecta.position - objectb.position)
    return dist

def gravitational_force(objecta, objectb, dt):
    d = distance(objecta, objectb)
    F_mag = (6.673e-11 * objecta.mass * objectb.mass)/(d**2)
    s = objectb.position - objecta.position
    F = F_mag * (s / d)
    a = F / objecta.mass
    objecta.velocity += dt * a

def move(objecta, dt):
    objecta.position += dt * objecta.velocity


def collission(objecta, objectb):
    if distance(objecta, objectb) <  KM_PER_PIXLE:
        if objecta.mass > objectb.mass:
            objecta.mass += objectb.mass
            planets_to_remove.append(objectb)
        else:
            objectb.mass += objecta.mass
            planets_to_remove.append(objecta)

def remove_planet():
    for planet in planet_list:
        for planetb in planets_to_remove:
            if planet == planetb:
                planet_list.remove(planet)
                planets_to_remove.remove(planetb)
                message = f'{planet.name} got Destroyed'
                new_message = True

def calculate_passed_time(dt):
    global passed_time, years, days
    passed_time += time_step
    years = int((((passed_time/60)/60)/24)//365)
    days = int((((passed_time/60)/60)//24) - (365 * years))

# Options to create your own planet
creation_curser = [0, 255, 255, 255, 255, 255]

possible_distancesa = [0.5 * x for x in range(19)]
index_possible_distancesa = 3
own_distancea = possible_distancesa[index_possible_distancesa]
possible_distancesb = [0, 10, 11, 12, 13]
index_possible_distancesb = 2
own_distanceb = possible_distancesb[index_possible_distancesb]
own_distance = float(str(possible_distancesa[index_possible_distancesa]) +'e'+ str(possible_distancesb[index_possible_distancesb]))
possible_massa = [0.5 * x for x in range(19)]
index_possible_massa = 3
own_massa = possible_massa[index_possible_massa]
possible_massb = [x for x in range(32)]
index_possible_massb = 24
own_massb = possible_massb[index_possible_massb]
own_mass = float(str(possible_massa[index_possible_massa]) +'e'+ str(possible_massb[index_possible_distancesb]))
possible_speed = [1000 * x for x in range(30)]
index_possible_speed = 5
own_speed = possible_speed[index_possible_speed]

def change_value():
    global index_possible_distancesa, index_possible_distancesb, index_possible_massa, index_possible_massb, index_possible_speed, own_distancea, own_distanceb, own_distance, own_massa, own_massb, own_mass, own_speed
    x = creation_curser.index(0)
    if x == 0:
        index_possible_distancesa += 1
        index_possible_distancesa %= len(possible_distancesa)
    elif x == 1:
        index_possible_distancesb += 1
        index_possible_distancesb %= len(possible_distancesb)
    elif x == 2:
        index_possible_massa += 1
        index_possible_massa %= len(possible_massa)
    elif x == 3:
        index_possible_massb += 1
        index_possible_massb %= len(possible_massb)
    elif x == 4:
        index_possible_speed += 1
        index_possible_speed %= len(possible_speed)

    own_distancea = possible_distancesa[index_possible_distancesa]
    own_distanceb = possible_distancesb[index_possible_distancesb]
    own_distance = float(str(possible_distancesa[index_possible_distancesa]) +'e'+ str(possible_distancesb[index_possible_distancesb]))
    own_massa = possible_massa[index_possible_massa]
    own_massb = possible_massb[index_possible_massb]
    own_mass = float(str(possible_massa[index_possible_massa]) +'e'+ str(possible_massb[index_possible_massb]))
    own_speed = possible_speed[index_possible_speed]


def move_creation_curser():
    x = creation_curser.index(0)
    creation_curser[x] = 255
    y = x + 1
    y %= len(creation_curser)
    creation_curser[y] = 0


def create_own_planet():
    global new_planets_counter
    new_planets_counter += 1
    new_variable = 'own_planet' + str(new_planets_counter)
    vars()[new_variable] = Planet('earth.png', ('Own Planet' + str(new_planets_counter)), (own_distance, 0), (0, own_speed), own_mass, 7)
    planet_list.append(vars()[new_variable])

# Presentation
def show_FPS(FPS):
    font = pg.font.Font('freesansbold.ttf', 15)
    FPS_str = f'FPS {str(FPS)[11:13]}'
    score = font.render(FPS_str, True, (255, 255, 255))
    screen.blit(score, (((DISPLAY_WITH * 0.95),
                         (DISPLAY_HEIGHT - (DISPLAY_HEIGHT * 0.999)))))

def show_menu():
    screen.blit(menu_background, (10, 10))
    titlefont = pg.font.Font('freesansbold.ttf', 30)
    font = pg.font.Font('freesansbold.ttf', 15)
    title = titlefont.render('Controls', True, (255, 255, 255))
    screen.blit(title, (25, 30))
    screen.blit(wasd, (30, 100))
    scorea = font.render('Move Camera', True, (255, 255, 255))
    screen.blit(scorea, (30, 80))
    scoreb = font.render('Pause Simulation [P]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 200))
    scoreb = font.render('Increase Speed [: .]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 225))
    scoreb = font.render('Reduce Speed [; ,]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 250))
    scoreb = font.render('Hide Planet Info [F1]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 275))
    scoreb = font.render('Hide Controls [C]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 300))
    scoreb = font.render('Create Planet [Q]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 350))
    scoreb = font.render('Destroy Planet [E]', True, (255, 255, 255))
    screen.blit(scoreb, (30, 375))

def show_destruction_menu():
    global target_curser_position
    pixel_counter = 0
    screen.blit(menu_background, (10, 10))
    titlefont = pg.font.Font('freesansbold.ttf', 16)
    font = pg.font.Font('freesansbold.ttf', 13)
    title = titlefont.render('Choose a Planet to Annihilate', True, (255, 255, 255))
    screen.blit(title, (25, 30))
    title = font.render('[E] Back to Menu   [X] Annihilate', True, (255, 255, 255))
    screen.blit(title, (25, 60))
    screen.blit(deathstar, (30, 60))

    planet_list_18 = planet_list[:17]
    if len(planet_list) < 19:
        for planet in planet_list:
            score = font.render(planet.name, True, (255, 255, 255))
            screen.blit(score, (30, (250 + pixel_counter)))
            pixel_counter += 25
    else:
        for planet in planet_list_18:
            score = font.render(planet.name, True, (255, 255, 255))
            screen.blit(score, (30, (250 + pixel_counter)))
            pixel_counter += 25

    ''' Prevents simulation from crashing if the planet list becomes empty'''
    if target_curser_position >= (len(planet_list)-1):
        if len(planet_list) != 0:
            target_curser_position = (len(planet_list)-1)
        else:
            target_curser_position = 0
    ''' Draws cursor'''
    if len(planet_list) != 0:
        screen.blit(destruction_cursor, (200, 240 + (target_curser_position*25)))


def show_creation_menu_a():
    pixel_counter = 0
    screen.blit(menu_background, (10, 10))
    titlefont = pg.font.Font('freesansbold.ttf', 20)
    font = pg.font.Font('freesansbold.ttf', 13)
    title = titlefont.render('Choose an Option', True, (255, 255, 255))
    screen.blit(title, (25, 30))
    title = font.render('[Q] Back to Menu   [X] Create Planet', True, (255, 255, 255))
    screen.blit(title, (25, 60))
    screen.blit(planet_wrench, (30, 100))
    title = font.render('Distance from Centre', True, (255, 255, 255))
    screen.blit(title, (25, 270))
    distancea = font.render(str(own_distancea), True, (255, creation_curser[0], 200))
    screen.blit(distancea, (25, 285))
    e = font.render('e', True, (255, 255, 200))
    screen.blit(e, (45, 285))
    distanceb = font.render(str(own_distanceb), True, (255, creation_curser[1], 200))
    screen.blit(distanceb, (53, 285))
    title = font.render('Planet Mass', True, (255, 255, 255))
    screen.blit(title, (25, 300))
    massa = font.render(str(own_massa), True, (255, creation_curser[2], 200))
    screen.blit(massa, (25, 315))
    e = font.render('e', True, (255, 255, 200))
    screen.blit(e, (45, 315))
    massb = font.render(str(own_massb), True, (255, creation_curser[3], 200))
    screen.blit(massb, (53, 315))
    title = font.render('Speed', True, (255, 255, 255))
    screen.blit(title, (25, 330))
    speed = font.render(str(own_speed), True, (255, creation_curser[4], 200))
    screen.blit(speed, (25, 345))
    title = font.render('[S] Select Value to Change', True, (255, 255, 255))
    screen.blit(title, (25, 375))
    title = font.render('[D] Change Value', True, (255, 255, 255))
    screen.blit(title, (25, 390))


def show_time():
    if paused:
        status = 'Paused'
    else:
        status = f'x{int(time_step)}'
    font = pg.font.Font('freesansbold.ttf', 16)
    score = font.render(f'[{status}]    T+ {years} years {days} days', True, (255, 255, 255))
    screen.blit(score, ((DISPLAY_WITH - 300), DISPLAY_HEIGHT - 100))



# Start variables
time_step = 10000
passed_time = 0
years = 0
days = 0
running = True
simulating = True
paused = False
recalculating = False
show_information = True
show_controls = True
destruction_menu = False
creation_menu_a = False
new_planets_counter = 0
new_message = False
message = ''
target_curser_position = 0
offset_left_right = 0
offset_up_down = 0
planets_to_remove =[]

# Game Loop
while running:
    for event in pg.event.get():
        ''' Closes the Window if you press the quit button'''
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1 and show_information == True:
                show_information = False
            elif event.key == pg.K_F1 and show_information == False:
                show_information = True
            elif event.key == pg.K_p and paused == True:
                paused = False
                simulating = True
            elif event.key == pg.K_p and paused == False:
                paused = True
                simulating = False
            elif event.key == pg.K_w and destruction_menu == False and creation_menu_a == False:
                OFFSETY += (DISPLAY_WITH/20)
                recalculating = True
            elif event.key == pg.K_s and destruction_menu == False and creation_menu_a == False:
                OFFSETY -= (DISPLAY_WITH/20)
                recalculating = True
            elif event.key == pg.K_d and destruction_menu == False and creation_menu_a == False:
                OFFSETX -= (DISPLAY_HEIGHT/20)
                recalculating = True
            elif event.key == pg.K_a and destruction_menu == False and creation_menu_a == False:
                OFFSETX += (DISPLAY_HEIGHT/20)
                recalculating = True
            elif event.key == pg.K_c and show_controls == True and creation_menu_a == False:
                show_controls = False
            elif event.key == pg.K_c and show_controls == False and creation_menu_a == False:
                show_controls = True
            elif event.key == pg.K_e and show_controls == True and creation_menu_a == False:
                show_controls = False
                destruction_menu = True
                creation_menu_a = False
            elif event.key == pg.K_e and show_controls == False:
                show_controls = True
                destruction_menu = False
                creation_menu_a = False
            elif event.key == pg.K_q and show_controls == True:
                show_controls = False
                destruction_menu = False
                creation_menu_a = True
            elif event.key == pg.K_q and show_controls == False:
                show_controls = True
                destruction_menu = False
                creation_menu_a = False
            elif event.key == pg.K_w and destruction_menu == True:
                if target_curser_position > 0:
                    target_curser_position -= 1
            elif event.key == pg.K_s and destruction_menu == True:
                if target_curser_position < len(planet_list)-1:
                    target_curser_position += 1
            elif event.key == pg.K_x and destruction_menu == True and len(planet_list) > 0:
                planets_to_remove.append(planet_list[target_curser_position])
            elif event.key == pg.K_PERIOD and time_step < 100000:
                paused = False
                simulating = True
                time_step *= 2
            elif event.key == pg.K_COMMA and time_step > 5000:
                time_step *= 0.5
            elif event.key == pg.K_COMMA and time_step == 5000:
                time_step *= 0.5
                paused = True
                simulating = False
            elif event.key == pg.K_w and creation_menu_a == True:
                pass
            elif event.key == pg.K_s and creation_menu_a == True:
                move_creation_curser()
            elif event.key == pg.K_a and creation_menu_a == True:
                pass
            elif event.key == pg.K_d and creation_menu_a == True:
                change_value()
            elif event.key == pg.K_x and creation_menu_a == True:
                create_own_planet()


    ''' Defines Background-Color'''
    screen.fill((0, 0, 2))

    ''' Draws dynamic objects into the correct position'''
    for i in range(len(planet_list)):
        planet_list[i].draw()
    if show_information:
        show_time()
        for i in range(len(planet_list)):
            planet_list[i].show_names()
            planet_list[i].show_orbit()

    if show_controls:
        show_menu()

    if destruction_menu:
        show_destruction_menu()

    if creation_menu_a:
        show_creation_menu_a()


    '''Simulate body motion'''
    if simulating:
        for i in range(len(planet_list)):
            for j in range(len(planet_list)):
                if i != j:
                    planet_list[i].calculate_orbit()
                    gravitational_force(planet_list[i], planet_list[j], time_step)

        for i in range(len(planet_list)):
            for j in range(len(planet_list)):
                if i != j:
                    collission(planet_list[i], planet_list[j])

        for i in range(len(planet_list)):
            move(planet_list[i], time_step)

        calculate_passed_time(time_step)

    if recalculating:
        for i in range(len(planet_list)):
            planet_list[i].recalculate_orbit()
        recalculating = False


    show_FPS(fpsClock)

    pg.display.update()
    fpsClock.tick(FPS)
    remove_planet()
