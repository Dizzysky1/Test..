import sys
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 3D snake game that plays itself

grid_size = 10
cube_size = 1

# directions (dx, dy, dz)
DIRECTIONS = {
    'UP': (0, 1, 0),
    'DOWN': (0, -1, 0),
    'LEFT': (-1, 0, 0),
    'RIGHT': (1, 0, 0),
    'FORWARD': (0, 0, -1),
    'BACKWARD': (0, 0, 1)
}

# BFS autoplayer
from collections import deque

def bfs_path(start, goal, snake_set):
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        pos, path = queue.popleft()
        if pos == goal:
            return path
        for d in DIRECTIONS.values():
            nxt = (pos[0] + d[0], pos[1] + d[1], pos[2] + d[2])
            if not (0 <= nxt[0] < grid_size and 0 <= nxt[1] < grid_size and 0 <= nxt[2] < grid_size):
                continue
            if nxt in visited or nxt in snake_set:
                continue
            visited.add(nxt)
            queue.append((nxt, path + [d]))
    return []


def place_food(snake):
    free_spaces = [(x, y, z) for x in range(grid_size) for y in range(grid_size) for z in range(grid_size)
                   if (x, y, z) not in snake]
    return random.choice(free_spaces) if free_spaces else None


def draw_cube(x, y, z, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    # Each face of the cube
    vertices = [
        (x, y, z),
        (x + cube_size, y, z),
        (x + cube_size, y + cube_size, z),
        (x, y + cube_size, z),
        (x, y, z + cube_size),
        (x + cube_size, y, z + cube_size),
        (x + cube_size, y + cube_size, z + cube_size),
        (x, y + cube_size, z + cube_size),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (1, 2, 6, 5),
        (0, 3, 7, 4),
    ]
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-grid_size/2, -grid_size/2, -30)
    glEnable(GL_DEPTH_TEST)

    snake = [(grid_size//2, grid_size//2, grid_size//2)]
    snake_set = set(snake)
    direction = DIRECTIONS['RIGHT']
    food = place_food(snake)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # autoplayer decides direction
        path = bfs_path(snake[0], food, snake_set)
        if path:
            direction = path[0]
        else:
            # no path to food, move randomly without collision
            for d in DIRECTIONS.values():
                nxt = (snake[0][0]+d[0], snake[0][1]+d[1], snake[0][2]+d[2])
                if (0 <= nxt[0] < grid_size and 0 <= nxt[1] < grid_size and 0 <= nxt[2] < grid_size and nxt not in snake_set):
                    direction = d
                    break

        new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1], snake[0][2]+direction[2])

        if not (0 <= new_head[0] < grid_size and 0 <= new_head[1] < grid_size and 0 <= new_head[2] < grid_size):
            print('Game Over: hit wall')
            pygame.quit()
            return
        if new_head in snake_set:
            print('Game Over: hit self')
            pygame.quit()
            return
        snake.insert(0, new_head)
        snake_set.add(new_head)
        if new_head == food:
            food = place_food(snake)
        else:
            tail = snake.pop()
            snake_set.remove(tail)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for segment in snake:
            draw_cube(*segment, color=(0,1,0))
        if food:
            draw_cube(*food, color=(1,0,0))
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
