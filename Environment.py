import math

import pygame


class Environment:
    buttonColor = [169, 169, 169]
    buttonActive = [169, 113, 169]
    tileColor = [255, 255, 255]
    robotColor = [0, 0, 255]
    trashColor = [0, 255, 0]
    blockColor = [80, 80, 80]
    visitedColor = [255, 250, 150]
    visitedColor2 = [255, 250, 0]
    finalColor = [214, 93, 177]
    finalColor2 = [132, 94, 194]
    sideBarColor = [224, 224, 224]

    finalColorArr = []
    visitedColorArr = []
    tileMap = None

    def __init__(self, screen_height, screen_width, screen):
        # set the size of title and the spacing between each title
        self.tile_size = 18
        self.spacing = 2

        # set the font of the text
        self.font = pygame.font.SysFont('OpenSans', 24)
        self.fontHeader = pygame.font.SysFont('OpenSans', 25)

        # create button array
        self.DrawButtonArr = []
        self.modeButtonArr = []

        # set the actual map size
        self.screen = screen
        self.map_height = screen_height
        self.map_width = screen_width - 200

        self.resetMap()

    # load initial map.
    def load_map(self):
        coord_y = 0
        for y in range(len(self.tileMap)):
            coord_x = 0
            for x in range(len(self.tileMap[y])):
                if self.tileMap[y][x] == 0:
                    pygame.draw.rect(self.screen, self.tileColor, [coord_x, coord_y, self.tile_size, self.tile_size])
                elif self.tileMap[y][x] == 4:
                    pygame.draw.rect(self.screen, self.blockColor, [coord_x, coord_y, self.tile_size, self.tile_size])

                coord_x += self.tile_size + self.spacing

            coord_y += self.tile_size + self.spacing

        pygame.draw.rect(self.screen, self.sideBarColor, [self.map_width, 0, 200, self.map_height])

        # Displaying Drawing Tool section and its button
        self.screen.blit(self.fontHeader.render('Drawing Tool:', True, [128, 128, 0]),
                         [self.map_width + 30, 20, 125, 40])
        # Obstacle Button
        self.DrawButtonArr.append(self.button('Obstacle', self.buttonColor, self.map_width + 30, 60, 125, 40))
        # Trash Button
        self.DrawButtonArr.append(self.button('Trash', self.buttonColor, self.map_width + 30, 110, 125, 40))
        # robot Button
        self.DrawButtonArr.append(self.button('Robot', self.buttonColor, self.map_width + 30, 160, 125, 40))
        # Reset Tile Button
        self.DrawButtonArr.append(self.button('Delete', self.buttonColor, self.map_width + 30, 210, 125, 40))

        # Displaying Algorithms section and its button
        self.screen.blit(self.fontHeader.render('Algorithms:', True, [128, 128, 0]),
                         [self.map_width + 30, 270, 125, 40])
        # A* Star Button
        self.modeButtonArr.append(self.button('Dijkstra', self.buttonActive, self.map_width + 30, 310, 125, 40))
        # Dijkstra's Shortest Path Button
        self.modeButtonArr.append(self.button('A* Search', self.buttonColor, self.map_width + 30, 360, 125, 40))
        # Breadth First Search Button
        self.modeButtonArr.append(self.button('BFS', self.buttonColor, self.map_width + 30, 410, 125, 40))
        # "Load map" Button
        self.modeButtonArr.append(self.button('Load Map', self.buttonColor, self.map_width + 30, 460, 125, 40))
        # "Save" Button
        self.modeButtonArr.append(self.button('Save Map', self.buttonColor, self.map_width + 30, 510, 125, 40))

    # update the block base on the user input
    def updateBlock(self, mouse_pos, block_type):
        columns = int(math.floor(mouse_pos[0] / (self.tile_size + self.spacing)))
        rows = int(math.floor(mouse_pos[1] / (self.tile_size + self.spacing)))

        if columns < len(self.tileMap[0]) and rows < len(self.tileMap):
            coord_x = columns * (self.spacing + self.tile_size)
            coord_y = rows * (self.spacing + self.tile_size)

            if block_type == "block":
                self.tileMap[rows][columns] = 4
                pygame.draw.rect(self.screen, self.blockColor, [coord_x, coord_y, self.tile_size, self.tile_size])

            elif block_type == "trash":
                if self.tileMap[rows][columns] != 1:
                    self.tileMap[rows][columns] = 1
                    pygame.draw.rect(self.screen, self.trashColor, [coord_x, coord_y, self.tile_size, self.tile_size])
                else:
                    return None

            elif block_type == "robot":
                self.tileMap[rows][columns] = 2
                pygame.draw.rect(self.screen, self.robotColor, [coord_x, coord_y, self.tile_size, self.tile_size])

            elif block_type == "tile":
                self.tileMap[rows][columns] = 0
                pygame.draw.rect(self.screen, self.tileColor, [coord_x, coord_y, self.tile_size, self.tile_size])

            value = (rows, columns)
            return value

    # click button
    def clickDrawButton(self, mouse_pos):
        # check draw button
        for x in range(len(self.DrawButtonArr)):
            limitX = self.DrawButtonArr[x][1] + self.DrawButtonArr[x][3]
            limitY = self.DrawButtonArr[x][2] + self.DrawButtonArr[x][4]

            if self.DrawButtonArr[x][1] < mouse_pos[0] < limitX and self.DrawButtonArr[x][2] < mouse_pos[1] < limitY:
                color = self.DrawButtonArr[x][5]
                if color == self.buttonColor:
                    self.clearDrawButton()
                    self.DrawButtonArr[x] = self.button(self.DrawButtonArr[x][0], self.buttonActive,
                                                        self.DrawButtonArr[x][1], self.DrawButtonArr[x][2],
                                                        self.DrawButtonArr[x][3], self.DrawButtonArr[x][4])

                    return self.DrawButtonArr[x][0]
                else:
                    self.clearDrawButton()
                    return None

        return -1

    # select Mode button
    def clickModeButton(self, mouse_pos):
        # check mode button
        for y in range(len(self.modeButtonArr)):
            limitX = self.modeButtonArr[y][1] + self.modeButtonArr[y][3]
            limitY = self.modeButtonArr[y][2] + self.modeButtonArr[y][4]

            if self.modeButtonArr[y][1] < mouse_pos[0] < limitX and self.modeButtonArr[y][2] < mouse_pos[1] < limitY:
                color = self.modeButtonArr[y][5]
                if color == self.buttonColor:
                    self.clearModeButton()
                    self.modeButtonArr[y] = self.button(self.modeButtonArr[y][0], self.buttonActive,
                                                        self.modeButtonArr[y][1], self.modeButtonArr[y][2],
                                                        self.modeButtonArr[y][3], self.modeButtonArr[y][4])

                    return self.modeButtonArr[y][0]

        return -1

    # clear draw button
    def clearDrawButton(self):
        for x in range(len(self.DrawButtonArr)):
            self.DrawButtonArr[x] = self.button(self.DrawButtonArr[x][0], self.buttonColor,
                                                self.DrawButtonArr[x][1], self.DrawButtonArr[x][2],
                                                self.DrawButtonArr[x][3], self.DrawButtonArr[x][4])

    # clear mode button
    def clearModeButton(self):
        for x in range(len(self.modeButtonArr)):
            self.modeButtonArr[x] = self.button(self.modeButtonArr[x][0], self.buttonColor,
                                                self.modeButtonArr[x][1], self.modeButtonArr[x][2],
                                                self.modeButtonArr[x][3], self.modeButtonArr[x][4])

    # create button function
    def button(self, msg, color, x, y, w, h):
        textSurf = self.font.render(msg, True, [255, 250, 205])
        textRect = textSurf.get_rect()
        textRect.center = ((x + w / 2), (y + (h / 2)))
        pygame.draw.rect(self.screen, color, [x, y, w, h])
        self.screen.blit(textSurf, textRect)
        button = (msg, x, y, w, h, color)
        return button

    # draw visited tile
    def visitedTile(self, columns, rows):
        coord_x = columns * (self.spacing + self.tile_size)
        coord_y = rows * (self.spacing + self.tile_size)
        if self.tileMap[rows][columns] == 0:
            pygame.draw.rect(self.screen, self.visitedColorArr[0], [coord_x, coord_y, self.tile_size, self.tile_size])

    '''
        Draw final path
        input: 2D array (rows, columns)
    '''

    def drawFinalpath(self, path):
        # write step into gui
        self.updateStepCount(len(path))

        for x in range(len(path)):
            rows = path[x][0]
            columns = path[x][1]
            coord_x = columns * (self.spacing + self.tile_size)
            coord_y = rows * (self.spacing + self.tile_size)

            if self.tileMap[rows][columns] == 0:
                self.tileMap[rows][columns] = 3
                pygame.draw.rect(self.screen, self.finalColorArr[0], [coord_x, coord_y, self.tile_size, self.tile_size])

            elif self.tileMap[rows][columns] == 3:
                pygame.draw.rect(self.screen, [0, 142, 155], [coord_x, coord_y, self.tile_size, self.tile_size])

        self.finalColorArr.pop(0)
        self.visitedColorArr.pop(0)

    # update message box
    def updateMsgBox(self, msg):
        x, y, w, h = self.map_width + 5, 570, 180, 40
        # overwrite the text and re-render the text
        pygame.draw.rect(self.screen, self.sideBarColor, [x, y, w, h])
        textSurf = self.font.render(msg, True, [255, 0, 0])
        textRect = textSurf.get_rect()
        textRect.center = ((x + w / 2), (y + (h / 2)))
        self.screen.blit(textSurf, textRect)

    # update timer box
    def updateTimerBox(self, finalTime):
        finalTime = "Time Taken: " + str(finalTime) + " seconds"

        x, y, w, h = 0, 595, 500, 40
        textTime = self.font.render(finalTime, True, [255, 255, 255])
        textTimeRec = textTime.get_rect()
        textTimeRec.center = ((x + w / 2), (y + (h / 2)))
        self.screen.blit(textTime, textTimeRec)

    # udpate step count
    def updateStepCount(self, value):
        self.stepCount += value
        printString = "Step taken: " + str(self.stepCount)

        x, y, w, h = 500, 595, 500, 40
        textStep = self.font.render(printString, True, [255, 255, 255])
        textStepRec = textStep.get_rect()
        textStepRec.center = ((x + w / 2), (y + (h / 2)))
        self.screen.blit(textStep, textStepRec)

    # load tile map file
    def loadSaveMap(self):
        self.resetMap()
        # clear the existing tile map
        self.tileMap = []

        f = open("textMap.txt", "r")
        for line in f:
            self.tileMap.append([int(x) for x in line.split(',')])
        f.close()
        self.updateMsgBox("Map Loaded!")
        self.load_map()

    # save tile map
    def saveMap(self):
        f = open("textMap.txt", "w")

        for x in range(30):
            for y in range(49):
                if self.tileMap[x][y] == 4:
                    f.writelines(str(self.tileMap[x][y]) + ",")
                else:
                    f.writelines("0,")

            if self.tileMap[x][y + 1] == 4:
                f.write(str(self.tileMap[x][y + 1]) + "\n")
            else:
                f.write("0\n")

        f.close()
        self.updateMsgBox("Map Saved!")

    # reset environment
    def resetMap(self):
        # 2D map layout.
        self.tileMap = [[0 for c in range(50)] for r in range(30)]

        # variable
        self.stepCount = 0

        # color Array
        self.finalColorArr = [self.finalColor, self.finalColor2]
        self.visitedColorArr = [self.visitedColor, self.visitedColor2]

        # draw rect to override time box
        pygame.draw.rect(self.screen, [122, 123, 123], [0, 595, 1000, 40])

    # print the 2D map layout.
    def printTitle(self):
        for r in range(len(self.tileMap)):
            print self.tileMap[r]
