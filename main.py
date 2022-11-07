from graphics import *
from AISolver import *
import random


class Player:
    def __init__(self, center, cellSize):
        self.circle = Circle(center, cellSize / 3)
        self.pos = Point(center.x - (cellSize / 2), center.y - (cellSize / 2))
        self.cellSize = cellSize
        self.center = center

    def setColor(self, color):
        self.circle.setFill(color)

    def show(self, win):
        self.circle.draw(win)

    def checkWallChange(self, wallChanges, grid, size, yLen, win):
        for idx, wallChange in enumerate(wallChanges):
            if (self.pos.x) == wallChange[1].x and self.pos.y == wallChange[1].y:
                cell = getCellFromPos(grid, self.pos, size, yLen)
                cell.changeBorder(cell.walls)
                win.update()
                break

    def checkPortal(self, portals, win):
        for idx, portal in enumerate(portals):
            if (self.pos.x) == portal[1].x and self.pos.y == portal[1].y:
                time.sleep(0.2)
                self.circle.undraw()
                if idx == 0:
                    self.pos = Point(portals[len(portals) - 1][1].x, portals[len(portals) - 1][1].y)
                    self.circle = Circle(Point(portals[len(portals) - 1][1].x + int(self.cellSize / 2),
                                               portals[len(portals) - 1][1].y + int(self.cellSize / 2)),
                                         self.cellSize / 3)
                elif idx == len(portals) - 1:
                    self.pos = Point(portals[0][1].x, portals[0][1].y)
                    self.circle = Circle(
                        Point(portals[0][1].x + int(self.cellSize / 2), portals[0][1].y + int(self.cellSize / 2)),
                        self.cellSize / 3)
                else:
                    self.pos = Point(portals[len(portals) - idx - 1][1].x, portals[len(portals) - idx - 1][1].y)
                    self.circle = Circle(Point(portals[len(portals) - idx - 1][1].x + int(self.cellSize / 2),
                                               portals[len(portals) - idx - 1][1].y + int(self.cellSize / 2)),
                                         self.cellSize / 3)
                self.circle.draw(win)
                self.setColor("yellow")
                win.update()
                break

    def checkRewards(self, rewards, score, cellSize, win, grid, xLen, yLen):
        # if player. in rewards[1]:
        #     rewards[0].undraw()
        for item in rewards:
            if (self.pos.x) == item[1].x and self.pos.y == item[1].y:
                item[0].undraw()
                rewards.remove(item)
                score[0] += 1
                score[1].undraw()
                score[1] = Text(Point(int(cellSize / 2), int(cellSize / 2)),
                                "\tScore: " + str(score[0]) + "/" + str(score[2]))
                size = 36 - xLen - yLen
                if size < 1: size = 6
                score[1].setSize(size)
                if score[0] == score[2]:
                    score[1].setOutline("green")
                    startEnd(grid)
                else:
                    score[1].setOutline("white")
                score[1].draw(win)
                win.update()
                break
        return score

    def moveUp(self, win):
        self.circle.undraw()
        self.circle.move(0, -self.cellSize)
        self.pos = Point(self.pos.x, self.pos.y - self.cellSize)
        self.circle.draw(win)
        win.update()

    def moveDown(self, win):
        self.circle.undraw()
        self.circle.move(0, self.cellSize)
        self.pos = Point(self.pos.x, self.pos.y + self.cellSize)
        self.circle.draw(win)
        win.update()

    def moveRight(self, win):
        self.circle.undraw()
        self.circle.move(self.cellSize, 0)
        self.pos = Point(self.pos.x + self.cellSize, self.pos.y)
        self.circle.draw(win)
        win.update()

    def moveLeft(self, win):
        self.circle.undraw()
        self.circle.move(-self.cellSize, 0)
        self.pos = Point(self.pos.x - self.cellSize, self.pos.y)
        self.circle.draw(win)
        win.update()


