import dijkstra
import random
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import*

matrix = []
graph = dijkstra.Graph([])

snake = []
food = []
wall = []


def initializeAll():
    createMatrix()
    createFood()
    createSnake()
    move()


def createSnake():
    snake.append([7, 7])
    snake.append([7, 8])
    snake.append([7, 9])
    snake.append([8, 9])
    snake.append([8, 10])
    snake.append([8, 11])
    snake.append([8, 12])
    snake.append([8, 13])


def createMatrix():
    for i in range(15):
        row = []
        for j in range(15):
            cell = [i, j]
            row.append(cell)
        matrix.append(row)
    populateGraph()


def createGraphImage():
    saveGraph = nx.Graph([])
    saveGraph = graph
    nx.draw(graph)
    plt.savefig("paths_graph.png")


def populateGraph():
    for i in range(15):
        for j in range(15):
            if(matrix[i][j] == [0, 0]):
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(matrix[i][j] == [0, 14]):
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(matrix[i][j] == [14, 0]):
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(matrix[i][j] == [14, 14]):
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(i == 0):
                if(j != 0 and j != 14):
                    graph.add_edge(matrix[i][j], matrix[i][j+1])
                    graph.add_edge(matrix[i][j], matrix[i][j-1])
                    graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(i == 14):
                if(j != 0 and j != 14):
                    graph.add_edge(matrix[i][j], matrix[i][j+1])
                    graph.add_edge(matrix[i][j], matrix[i][j-1])
                    graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(j == 0):
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(j == 14):
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            else:
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i][j-1])


def saveGraph():
    nx.draw(Graph(graph))
    plt.savefig("paths_graph.png")


def createFood():
    for i in range(2):
        r1 = random.randint(0, 14)
        r2 = random.randint(0, 14)
        f = [r1, r2]
        if(f in snake):
            if(len(food) < 2):
                createFood()
            else:
                break
        else:
            food.append(f)
            if(len(food) == 2):
                break


def removeSnakeFromGraph():
    graph.remove_edge(snake[0], snake[1])
    graph.remove_edge(snake[1], snake[2])
    graph.remove_edge(snake[2], snake[3])
    graph.remove_edge(snake[3], snake[4])
    graph.remove_edge(snake[4], snake[5])
    graph.remove_edge(snake[5], snake[6])


def addSnakeToGraph():
    graph.add_edge(snake[0], snake[1])
    graph.add_edge(snake[1], snake[2])
    graph.add_edge(snake[2], snake[3])
    graph.add_edge(snake[3], snake[4])
    graph.add_edge(snake[4], snake[5])
    graph.add_edge(snake[5], snake[6])


def move():
    while (True):
        removeSnakeFromGraph()
        if(len(food) == 2):
            print("Food1 = " + str(food[0]))
            print("Food2 = " + str(food[1]))
            print("Head = " + str(snake[0]))
            if (str(snake[0]) == str(food[1])):
                food.remove(food[1])
            if (str(snake[0]) == str(food[0])):
                food.remove(food[0])

        if(len(food) == 1):
            print("Food1 = " + str(food[0]))
            print("Head = " + str(snake[0]))
            if(str(snake[0]) == str(food[0])):
                food.remove(food[0])

        if(len(food) == 0):
            False
            print("Sve si popapal, gladus jedan :D")
            break

        path = closestFood(snake[0])

        snake.insert(0, path[1])
        del snake[-1]
        addSnakeToGraph()


def closestFood(head):
    path = []
    if(len(food) == 1):
        path = graph.dijkstra(str(head), str(food[0]))
    else:
        path1 = graph.dijkstra(str(head), str(food[0]))
        path2 = graph.dijkstra(str(head), str(food[1]))
        if(len(path1) <= len(path2)):
            path = path1
        else:
            path = path2
    print(path)
    return path


def calculateObjectPosition(a, b):
    position, newI, newJ = 0, 0, 0
    foundA, foundB = False, False
    for j in range(CON.CELLS):
        calc = (j)*CON.STEP + CON.PIXEL
        if calc == a:
            newI = j
            foundA = True
        if calc == b:
            newJ = j
            foundB = True
        if(foundA and foundB):
            break

    position = (newJ*CON.CELLS)+newI
    print(position)
    return position


class Shape:
    """This is a template to make obstacles and snake body parts"""

    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        if kind == "snake":
            self.ref = Canvas.create_rectangle(self.can,
                                               a - CON.SN_SIZE, b - CON.SN_SIZE,
                                               a + CON.SN_SIZE, b + CON.SN_SIZE,
                                               fill=CON.SN_COLOR,
                                               width=2)
        elif kind == "food":
            self.ref = Canvas.create_oval(self.can,
                                          a - CON.OB_SIZE, b - CON.OB_SIZE,
                                          a + CON.SN_SIZE, b + CON.SN_SIZE,
                                          fill=CON.OB_COLOR,
                                          width=2)

    def modify(self, a, b):
        self.x, self.y = a, b
        self.can.coords(self.ref,
                        a - CON.SIZE[self.kind], b - CON.SIZE[self.kind],
                        a + CON.SIZE[self.kind], b + CON.SIZE[self.kind])

    def delete(self):
        self.can.delete(self.ref)


# print(graph.edges)
master = Tk()

w = Canvas(master, width=300, height=300)

w.pack()
"""Drawing vertical lines"""
w.create_line(0, 20, 300, 20)
w.create_line(0, 40, 300, 40)
w.create_line(0, 60, 300, 60)
w.create_line(0, 80, 300, 80)
w.create_line(0, 100, 300, 100)
w.create_line(0, 120, 300, 120)
w.create_line(0, 140, 300, 140)
w.create_line(0, 160, 300, 160)
w.create_line(0, 180, 300, 180)
w.create_line(0, 200, 300, 200)
w.create_line(0, 220, 300, 220)
w.create_line(0, 240, 300, 240)
w.create_line(0, 260, 300, 260)
w.create_line(0, 280, 300, 280)
w.create_line(0, 300, 300, 300)
"""Drawing horizontal lines"""
w.create_line(20, 0, 20, 300)
w.create_line(40, 0, 40, 300)
w.create_line(60, 0, 60, 300)
w.create_line(80, 0, 80, 300)
w.create_line(100, 0, 100, 300)
w.create_line(120, 0, 120, 300)
w.create_line(140, 0, 140, 300)
w.create_line(160, 0, 160, 300)
w.create_line(180, 0, 180, 300)
w.create_line(200, 0, 200, 300)
w.create_line(220, 0, 220, 300)
w.create_line(240, 0, 240, 300)
w.create_line(260, 0, 260, 300)
w.create_line(280, 0, 280, 300)
w.create_line(300, 0, 300, 300)

w.create_rectangle(40, 60, 60, 40, fill='red')

mainloop()
