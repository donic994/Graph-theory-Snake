from tkinter import*
from random import randint
import constants as CON
import turtle
import numpy as np
import dijkstra
import networkx as nx
import matplotlib.pyplot as plt

"""
MMMMMMMM               MMMMMMMM               AAA               TTTTTTTTTTTTTTTTTTTTTTTHHHHHHHHH     HHHHHHHHH
M:::::::M             M:::::::M              A:::A              T:::::::::::::::::::::TH:::::::H     H:::::::H
M::::::::M           M::::::::M             A:::::A             T:::::::::::::::::::::TH:::::::H     H:::::::H
M:::::::::M         M:::::::::M            A:::::::A            T:::::TT:::::::TT:::::THH::::::H     H::::::HH
M::::::::::M       M::::::::::M           A:::::::::A           TTTTTT  T:::::T  TTTTTT  H:::::H     H:::::H
M:::::::::::M     M:::::::::::M          A:::::A:::::A                  T:::::T          H:::::H     H:::::H
M:::::::M::::M   M::::M:::::::M         A:::::A A:::::A                 T:::::T          H::::::HHHHH::::::H
M::::::M M::::M M::::M M::::::M        A:::::A   A:::::A                T:::::T          H:::::::::::::::::H
M::::::M  M::::M::::M  M::::::M       A:::::A     A:::::A               T:::::T          H:::::::::::::::::H
M::::::M   M:::::::M   M::::::M      A:::::AAAAAAAAA:::::A              T:::::T          H::::::HHHHH::::::H
M::::::M    M:::::M    M::::::M     A:::::::::::::::::::::A             T:::::T          H:::::H     H:::::H
M::::::M     MMMMM     M::::::M    A:::::AAAAAAAAAAAAA:::::A            T:::::T          H:::::H     H:::::H
M::::::M               M::::::M   A:::::A             A:::::A         TT:::::::TT      HH::::::H     H::::::HH
M::::::M               M::::::M  A:::::A               A:::::A        T:::::::::T      H:::::::H     H:::::::H
M::::::M               M::::::M A:::::A                 A:::::A       T:::::::::T      H:::::::H     H:::::::H
MMMMMMMM               MMMMMMMMAAAAAAA                   AAAAAAA      TTTTTTTTTTT      HHHHHHHHH     HHHHHHHHH
"""

graph = dijkstra.Graph([])
Matrix = [[dijkstra.inf for x in range(CON.CELLS)] for y in range(CON.CELLS)]


def InitializeMatrix():

    for i in range(CON.CELLS):
        for j in range(CON.CELLS):
            if(i == j):
                Matrix[i][j] = 0
        print(Matrix[i])

    FillGraph()


def FillGraph():
    for i in range(CON.CELLS):
        for j in range(CON.CELLS):
            if((j*CON.CELLS)+(i-1)) >= 0 and ((j*CON.CELLS)+(i-1))<15:
                graph.add_edge((j*CON.CELLS)+i, (j*CON.CELLS)+(i-1))
            if((j*CON.CELLS)+(i+1)) <= pow(CON.CELLS, 2):
                graph.add_edge((j*CON.CELLS)+i, (j*CON.CELLS)+(i+1))
            if (((j-1)*CON.CELLS)+(i)) >= 0  and ((j*CON.CELLS)+(i-1))<15:
                graph.add_edge((j*CON.CELLS)+i, ((j-1)*CON.CELLS)+(i))
            if(((j+1)*CON.CELLS)+(i)) <= pow(CON.CELLS, 2):
                graph.add_edge((j*CON.CELLS)+i, ((j+1)*CON.CELLS)+(i))

    print(graph.edges)

    # nx.draw(graph)
    # plt.savefig("paths_graph.png")


