import math
from priority_queue import PQ


class Node:
    def __init__(self, row, column):
        self.parent = None
        self.row = row
        self.column = column
        self.distance = 0

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance


class BFS:

    def __init__(self, environment, start, end):
        self.environment = environment
        self.map = self.environment.tileMap

        # create variable
        self.trashPQ = PQ()
        self.notFound = 0

        # add all trash into PQ.
        for x in range(len(end)):
            trash = Node(end[x][0], end[x][1])
            trash.distance = math.sqrt((abs(trash.row - start[0]) ** 2) + (abs(trash.column - start[1]) ** 2))
            self.trashPQ.insert(trash)

        # create start and end node
        self.startNode = Node(start[0], start[1])

        # select the closest trash as initial end point.
        self.endNode = self.trashPQ.deleteMin()

        self.visitedNodes = []

        self.possibleNodes = [self.startNode]

    def isValidNode(self, row, column):
        return 0 <= row < len(self.map) and 0 <= column < len(self.map[0]) and self.map[row][column] != 4

    def findNewPath(self, currentNode):
        for row in range(1, -2, -1):
            for column in range(1, -2, -1):
                if row == 0 and column == 0:
                    # Skip current node position.
                    continue

                nextRow = currentNode.row + row
                nextColumn = currentNode.column + column

                if not self.isValidNode(nextRow, nextColumn):
                    # Node is not valid, skip this node.
                    continue

                # Node is valid, create this new node.
                newNode = Node(nextRow, nextColumn)
                newNode.parent = currentNode

                if newNode in self.visitedNodes:
                    # If node is already created, skip this.
                    continue

                if (row < 0 or row > 0) and (column < 0 or column > 0):
                    # Diagonal cost is actually more than straight path.
                    newNode.distance = currentNode.distance + math.sqrt(2)
                else:
                    newNode.distance = currentNode.distance + 1

                self.environment.visitedTile(newNode.column, newNode.row)
                self.possibleNodes.append(newNode)

                self.visitedNodes.append(newNode)

    def getEndNodeIsInPossibleNodes(self):
        for i in range(len(self.possibleNodes)):
            if self.endNode == self.possibleNodes[i]:
                return True
        return False

    def getEndNodeFromPossibleNodes(self):
        for i in range(len(self.possibleNodes)):
            if self.endNode == self.possibleNodes[i]:
                return self.possibleNodes[i]
        return None

    def resetPath(self, startNode, endNode):
        self.visitedNodes = []

        self.possibleNodes = [startNode]

        self.startNode = startNode
        self.startNode.distance = 0

        self.endNode = endNode

    def update(self):
        if len(self.possibleNodes) == 0:
            self.notFound = self.notFound + 1

            if self.trashPQ.isEmpty():
                # No more trash to find.
                return "Fail to locate " + str(self.notFound) + " trash"

            # If there are more trash to find.
            self.resetPath(self.startNode, self.trashPQ.deleteMin())
        else:
            # If there are possible path, let's check if any of them are the end node.
            if not self.getEndNodeIsInPossibleNodes():
                # None of them are end nodes so let's find new nodes.
                self.findNewPath(self.possibleNodes.pop(0))
            else:
                # Final path have been found.
                path = []
                currentNode = self.getEndNodeFromPossibleNodes()

                while currentNode.parent is not None:
                    path.append([currentNode.row, currentNode.column])
                    currentNode = currentNode.parent

                self.environment.drawFinalpath(path)

                if self.trashPQ.isEmpty():
                    if self.notFound > 0:
                        return "Fail to locate " + str(self.notFound) + " trash"
                    else:
                        # No more trash to find.
                        return "Job completed!"

                # If there are more trash to find.
                self.resetPath(self.endNode, self.trashPQ.deleteMin())
