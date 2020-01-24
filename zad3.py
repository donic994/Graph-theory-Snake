import dijkstra
import random
import networkx as nx
import matplotlib.pyplot as plt
import copy
from tkinter import Tk,Canvas

matrix = []
graph = dijkstra.Graph([])

snake = []
snakeBodyParts = []
snakeTemp = []
food = []
foodObject = []

tk = Tk()
tk.title = "Snake"
tk.resizable(0,0)

w = Canvas(tk, width=300, height=300, bg = '#FFFAF0')
w.pack()


def initializeAll(w):
    createMatrix()
    createSnake()
    showSnake()
    snakeTemp = copy.deepcopy(snake)
    createFood()
    showFood()

    move(snakeTemp)

def createMatrix():
    for i in range(0,16):
        row = []
        for j in range(0,16):
            cell = [i, j]
            row.append(cell)
        matrix.append(row)
    populateGraph()

def populateGraph():
    for i in range(1,16):
        for j in range(1,16):
            if(matrix[i][j] == [1,1]):
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(matrix[i][j] == [1, 15]):
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(matrix[i][j] == [15, 1]):
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(matrix[i][j] == [15, 15]):
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(i == 1):
                if(j != 1 and j != 15):
                    graph.add_edge(matrix[i][j], matrix[i][j+1])
                    graph.add_edge(matrix[i][j], matrix[i][j-1])
                    graph.add_edge(matrix[i][j], matrix[i+1][j])
            elif(i == 15):
                if(j != 1 and j != 15):
                    graph.add_edge(matrix[i][j], matrix[i][j+1])
                    graph.add_edge(matrix[i][j], matrix[i][j-1])
                    graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(j == 1):
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            elif(j == 15):
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i][j-1])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
            else:
                graph.add_edge(matrix[i][j], matrix[i+1][j])
                graph.add_edge(matrix[i][j], matrix[i-1][j])
                graph.add_edge(matrix[i][j], matrix[i][j+1])
                graph.add_edge(matrix[i][j], matrix[i][j-1])

def createSnake():
    r1 = random.randint(1, 15)
    r2 = random.randint(1, 15)
    if(r1 <= 8 and r2 < 10):
        snake.append(str([r1, r2]))
        snake.append(str([r1, r2+1]))
        snake.append(str([r1, r2+2]))
        snake.append(str([r1, r2+3]))
        snake.append(str([r1, r2+4]))
        snake.append(str([r1, r2+5]))
        snake.append(str([r1, r2+6]))
    elif(r2 <= 8):
        snake.append(str([r1, r2]))
        snake.append(str([r1-1, r2]))
        snake.append(str([r1-2, r2]))
        snake.append(str([r1-3, r2]))
        snake.append(str([r1-4, r2]))
        snake.append(str([r1-5, r2]))
        snake.append(str([r1-6, r2]))
    else:
        snake.append(str([r1, r2]))
        snake.append(str([r1, r2-1]))
        snake.append(str([r1, r2-2]))
        snake.append(str([r1, r2-3]))
        snake.append(str([r1, r2-4]))
        snake.append(str([r1, r2-5]))
        snake.append(str([r1, r2-6]))

def showSnake():
    for s in snake:
        stringBodyPart = s.split(',')
        x1 = int(stringBodyPart[0][1:])
        y1 = int(stringBodyPart[1][:-1])
        bodyPart = w.create_rectangle(
            x1*20-20, y1*20-20, x1*20, y1*20, fill='#22bb45')
        snakeBodyParts.append(bodyPart)

def createFood():
    for _ in range(2):
        r1 = random.randint(1, 15)
        r2 = random.randint(1, 15)
        f = [r1, r2]
        if(str(f) in snake):
            if(len(food) < 2):
                r1 = random.randint(1, 15)
                r2 = random.randint(1, 15)
                f = [r1, r2]
                createFood()
            else:
                break
        else:
            food.append(f)
            if(len(food) == 2):
                break

def showFood():
    for var in food:
        x1 = var[0]
        y1 = var[1]
        f = w.create_rectangle(x1*20-20, y1*20-20, x1*20, y1*20, fill='#b94522')
        foodObject.append(f)