class Cell:
    def __init__(self, x, y, size, idx):
        self.idx = idx
        self.pos = Point(x, y)
        self.coords = Point(x + (size / 2), y + (size / 2))
        self.north = Line(Point(x, y), Point(x + size, y))
        self.south = Line(Point(x, y + size), Point(x + size, y + size))
        self.east = Line(Point(x + size, y), Point(x + size, y + size))
        self.west = Line(Point(x, y), Point(x, y + size))
        self.borders = [self.north, self.south, self.east, self.west]
        self.visited = False
        self.neighbours = []
        self.walls = [True, True, True, True]

    def checkWall(self, direction):
        return self.walls[direction]

    def countWalls(self):
        cont = 0
        for i in self.walls:
            if i: cont += 1
        return cont

    def setVisible(self):
        self.setCellColor("white")

    def setCellColor(self, color):
        self.north.setOutline(color)
        self.south.setOutline(color)
        self.east.setOutline(color)
        self.west.setOutline(color)

    def drawCell(self, win):
        self.showBorder(self.north, win, 0)
        self.showBorder(self.south, win, 1)
        self.showBorder(self.east, win, 2)
        self.showBorder(self.west, win, 3)

    def setNeighbours(self, neighbours):
        self.neighbours = neighbours

    def printNeighbours(self):
        for item in self.neighbours:
            print(item)

    def showBorder(self, line, win, wall):
        self.walls[wall] = True
        line.setOutline("white")
        line.draw(win)

    def hideBorder(self, line, wall):
        self.walls[wall] = False
        line.undraw()

    def changeBorder(self, wall):
        first = 0
        while True:
            rnd = random.randint(0, len(self.walls) - 1)
            if not self.walls[rnd] and first != 0:
                second = [self.borders[rnd], wall[rnd]]
            elif first == 0:
                first = [self.borders[rnd], wall[rnd]]
        self.hideBorder(first[0], first[1])
        self.showBorder(second[0], second[1])

    def isVisited(self):
        return self.visited

    def setVisited(self):
        self.visited = True


def getCellFromPos(grid, pos, size, yLen):
    x, y = (pos.x / size) - 1, (pos.y / size) - 1
    idx = yLen * x + y
    return grid[int(idx)]


def createRectangle(xy1, xy2):
    pt1 = Point(xy1[0], xy1[1])
    pt2 = Point(xy2[0], xy2[1])
    return Rectangle(pt1, pt2)


def findNeighbours(cell, grid, xLen, yLen):
    neigbours = []
    for item in grid:
        if item.idx != cell.idx:
            if cell.idx - 1 == item.idx and cell.idx % yLen != 0:  # North
                neigbours.append([item, "north"])
            if cell.idx + 1 == item.idx and (cell.idx + 1) % yLen != 0:  # South
                neigbours.append([item, "south"])
            if cell.idx + yLen == item.idx and cell.idx < yLen * (xLen - 1):  # East
                neigbours.append([item, "east"])
            if cell.idx - yLen == item.idx and cell.idx >= yLen:  # West
                neigbours.append([item, "west"])
    cell.setNeighbours(neigbours)


def removeNeighbour(neighbours, cell, size):
    toRemove = []
    if size != 0:
        for index in range(size):
            if cell.neighbours[index][0].isVisited():
                toRemove.append(cell.neighbours[index])
        for item in toRemove:
            cell.neighbours.remove(item)
    return neighbours


def recursiveRemoval(cell, size, done, win):
    while len(done) < size:
        if cell not in done: done.append(cell)
        # cell.setBackground("red")
        for c in done:
            c.neighbours = removeNeighbour(c.neighbours, c, len(c.neighbours))
        if len(cell.neighbours) > 0:
            rnd = random.randint(0, len(cell.neighbours) - 1)
            neighbour = cell.neighbours[rnd]
            if not neighbour[0].isVisited():
                if neighbour[1] == "north":
                    cell.hideBorder(cell.north, 0)
                    neighbour[0].hideBorder(neighbour[0].south, 1)
                elif neighbour[1] == "south":
                    cell.hideBorder(cell.south, 1)
                    neighbour[0].hideBorder(neighbour[0].north, 0)
                elif neighbour[1] == "east":
                    cell.hideBorder(cell.east, 2)
                    neighbour[0].hideBorder(neighbour[0].west, 3)
                elif neighbour[1] == "west":
                    cell.hideBorder(cell.west, 3)
                    neighbour[0].hideBorder(neighbour[0].east, 2)
                neighbour[0].setVisited()
                cell.neighbours.remove(neighbour)
                line = Line(cell.coords, neighbour[0].coords)
                line.setFill("red")
                line.setWidth(5)
                line.draw(win)
                cell = neighbour[0]
        else:
            if len(done) < size:
                for item in done:
                    if len(item.neighbours) > 0:
                        cell = item
                        break


