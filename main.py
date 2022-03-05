import pygame
import math
import random


pygame.init()
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

pos = []

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day

    def __init__(self, x, y, radius, color, mass, moon_num):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.moon_num = moon_num

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.theta = 0
        self.phi = 0

    def draw(self, screen):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(screen, self.color, False, updated_points, 2)

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)

            # make a card for distance
            #pygame.draw.rect(screen, WHITE, 1, width=0)

            # screen.blit(distance_text, (x - distance_text.get_width() /
            # 2, y - distance_text.get_height()/2))
    def draw_moon(self, screen):
        # earth or mars?
        if self.moon_num == 1:  # earth
            # get center, and radius of the orbit
            x_center = self.x * self.SCALE + WIDTH / 2
            y_center = self.y * self.SCALE + HEIGHT / 2
            r = 0.15 * Planet.AU * self.SCALE

            # create the orbit
            x = r * math.cos(self.theta) + x_center
            y = r * math.sin(self.theta) + y_center
            self.theta -= math.pi/40

            pygame.draw.circle(screen, WHITE, (x, y), 4)
        elif self.moon_num == 2:  # mars
            # get center, and radius of the orbit
            x_center = self.x * self.SCALE + WIDTH / 2
            y_center = self.y * self.SCALE + HEIGHT / 2
            r1 = 0.15 * Planet.AU * self.SCALE  # deimos
            r2 = 0.10 * Planet.AU * self.SCALE

            # create the orbit of phobos
            x2 = r2 * math.cos(self.phi) + x_center
            y2 = r2 * math.sin(self.phi) + y_center
            self.phi -= math.pi/30

            # create the orbit of deimos
            x1 = r1 * math.cos(self.theta) + x_center
            y1 = r1 * math.sin(self.theta) + y_center
            self.theta -= math.pi/50

            pygame.draw.circle(screen, BLUE, (x1, y1), 2)
            pygame.draw.circle(screen, RED, (x2, y2), 3)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# asteroids belt
def asteroids(screen, num):
    global pos
    r_min = 1.8 * Planet.AU * Planet.SCALE
    r_max = 2.5 * Planet.AU * Planet.SCALE
    theta = 0
    if len(pos) == 0:
        for asteroid in range(num):
            r = random.uniform(r_min, r_max)
            theta += math.pi/100
            x = r * math.cos(theta) + WIDTH/2
            y = r * math.sin(theta) + HEIGHT/2
            pos.append((x, y))
            
            
    # move it from here 🤔     
    for x, y in pos:
        pygame.draw.circle(screen, WHITE, (x, y), 1)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 0)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 1)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 2)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 0)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, 0)
    venus.y_vel = 35.02 * 1000

    planets = [sun, earth, mars, mercury,
               venus]

    
    while run:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(screen)
            planet.draw_moon(screen)

        asteroids(screen, 400)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
