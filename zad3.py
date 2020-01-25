"""
ASSIGNMENT 3:
A small application with 15x15 grid needs to be implemented. 
Each box on the grid has its own coordinate.
On that grid, a 7-squares long snake should be displayed. 
The position and orientation of the snake should be determined randomly, as should the position of the two squares. 
The size of the snake remains the same when collecting new squares.
It is necessary to find the shortest path by which the snake would pick up both squares 
without colliding with itself or against the wall, that is, the edge of the grid. 
Should such a scenario occur, it would collide with itself or hit the edge of the net, 
the game is over and the task must be solved from scratch.
Additional constraint is that the snake should not repeat the path she had already taken,
but use the path that the snake did not go through as it went to collect the first square.
Attach graphic images of the implemented solution. 
It is important to see the initial situation and the shortest path to the final solution.
Show the movement of the snake graphically (from a software solution or displayed in an arbitrary graphical tool) 
and by specifying the coordinates of the boxes.
"""

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
tk.title("Snake")
tk.resizable(0,0)

w = Canvas(tk, width=300, height=300, bg = '#FFFAF0')
w.pack()

"""
This method initializes methods for creating matrix, snake and food
"""
def initializeAll(w):
    createMatrix()
    createSnake()
    showSnake()
    snakeTemp = copy.deepcopy(snake)
    createFood()
    showFood()

    move(snakeTemp)

"""
Creates matrix that we later transfer to a graph
"""
def createMatrix():
    for i in range(0,16):
        row = []
        for j in range(0,16):
            cell = [i, j]
            row.append(cell)
        matrix.append(row)
    populateGraph()

"""
Populates graph with vertices that are neighbours
Two vertices are neighbours if they have mutual edge in a matrix/grid.
"""
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

"""
Creates a snake that is seven consecutive squares long.
Positions of squares are selected in such way that no square ends up in a wall.
Positions oof squares are stored in a list.
"""
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

"""
Creates snake body parts based on square positions that we can show on canvas.
Body parts are represented as green rectangles on canvas.
Body parts(rectangles on canvas) are stored in a list so we can manipulate with them later on.
"""
def showSnake():
    for s in snake:
        stringBodyPart = s.split(',')
        x1 = int(stringBodyPart[0][1:])
        y1 = int(stringBodyPart[1][:-1])
        bodyPart = w.create_rectangle(
            x1*20-20, y1*20-20, x1*20, y1*20, fill='#22bb45')
        snakeBodyParts.append(bodyPart)

"""
Creates two foods. 
Generates random x and y positon of a food to be represented on grid. 
If the food position is not already taken by the snakes body, we save it in a list.
If the food position is already taken by the snakes body, we generate new position as long as we dont get the one that isnt taken.
"""
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

"""
Creates food object based on food positions that we can show on canvas.
Food objects are represented as red rectangles on canvas.
Food objects (rectangles on canvas) are stored in a list so we can manipulate with them later on.
"""
def showFood():
    for var in food:
        x1 = var[0]
        y1 = var[1]
        f = w.create_rectangle(x1*20-20, y1*20-20, x1*20, y1*20, fill='#b94522')
        foodObject.append(f)

"""
Removes edges from the graph that are located in snake.
This is done so we won't have to deal with snake eating herself.
By removing edges from the graph, our algorithm (Dijkstra) can't take those edges in calculation 
and therefore snake can't take path that colides with her own body.
Since we can't use the squares we have already visited we are removing those edges from graph permanently(we don't add them back later)
"""
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

"""
Adding edges to the graph that are located in snake.
"""
def addSnakeToGraph():
    graph.add_edge(str(snake[0]),str( snake[1]))
    graph.add_edge(str(snake[1]),str( snake[2]))
    graph.add_edge(str(snake[2]),str( snake[3]))
    graph.add_edge(str(snake[3]), str(snake[4]))
    graph.add_edge(str(snake[4]), str(snake[5]))
    graph.add_edge(str(snake[5]), str(snake[6]))

"""
First we are removing snake from graph.
Second we are checking how many more foods are there left to eat.
We are comparing snakes head position with position of the food. 
If they are the same, we are removing the food from list, and also deleting food object from canvas.
Then we are calculating closest path to the food, adding next postion in path as snakes new head and moving snake to its new position.
If there is no more food left, we print cute message and the game is over.
"""
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

"""
Calculates the paths from snakes head to food, compares path lenghts and chooses the shortest of the two.
Returns list of vertices in the path.
"""
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

"""
Shows the trail behind snake of all positions snake has passed.
"""
def showPathWhileMoving(w):
    stringBodyPart = snake[7].split(',')
    x1 = int(stringBodyPart[0][1:])
    y1 = int(stringBodyPart[1][:-1])
    w.create_rectangle(x1*20-20, y1*20-20, x1*20, y1*20, fill='#2296b9')

"""
This method likes to MOVE IT, MOVE IT. 
This method takes the new head of the snake and based on its position creates body part.
After the body part is created it is added to the FIRST position in the list of body parts.
Last element od body part (tail) list is deleted.
Adding new head, and deleting tail gives the impression of the snake moving on the canvas.
"""
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

"""
Draws vertical and horizontal lines in canvas.
We do this to get a visual representation of grid in canvas.
"""
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
