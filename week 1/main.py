import pygame
import numpy as np
import random

# Configuration

WIDTH = 800
HEIGHT = 800

BOWL_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
BOWL_RADIUS = 300

# Start with 1 ball, then 2. Many at once is the bonus.
NUM_PARTICLES = 3
PARTICLE_RADIUS = 12
PARTICLE_SPEED = 150.0

# Pixels per second squared, not m/s^2. Note that +y points DOWN on screen.
GRAVITY = np.array([0,900])

# How much speed survives a bounce. 1.0 loses nothing, below 1.0 is weaker.
WALL_RESTITUTION = 1
RESTITUTION = 1.0

FPS = 60

positions_set = []
velocity_set = []

for i in range(NUM_PARTICLES):

    # A random spot inside the bowl, with the whole ball fitting.
    angle = random.uniform(0, 2 * np.pi)
    distance = random.uniform(0, BOWL_RADIUS - PARTICLE_RADIUS)

    positions_set.append(BOWL_CENTER + distance * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))

    # A random direction, at roughly PARTICLE_SPEED.
    # Swap for np.array([0.0, 0.0]) to drop the ball from rest.
    angle = random.uniform(0, 2 * np.pi)

    velocity_set.append(PARTICLE_SPEED * np.array([
        np.cos(angle),
        np.sin(angle)
    ]))
    #converting the arrays to numpy arrays so I can perform mathematical operations
    positions = np.array(positions_set)
    velocities = np.array(velocity_set)
# Pygame setup

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

clock = pygame.time.Clock()

running = True

# Main loop

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Seconds since the last frame. This is your timestep.
    dt = clock.tick(FPS) / 1000.0

    ###########################################################################
    # TODO: Make every ball fall, and bounce it off the wall of the bowl.     #
    #                                                                         #
    # Two things happen here, in an order that matters.                       #
    #                                                                         #
    # First, it falls. Gravity is an acceleration, so ask yourself what it    #
    # changes directly: the position, or the velocity? And once that has      #
    # changed, what does the ball's new position depend on?                   #
    #                                                                         #
    # Second, it has to stay in the bowl. Work out how you would even         #
    # tell that it has escaped, given that you know where the centre of       #
    # the bowl is, how wide the bowl is, and how wide the ball is.            #
    # Careful: the ball is drawn with a radius of its own, so its edge        #
    # reaches the wall before its centre would.                               #
    #                                                                         #
    # Once you know it has escaped, two things need fixing. Where should      #
    # the ball actually be, and what should its velocity become? For the      #
    # velocity, only the part heading into the wall should change. The        #
    # part sliding along the wall carries on untouched. WALL_RESTITUTION      #
    # decides how much of the incoming speed comes back out.                  #
    ###########################################################################
    
    # CODE STARTS HERE.
    positions = positions + velocities*dt #updates position
    velocities = velocities+GRAVITY*dt #updates velocity
    
    for i in range(len(positions)):
        normal = positions[i]-BOWL_CENTER
        magnitude = np.linalg.norm(normal)
        unit_normal = normal/magnitude
        if(magnitude + PARTICLE_RADIUS> BOWL_RADIUS): #to prevent the ball from going into the boundary
            offset = magnitude + PARTICLE_RADIUS - BOWL_RADIUS
            positions[i] = positions[i] - unit_normal*offset #creating offset for each ball
            v_particle = velocities[i]
            n_particle = unit_normal
            #updating velocity after collision with boundary for each particle
            velocities[i] = (v_particle-2*np.dot(v_particle,n_particle)*n_particle)*WALL_RESTITUTION 
    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    ###########################################################################
    # TODO: Make the balls bounce off each other.                             #
    #                                                                         #
    # Start with the condition. Given two balls, what has to be true          #
    # about where they are for them to be touching? Every ball has the        #
    # same radius, which makes this simpler than it sounds.                   #
    #                                                                         #
    # Then the response. A collision changes velocities, not positions.       #
    # Which direction does the change act along, and how would you get        #
    # that direction from the two positions you have? Only the motion         #
    # along that direction matters, the rest is unaffected.                   #
    #                                                                         #
    # One trap worth thinking about: two balls that are overlapping but       #
    # already moving apart should be left alone. If you bounce them again     #
    # they will get stuck together. How would you tell "approaching"          #
    # from "separating"?                                                      #
    #                                                                         #
    # Finally, this has to happen for every pair of balls, not just one.      #
    ###########################################################################

    # CODE STARTS HERE.
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)): #cycling through all possible combinations of two balls
            normal_p = positions[i] - positions[j] #calculating normal(line of impact) for the two balls
            magnitude_p = np.linalg.norm(normal_p)
            unit_normal_p = normal_p/magnitude_p
            relative_velocity = velocities[i] - velocities[j] #calculating relative velocity between the two balls
            relative_speed = np.dot(relative_velocity, unit_normal_p) #calculating relative speed along the line of impact of the two balls
            approaching = np.dot(relative_velocity, unit_normal_p) < 0 #checks whether the balls approaching or separating
            if (magnitude_p < 2 * PARTICLE_RADIUS and approaching): #check for collision
                v_i = velocities[i]
                v_j = velocities[j]
                #breaking the velocity into normal and tangential components
                v_i_normal = np.dot(v_i, unit_normal_p) * unit_normal_p
                v_j_normal = np.dot(v_j, unit_normal_p) * unit_normal_p

                v_i_tangent = v_i - v_i_normal
                v_j_tangent = v_j - v_j_normal

                #using formula for change in normal velocity after collision
                v_i_normal -= ((1+RESTITUTION)*relative_speed/2)*unit_normal_p
                v_j_normal += ((1+RESTITUTION)*relative_speed/2)* unit_normal_p
                #adding up the new velocities and hence updating it``
                velocities[i] = v_i_tangent+v_i_normal
                velocities[j] = v_j_tangent + v_j_normal
                
    pass

    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

    # Render

    screen.fill((20, 20, 25))

    pygame.draw.circle(
        screen,
        (180, 180, 180),
        BOWL_CENTER.astype(int),
        BOWL_RADIUS,
        width=3
    )

    for position in positions:
        pygame.draw.circle(
            screen,
            (220, 220, 220),
            (int(position[0]), int(position[1])),
            PARTICLE_RADIUS
        )

    pygame.display.flip()

pygame.quit()