def createGrid(size, xLen, yLen):
    grid = []
    deadEnds = []
    idx = 0
    for x in range(xLen):
        for y in range(yLen):
            # rect = createRectangle([x * size + size, y * size + size], [(x + 1) * size + size, (y + 1) * size + size])
            grid.append(Cell(x * size + size, y * size + size, size, idx))
            idx += 1
    for cell in grid:
        findNeighbours(cell, grid, xLen, yLen)
        if cell.countWalls() == 3: deadEnds.append(cell)

    return grid, deadEnds


def drawGrid(grid, win):
    # for i in range (len(grid)):
    #     if i != len(grid):
    #         line = Line(grid[i].coords, grid[i+1].coords)
    #         line.setFill("red")
    #         line.setWidth(5)
    #         line.draw(win)
    #     grid[i].drawCell(win)

    for cell in grid:
        cell.drawCell(win)


def startEnd(grid):
    # grid[0].hideBorder(grid[0].north,0)
    grid[len(grid) - 1].hideBorder(grid[len(grid) - 1].south, 1)


def startGame(grid, win, cellSize, xLen, yLen, rewards, score, portals, wallChanges):
    player = Player(grid[0].coords, cellSize)
    Circle(grid[0].coords, cellSize / 3)
    player.setColor("Yellow")
    player.show(win)
    while True:
        key = win.getKey()
        cell = getCellFromPos(grid, player.pos, cellSize, yLen)
        # print(key)
        if (key == "a" or key == "Left") and not cell.checkWall(3):  # Left
            player.moveLeft(win)
        elif (key == "s" or key == "Down") and not cell.checkWall(1):  # Down
            player.moveDown(win)
        elif (key == "d" or key == "Right") and not cell.checkWall(2):  # Right
            player.moveRight(win)
        elif (key == "w" or key == "Up") and not cell.checkWall(0):  # Up
            player.moveUp(win)
        elif key == "r":  # Reset
            player.circle.move(-player.circle.getCenter().x + grid[0].coords.x,
                               -player.circle.getCenter().y + grid[0].coords.y)
            player.pos = Point(grid[0].coords.x - (cellSize / 2), grid[0].coords.y - (cellSize / 2))
        elif key == "q":  # Quit
            message = Text(Point(win.getWidth() / 2, 20), 'Click anywhere to exit')
            message.setOutline("white")
            message.draw(win)
            break

        score = player.checkRewards(rewards, score, cellSize, win, grid, xLen, yLen)
        player.checkPortal(portals, win)
        # player.checkWallChange(wallChanges, grid, cellSize, yLen, win)
        # print("Player: ",player.pos, "  last: ",grid[len(grid)-1].pos)
        if player.pos.x == grid[len(grid) - 1].pos.x and player.pos.y > grid[len(grid) - 1].pos.y:
            message = Text(Point(win.getWidth() / 2, 20), 'You won!')
            message.setOutline("white")
            message.draw(win)
            time.sleep(2)
            message.undraw()
            message = Text(Point(win.getWidth() / 2, 20), 'Click anywhere to exit')
            message.setOutline("white")
            message.draw(win)
            break

        win.update()


def makeRewards(grid, xLen, yLen, cellSize, win):
    ammount = int((xLen + yLen) / 2)
    rewards = []
    rands = []
    for i in range(ammount):
        while True:
            rnd = random.randint(0, len(grid) - 1)
            if rnd != 0 and rnd != len(grid) - 1 and rnd not in rands:
                circle = Circle(grid[rnd].coords, cellSize / 6)
                circle.setFill("green")
                circle.draw(win)
                rewards.append([circle, grid[rnd].pos])
                rands.append(rnd)
                break
    return rewards, ammount, rands


