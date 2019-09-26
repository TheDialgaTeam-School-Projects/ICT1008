import time

import pygame

from Environment import Environment
from algorithm import *

selectButton = ""
selectMode = "Dijkstra"
start = False
restart = False
bot_coord, del_coord, trash_coord, algorithm = None, None, None, None
trashPos = []
startTime = 0


def event_handler(run_state):
    global selectButton, start, selectMode, algorithm, restart
    global bot_coord, del_coord, trash_coord, trashPos, startTime

    for event in pygame.event.get():
        if start is False:
            mouse_pos = pygame.mouse.get_pos()

            # remove bot if duplicate exist
            if bot_coord == del_coord or bot_coord == trash_coord:
                bot_coord = None

            # remove trash if duplicate exist
            for x in trashPos:
                if x == del_coord or x == bot_coord:
                    trashPos.remove(x)

            # left mouse Button
            if pygame.mouse.get_pressed()[0] == 1:
                if selectButton == "Obstacle":
                    del_coord = environment.updateBlock(mouse_pos, "block")

                elif selectButton == "Delete":
                    del_coord = environment.updateBlock(mouse_pos, "tile")

                elif selectButton == "Trash":
                    # limit the trash to 2
                    if len(trashPos) < 2:
                        trash_coord = environment.updateBlock(mouse_pos, "trash")
                        trashPos.append(trash_coord)

                elif selectButton == "Robot":
                    # limit the robot to 1
                    if bot_coord is None:
                        bot_coord = environment.updateBlock(mouse_pos, "robot")

            # right mouse button
            elif pygame.mouse.get_pressed()[2] == 1:
                # check if button is click
                selected = environment.clickDrawButton(mouse_pos)
                modeSelected = environment.clickModeButton(mouse_pos)

                if selected != -1:
                    selectButton = selected

                if modeSelected != -1:
                    selectMode = modeSelected

                    if selectMode == "Load Map":
                        environment.loadSaveMap()
                        resetVariable()
                    elif selectMode == "Save Map":
                        environment.saveMap()

        # close the application
        if event.type == pygame.QUIT:
            run_state = False
            pygame.display.quit()
            pygame.quit()

        # space key to start
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if restart is False:
                    if bot_coord is not None and len(trashPos) != 0:
                        selectButton = ""
                        environment.updateMsgBox("")
                        start = True
                        restart = True

                        if selectMode == "Dijkstra":
                            algorithm = Dijkstra(environment, bot_coord, trashPos)

                        elif selectMode == "A* Search":
                            algorithm = Astar(environment, bot_coord, trashPos)

                        elif selectMode == "BFS":
                            algorithm = BFS(environment, bot_coord, trashPos)

                        startTime = time.time()

                    else:
                        environment.updateMsgBox("Missing Robot / Trash!")
                else:
                    # reset the environment
                    resetVariable()
                    environment.resetMap()
                    environment.load_map()

    return run_state


def resetVariable():
    global selectButton, start, selectMode, algorithm, restart
    global bot_coord, del_coord, trash_coord, trashPos, startTime

    selectButton = ""
    selectMode = "Dijkstra"
    start = False
    bot_coord, del_coord, trash_coord, algorithm = None, None, None, None
    trashPos = []
    restart = False


# set up stage size.
height = 630
width = 1200
title = "DSA Group 30"
FPS = 100
running = True

# initialise the game
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((122, 123, 123))
pygame.display.set_caption(title)
pygame.display.flip()

# initialise the map
game_timer = pygame.time.Clock()
environment = Environment(height, width, screen)
environment.load_map()

# game loop for update base on FPS
while running:
    pygame.display.flip()
    running = event_handler(running)

    if start:
        result = algorithm.update()

        if result is not None:
            finalTime = time.time()
            final = round((finalTime - startTime), 3)
            environment.updateTimerBox(final)
            environment.updateMsgBox(result)
            start = False

    game_timer.tick(FPS)