def removeSnakeFromGraph(snakeTemp):
    graph.remove_edge(str(snake[0]), str(snake[1]))
    graph.remove_edge(str(snake[0]), str(snake[2]))
    graph.remove_edge(str(snake[0]), str(snake[3]))
    graph.remove_edge(str(snake[0]), str(snake[4]))
    graph.remove_edge(str(snake[0]), str(snake[5]))
    graph.remove_edge(str(snake[0]), str(snake[6]))
    graph.remove_edge(str(snake[1]), str(snake[2]))
    graph.remove_edge(str(snake[2]), str(snake[3]))
    graph.remove_edge(str(snake[3]), str(snake[4]))
    graph.remove_edge(str(snake[4]), str( snake[5]))
    graph.remove_edge(str(snake[5]), str(snake[6]))

    graph.remove_edge(str(snake[0]), str(snakeTemp[0]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[1]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[2]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[3]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[4]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[5]))
    graph.remove_edge(str(snake[0]), str(snakeTemp[6]))

    # graph.remove_edge(snake[0], snake[0])
    # graph.remove_edge(snake[1], snake[1])
    # graph.remove_edge(snake[2], snake[2])
    # graph.remove_edge(snake[3], snake[3])
    # graph.remove_edge(snake[4], snake[4])
    # graph.remove_edge(snake[5], snake[5])
    # graph.remove_edge(snake[6], snake[6])


def addSnakeToGraph():
    graph.add_edge(str(snake[0]),str( snake[1]))
    graph.add_edge(str(snake[1]),str( snake[2]))
    graph.add_edge(str(snake[2]),str( snake[3]))
    graph.add_edge(str(snake[3]), str(snake[4]))
    graph.add_edge(str(snake[4]), str(snake[5]))
    graph.add_edge(str(snake[5]), str(snake[6]))
    # graph.add_edge(snake[0], snake[0])
    # graph.add_edge(snake[1], snake[1])
    # graph.add_edge(snake[2], snake[2])
    # graph.add_edge(snake[3], snake[3])
    # graph.add_edge(snake[4], snake[4])
    # graph.add_edge(snake[5], snake[5])
    # graph.add_edge(snake[6], snake[6])

def move(snakeTemp):
    while (True):
        tk.update()
        removeSnakeFromGraph(snakeTemp)
        if(len(food) == 2):
            print("Food1 = " + str(food[0]))
            print("Food2 = " + str(food[1]))
            print("Head = " + str(snake[0]))
            if (str(snake[0]) == str(food[1])):
                food.remove(food[1])
                w.delete(foodObject[1])
            if (str(snake[0]) == str(food[0])):
                food.remove(food[0])
                w.delete(foodObject[0])

        if(len(food) == 1):
            print("Food1 = " + str(food[0]))
            print("Head = " + str(snake[0]))
            if(str(snake[0]) == str(food[0])):
                food.remove(food[0])
                w.delete(foodObject[0])

        if(len(food) == 0):
            False
            print("Sve si popapal, gladus jedan :D")
            tk.mainloop()
            break

        path = closestFood(snake[0])

        addSnakeToGraph()
        snake.insert(0, path[1])
        moveSnake(w)
        showPathWhileMoving(w)


def closestFood(head):
    path = []
    if(len(food) == 1):
        path = graph.dijkstra(str(head), str(food[0]))
    elif(len(food)==2):
        path1 = graph.dijkstra(str(head), str(food[0]))
        path2 = graph.dijkstra(str(head), str(food[1]))
        if(len(path1) <= len(path2)):
            path = path1
        else:
            path = path2
    print(path)
    return path

def showPathWhileMoving(w):
    stringBodyPart = snake[6].split(',')
    x1 = int(stringBodyPart[0][1:])
    y1 = int(stringBodyPart[1][:-1])
    w.create_rectangle(x1*20-20, y1*20-20, x1*20, y1*20, fill='#2296b9')

def moveSnake(w):
    stringBodyPart = snake[0].split(',')
    x1 = int(stringBodyPart[0][1:])
    y1 = int(stringBodyPart[1][:-1])
    bodyPart = w.create_rectangle(
        x1*20-20, y1*20-20, x1*20, y1*20, fill='#22bb45')
    snakeBodyParts.insert(0, bodyPart)
    tail = snakeBodyParts[7]
    w.delete(tail)
    del snakeBodyParts[-1]

def drawLinesInCanvas():
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

drawLinesInCanvas()

initializeAll(w)