def makePortals(grid, xLen, yLen, cellSize, win, rands):
    ammount = int((xLen + yLen) / 10)
    portals = []
    for i in range(ammount * 2):
        while True:
            rnd = random.randint(0, len(grid) - 1)
            print(len(grid[rnd].neighbours))
            count = grid[rnd].countWalls()
            if rnd != 0 and rnd != len(grid) - 1 and rnd not in rands and grid[rnd].countWalls() == 3:
                rectangle = Rectangle(Point(grid[rnd].pos.x + int(cellSize / 4), grid[rnd].pos.y + int(cellSize / 4)),
                                      Point(grid[rnd].pos.x + cellSize - int(cellSize / 4),
                                            grid[rnd].pos.y + cellSize - int(cellSize / 4)))
                rectangle.setFill(color_rgb(19, 200, 191))
                rectangle.draw(win)
                portals.append([rectangle, grid[rnd].pos])
                rands.append(rnd)
                break
    return portals, rands


def makeWallChange(grid, xLen, yLen, cellSize, win, rands):
    ammount = int((xLen + yLen) / 10)
    wallChanges = []
    for i in range(ammount):
        while True:
            rnd = random.randint(0, len(grid) - 1)
            if rnd != 0 and rnd != len(grid) - 1 and rnd not in rands and grid[rnd].countWalls() == 2:
                rectangle = Rectangle(Point(grid[rnd].pos.x + int(cellSize / 4), grid[rnd].pos.y + int(cellSize / 4)),
                                      Point(grid[rnd].pos.x + cellSize - int(cellSize / 4),
                                            grid[rnd].pos.y + cellSize - int(cellSize / 4)))
                rectangle.setFill(color_rgb(255, 100, 0))
                rectangle.draw(win)
                wallChanges.append([rectangle, grid[rnd].pos])
                rands.append(rnd)
                break
    return wallChanges


def getCellSize(width, height, xLen, yLen):
    if width / (xLen + 2) < height / (yLen + 2):
        cellSize = int(width / (xLen + 2))
        height = int(cellSize * (yLen + 2))
    else:
        cellSize = int(height / (yLen + 2))
        width = int(cellSize * (xLen + 2))
    win = GraphWin("Maze", width, height)
    return cellSize, win


def drawScore(text, win):
    text.setOutline("white")
    text.draw(win)


def main():
    width = 1000
    height = 700

    xLen = int(input("Introduce number of columns: "))
    yLen = int(input("Introduce number of lines: "))

    score = [0, Text(Point(0, 0), ""), 0]
    cellSize, win = getCellSize(width, height, xLen, yLen)
    win.setBackground("black")

    grid, deadEnds = createGrid(cellSize, xLen, yLen)
    # sys.setrecursionlimit(99999)

    grid[0].setVisited()
    drawGrid(grid, win)
    recursiveRemoval(grid[0], xLen * yLen, [], win)
    grid[len(grid) - 1].hideBorder(grid[len(grid) - 1].south, 1)

    # rewards, score[2] , rands = makeRewards(grid, xLen, yLen, cellSize, win)
    # portals, rands = makePortals(grid, xLen, yLen, cellSize, win, rands)
    rewards = []
    portals = []
    # wallchanges = makeWallChange(grid, xLen, yLen, cellSize, win, rands)
    score[1] = Text(Point(int(cellSize / 2), int(cellSize / 2)), "\tScore: 0/" + str(score[2]))
    size = 36 - xLen - yLen
    if size < 1: size = 6
    score[1].setSize(size)
    # score[1].setSize(int(cellSize/2))

    # drawScore(score[1], win) //DRAW SCORE

    win.update()

    ai = AI()
    # ai.drawLine(grid, yLen, win)
    wallchanges = []
    startGame(grid, win, cellSize, xLen, yLen, rewards, score, portals, wallchanges)

    win.getMouse()
    win.close()


main()