"""
   SSSSSSSSSSSSSSS NNNNNNNN        NNNNNNNN               AAA               KKKKKKKKK    KKKKKKKEEEEEEEEEEEEEEEEEEEEEE
 SS:::::::::::::::SN:::::::N       N::::::N              A:::A              K:::::::K    K:::::KE::::::::::::::::::::E
S:::::SSSSSS::::::SN::::::::N      N::::::N             A:::::A             K:::::::K    K:::::KE::::::::::::::::::::E
S:::::S     SSSSSSSN:::::::::N     N::::::N            A:::::::A            K:::::::K   K::::::KEE::::::EEEEEEEEE::::E
S:::::S            N::::::::::N    N::::::N           A:::::::::A           KK::::::K  K:::::KKK  E:::::E       EEEEEE
S:::::S            N:::::::::::N   N::::::N          A:::::A:::::A            K:::::K K:::::K     E:::::E
 S::::SSSS         N:::::::N::::N  N::::::N         A:::::A A:::::A           K::::::K:::::K      E::::::EEEEEEEEEE
  SS::::::SSSSS    N::::::N N::::N N::::::N        A:::::A   A:::::A          K:::::::::::K       E:::::::::::::::E
    SSS::::::::SS  N::::::N  N::::N:::::::N       A:::::A     A:::::A         K:::::::::::K       E:::::::::::::::E
       SSSSSS::::S N::::::N   N:::::::::::N      A:::::AAAAAAAAA:::::A        K::::::K:::::K      E::::::EEEEEEEEEE
            S:::::SN::::::N    N::::::::::N     A:::::::::::::::::::::A       K:::::K K:::::K     E:::::E
            S:::::SN::::::N     N:::::::::N    A:::::AAAAAAAAAAAAA:::::A    KK::::::K  K:::::KKK  E:::::E       EEEEEE
SSSSSSS     S:::::SN::::::N      N::::::::N   A:::::A             A:::::A   K:::::::K   K::::::KEE::::::EEEEEEEE:::::E
S::::::SSSSSS:::::SN::::::N       N:::::::N  A:::::A               A:::::A  K:::::::K    K:::::KE::::::::::::::::::::E
S:::::::::::::::SS N::::::N        N::::::N A:::::A                 A:::::A K:::::::K    K:::::KE::::::::::::::::::::E
 SSSSSSSSSSSSSSS   NNNNNNNN         NNNNNNNAAAAAAA                   AAAAAAAKKKKKKKKK    KKKKKKKEEEEEEEEEEEEEEEEEEEEEE
 """


class Master(Canvas):
    """create the game canvas, the snake, the obstacle, keep track of the score"""

    def __init__(self, boss=None):
        super().__init__(boss)
        self.configure(width=CON.WD, height=CON.HT, bg=CON.BG_COLOR)
        self.running = 0
        self.snake = None
        self.obstacle1 = None
        self.obstacle2 = None
        self.direction = None
        self.current = None
        self.score = Scores(boss)

    def start(self):
        """start snake game"""
        if self.running == 0:
            self.snake = Snake(self)
            self.obstacle1 = Obstacle(self)
            self.obstacle2 = Obstacle(self)
            self.direction = CON.LEFT
            self.current = Movement(self, CON.LEFT)
            self.current.begin()
            self.running = 1

    def clean(self):
        """restarting the game"""
        if self.running == 1:
            self.score.reset()
            self.current.stop()
            self.running = 0
            self.obstacle1.delete()
            self.obstacle2.delete()
            for block in self.snake.blocks:
                block.delete()

    def redirect(self, event):
        """taking keyboard inputs and moving the snake accordingly"""
        if self.running == 1 and \
                event.keysym in CON.AXES.keys() and\
                CON.AXES[event.keysym] != CON.AXES[self.direction]:
            self.current.flag = 0
            self.direction = event.keysym
            # a new instance at each turn to avoid confusion/tricking
            self.current = Movement(self, event.keysym)
            # program gets tricked if the user presses two arrow keys really quickly
            self.current.begin()


class Scores:
    """Objects that keep track of the score and high score"""

    def __init__(self, boss=None):
        self.counter = StringVar(boss, '0')
        self.maximum = StringVar(boss, '0')

    def increment(self):
        score = int(self.counter.get()) + 1
        maximum = max(score, int(self.maximum.get()))
        self.counter.set(str(score))
        self.maximum.set(str(maximum))

    def reset(self):
        self.counter.set('0')


class Shape:
    """This is a template to make obstacles and snake body parts"""

    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        if kind == CON.SN:
            self.ref = Canvas.create_rectangle(self.can,
                                               a - CON.SN_SIZE, b - CON.SN_SIZE,
                                               a + CON.SN_SIZE, b + CON.SN_SIZE,
                                               fill=CON.SN_COLOR,
                                               width=2)
        elif kind == CON.OB:
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


class Obstacle(Shape):
    """snake food"""

    def __init__(self, can):
        """only create the obstacles where there is no snake body part"""
        self.can = can

        p = int(CON.GRADUATION/2 - 1)
        n, m = randint(0, p), randint(0, p)
        a, b = CON.PIXEL * (2 * n + 1), CON.PIXEL * (2 * m + 1)
        while [a, b] in [[block.x, block.y] for block in self.can.snake.blocks]:
            n, m = randint(0, p), randint(0, p)
            a, b = CON.PIXEL * (2 * n + 1), CON.PIXEL * (2 * m + 1)
        super().__init__(can, a, b, CON.OB)


class BlockSnake(Shape):
    """snake body part"""

    def __init__(self, can, a, y):
        super().__init__(can, a, y, CON.SN)


