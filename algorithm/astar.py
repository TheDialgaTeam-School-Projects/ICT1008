import pygame
import math
from pygame.locals import *
from priority_queue import PQ


class Astar:
    def __init__(self, Environment, start, end):
        self.environment = Environment
        self.map = self.environment.tileMap

        # create variable
        self.trashPQ = PQ()
        self.possibleList = PQ()
        self.visitedList = []
        self.notFound = 0

        # calculate diagonal cost
        self.diagonal_cost = math.sqrt((len(self.map) ** 2) + (len(self.map[0]) ** 2)) / len(self.map)

        # create start and end node
        self.startNode = Node(None, start[0], start[1])

        # add all trash into PQ.
        for x in range(len(end)):
            temp = Node(None, end[x][0], end[x][1])
            temp.f = math.sqrt((abs(temp.posR - start[0])**2) + (abs(temp.posC - start[1])**2))
            self.trashPQ.insert(temp)

        # select the closest trash as initial end point.
        self.endNode = self.trashPQ.deleteMin()

        # add start node value
        self.startNode.g = 0
        self.startNode.h = self.calculateDist(self.startNode, self.endNode, self.diagonal_cost)
        self.startNode.f = self.startNode.h + self.startNode.g

        self.possibleList.insert(self.startNode)

    def update(self):
        if self.possibleList.isEmpty() is False:
            # get the minimum f value node from the PQ
            currentNode = self.possibleList.deleteMin()

            # add it to the visitedList to reduce duplicate.
            self.visitedList.append(currentNode)

            # check for end condition
            if currentNode == self.endNode:
                path = []
                # format the coord
                while currentNode.parent is not None:
                    position = [currentNode.posR, currentNode.posC]
                    path.append(position)
                    currentNode = currentNode.parent

                self.environment.drawFinalpath(path)

                if self.trashPQ.isEmpty():
                    if self.notFound > 0:
                        return "Fail to locate " + str(self.notFound) + " trash"
                    else:
                        return "Job completed!"
                else:
                    # clear PQ and select new start point.
                    self.visitedList = []
                    self.possibleList.clear()
                    self.startNode = self.endNode
                    self.endNode = self.trashPQ.deleteMin()

                    # initialise the new start node.
                    self.startNode.g = 0
                    self.startNode.h = self.calculateDist(self.startNode, self.endNode, self.diagonal_cost)
                    self.startNode.f = self.startNode.h + self.startNode.g

                    # insert new start point in to PQ
                    self.possibleList.insert(self.startNode)
                    return

            # create children of the nearby tile
            children = []
            for r in range(-1, 2):
                for c in range(-1, 2):
                    if r == 0 and c == 0:
                        continue
                    else:
                        tempR = currentNode.posR + r
                        tempC = currentNode.posC + c

                        # check if the tile exist on the map
                        if self.checkValid(tempR, tempC) is True:
                            newNode = Node(currentNode, tempR, tempC)
                            children.append(newNode)

            # loop through the tile
            for currentChild in children:
                # check if the tile is already visited
                if currentChild in self.visitedList:
                    continue

                # calculate the cost of traveling to the node
                cost = currentNode.g + self.calculateDist(currentNode, currentChild, self.diagonal_cost)

                # if it is a newly discovered node add to possible list
                if self.possibleList.contain(currentChild) is False:
                    currentChild.g = cost
                    currentChild.h = self.calculateDist(currentChild, self.endNode, self.diagonal_cost)
                    currentChild.f = currentChild.g + currentChild.h

                    self.possibleList.insert(currentChild)

                    # draw checked
                    self.environment.visitedTile(currentChild.posC, currentChild.posR)

                # if the cost higher than a per - discovered path -> skip it.
                elif cost >= currentChild.g:
                    continue

        else:
            if self.trashPQ.isEmpty():
                return "Fail to locate " + str(self.notFound) + " trash"
            else:
                # clear PQ and select new start point.
                self.visitedList = []
                self.possibleList.clear()
                self.notFound += 1
                self.endNode = self.trashPQ.deleteMin()
                self.possibleList.insert(self.startNode)
                return

    # check if tile is within range
    def checkValid(self, r, c):
        if r >= len(self.map) or r < 0 or c >= len(self.map[0]) or c < 0:
            return False
        elif self.map[r][c] == 4:
            return False
        else:
            return True

    def calculateDist(self, child, endNode, diagonal_cost):
        distR = abs(child.posR - endNode.posR)
        distC = abs(child.posC - endNode.posC)

        if distR > distC:
            return (distC * diagonal_cost) + (1 * (distR - distC))
        else:
            return (distR * diagonal_cost) + (1 * (distC - distR))


class Node:
    def __init__(self, parent, row, col):
        self.parent = parent
        self.posR = row
        self.posC = col

        # distance between the current node to start node
        self.g = float("inf")
        # estimated distance from current node to end node
        self.h = float("inf")
        # total cost the node.
        self.f = float("inf")

    # overload operator
    def __eq__(self, other):
        if self.posR == other.posR and self.posC == other.posC:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.f > other.f:
            return True
        else:
            return False