class Snake:
    """a snake keeps track of its body parts"""

    def __init__(self, can):
        """initial position"""
        self.can = can
        a = CON.WD/2
        self.blocks = [BlockSnake(can, a, a), BlockSnake(can, a, a), BlockSnake(can, a, a), BlockSnake(
            can, a, a), BlockSnake(can, a, a), BlockSnake(can, a, a), BlockSnake(can, a, a)]

    def move(self, path):
        """an elementary step consisting of putting the tail of the snake in the first position"""
        a = self.blocks[-1].x + CON.STEP * path[0]
        b = self.blocks[-1].y + CON.STEP * path[1]
        if (self.can.obstacle1 == None and self.can.obstacle2 == None):
            self.can.clean()
        elif (a == self.can.obstacle1.x and b == self.can.obstacle1.y):  # check if we find food 1
            self.can.score.increment()
            self.can.obstacle1.delete()
            moveHead(self, a, b)
            # self.blocks.append(Block(self.can, a, b))
            # self.can.obstacle = Obstacle(self.can)
        elif (a == self.can.obstacle2.x and b == self.can.obstacle2.y):
            self.can.score.increment()
            self.can.obstacle2.delete()
            moveHead(self, a, b)
            # self.blocks.append(Block(self.can, a, b))
            # self.can.obstacle = Obstacle(self.can)
        elif [a, b] in [[block.x, block.y] for block in self.blocks]:  # check if we hit a body part
            self.can.clean()
        elif (a == CON.WD + CON.PIXEL or a == - CON.PIXEL or b == CON.HT + CON.PIXEL or b == - CON.PIXEL):  # check if we hit a wall
            self.can.clean()
        else:
            moveHead(self, a, b)


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


def moveHead(self, a, b):
    pathToFood1 = graph.dijkstra(calculateObjectPosition(a, b), calculateObjectPosition(
        self.can.obstacle1.x, self.can.obstacle1.y))
    print("Food 1:" + str(graph.dijkstra(calculateObjectPosition(a, b), calculateObjectPosition(
        self.can.obstacle1.x, self.can.obstacle1.y))))
    pathToFood2 = graph.dijkstra(calculateObjectPosition(a, b), calculateObjectPosition(
        self.can.obstacle2.x, self.can.obstacle2.y))
    print("Food 2:" + str(graph.dijkstra(calculateObjectPosition(a, b), calculateObjectPosition(
        self.can.obstacle2.x, self.can.obstacle2.y))))

    self.blocks[0].modify(a, b)
    self.blocks = self.blocks[1:] + [self.blocks[0]]


class Movement:
    """object that enters the snake into a perpetual state of motion in a predefined direction"""

    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        """start the perpetual motion"""
        if self.flag > 0:
            self.can.snake.move(CON.DIRECTIONS[self.direction])
            self.can.after(CON.REFRESH_TIME, self.begin)

    def stop(self):
        """stop the perpetual movement"""
        self.flag = 0


"""                                       
        GGGGGGGGGGGGG     OOOOOOOOO     
     GGG::::::::::::G   OO:::::::::OO   
   GG:::::::::::::::G OO:::::::::::::OO 
  G:::::GGGGGGGG::::GO:::::::OOO:::::::O
 G:::::G       GGGGGGO::::::O   O::::::O
G:::::G              O:::::O     O:::::O
G:::::G              O:::::O     O:::::O
G:::::G    GGGGGGGGGGO:::::O     O:::::O
G:::::G    G::::::::GO:::::O     O:::::O
G:::::G    GGGGG::::GO:::::O     O:::::O
G:::::G        G::::GO:::::O     O:::::O
 G:::::G       G::::GO::::::O   O::::::O
  G:::::GGGGGGGG::::GO:::::::OOO:::::::O
   GG:::::::::::::::G OO:::::::::::::OO 
     GGG::::::GGG:::G   OO:::::::::OO   
        GGGGGG   GGGG     OOOOOOOOO     
                                   
"""

InitializeMatrix()

root = Tk()
root.title("Snake Game")
game = Master(root)
game.grid(column=1, row=0, rowspan=3)
root.bind("<Key>", game.redirect)
buttons = Frame(root, width=35, height=3*CON.HT/5)
Button(buttons, text='Start', command=game.start).grid()
Button(buttons, text='Stop', command=game.clean).grid()
Button(buttons, text='Quit', command=root.destroy).grid()
buttons.grid(column=0, row=0)
scoreboard = Frame(root, width=35, height=2*CON.HT/5)
Label(scoreboard, text='Game Score').grid()
Label(scoreboard, textvariable=game.score.counter).grid()
Label(scoreboard, text='High Score').grid()
Label(scoreboard, textvariable=game.score.maximum).grid()
scoreboard.grid(column=0, row=2)

root.mainloop()
