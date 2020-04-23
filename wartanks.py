"""--------------------------War Tanks----------------------------
objetive: Give a bullet to one of the enemy tanks, only giving
the initial velocity and the shooting angle of our tank. Also,
the user can decide the number of enemy tanks in a range of
1 to 40. The shooting angle is delimited from 0 to 90 degrees.
The velocity cannot be negative and it has to have meters/seconds
units.

by Edwin Marcelo Vasconez Lopez
Student of Physics
"""
# ----------------------------------------------------------------
# LIBRARIES
# -------------------
import tkinter as tk
import random as rm
import numpy as np

# CONSTANTS
# -------------------------------------------------
# Physics
# ---------------------------------
G = 9.8         # Gravity on Earth
DT = 0.01       # Variation of time

# Tkinter
# -------------------------------------------------
WIDTH = 800
HEIGHT = 500
EDGE = 20
WIDTHTANK = 65
HEIGHTANK = 50
WIDTHBALL = 15
BALLX0 = 0 + EDGE + WIDTHTANK
BALLY0 = HEIGHT - EDGE - 2*HEIGHTANK//3
BALLX1 = BALLX0 + WIDTHBALL
BALLY1 = BALLY0 - WIDTHBALL
LIMX = WIDTH - WIDTHBALL - 2*EDGE - WIDTHTANK
LIMY = HEIGHT - WIDTHBALL - 2*EDGE - 2*HEIGHTANK//3

# ----------------------------FUNCTIONS-------------------------------------
# ---------------------------------------------------------------------------


def verifynumetanks():
    """verifynumtanks: Verifies that the number of enemies
    is correct.
    Returns:
        num(int): Number of enemies
    """
    check = False
    while check is False:
        num = int(input("Number of enemies:"))
        if num >= 1 and num <= 40:
            check = True
        else:
            print("Number of enemies from 1 to 40")
    return num


def elements_list(listado):
    """elments_list: Gives each factor of a 4 elements list
    or tuple.
    Args:
        listado(list,tuple): 4 elements
    Returns:
        posx1,posy1,posx2,posy2(int): Position in the canvas
    """
    posx1 = listado[0]
    posy1 = listado[1]
    posx2 = listado[2]
    posy2 = listado[3]
    return posx1, posy1, posx2, posy2


def solapamiento(enemy1, enemy2, space):
    """solapamiento: Calculate the distance between to points to
    avoid overlaping between enemy tanks.
    Args:
        enemy1,enemy2(tuple): Position x1, x2, y1, and, y2 of tanks
        space(int): Distance for separate the 2 tanks
    Returns:
        (bool): True = no overlap, False = overlap
    """
    distance = (((enemy2[0] - enemy1[0])**2) + ((enemy2[1]-enemy1[1])**2))**0.5
    return space > abs(distance)


def position_enemies(number, board):
    """position_enemies: Gives the position in the canvas of each
    enemy tank
    Args:
        number(int): Number of tanks
        board: Name of the canvas
    Returns:
        lista1(list): position x1, x2, y1, and, y2 of tanks
    """
    lista1 = []
    cont = 0
    for cont in range(number):
        lista1.append(board.bbox('etank'+str(cont)))
    return lista1


def changedegree(angle):
    """grados: Degrees to Radians
    Args:
        angle(bool): Shooting angle in degrees
    Returns:
        (bool): Shooting angle in radians
    """
    return (angle*np.pi)/180


def verifyangle():
    """verifyangle: Verifies that the range of the angle
    is correct.
    Returns:
        angle(float): Correct angle in radians
    """
    check = False
    while check is False:
        angle = float(input("Shooting angle in degrees:"))
        if angle >= 0 and angle <= 90:
            angle = changedegree(angle)
            check = True
        else:
            print("Shooting angle in degrees from 0 to 90")
    return angle


def verifyinivelocity():
    """verifyinivelocity: Verifies that the range of the initial
    velocity is correct.
    Returns:
        velocity(float): Correct velocity
    """
    check = False
    while check is False:
        velocity = float(input("Initial velocity of the bullet in m/s:"))
        if velocity > 0:
            check = True
        else:
            print("Initial velocity must be greater than 0")
    return velocity


def parabolicmotion():
    """parabolicmotion: Calculates some important data for the analysis of
    the parabolic motion.
    Returns:
        lista(list): Flight time, initial velocity in x and y
    """
    teta = verifyangle()
    v_ini = verifyinivelocity()
    # Components in x and y of  the initial velocity
    v_inix = v_ini*np.cos(teta)
    v_iniy = v_ini*np.sin(teta)
    # Flight time
    tmax = (2*v_iniy)/G
    lista = [tmax, v_inix, v_iniy]
    return lista


def colision(tup1, tup2, con, photo, board):
    """colision: Proofs that there is or not a colision between the
    ball and an enemy tank.
    Args:
        tup1,tup2(tuple): Tuples with the positions of the ball and the tank
        con(bool): True = no colision
        photo: Variable name of the photo for colision
        board: Name of the canvas
    Returns
        con(bool): True = no colision, False = colision
    """
    xball1, yball1, xball2, yball2 = elements_list(tup1)
    xtank1, ytank1, xtank2, ytank2 = elements_list(tup2)
    if ytank1 == yball2:
        conta = xtank1
        for conta in range(xtank1, xtank2):
            if conta == xball1 or conta == xball2:
                createxplosiont((xtank1, ytank1), photo, board)
                con = False
    elif xtank1 == xball2:
        conta = ytank1
        for conta in range(ytank1, ytank2):
            if conta == yball1 or conta == yball2:
                createxplosiont((xtank1, ytank1), photo, board)
                con = False
    elif yball1 == ytank2:
        conta = xtank1
        for conta in range(xtank1, xtank2):
            if conta == xball1 or conta == xball2:
                createxplosiont((xtank1, ytank1), photo, board)
                con = False
    return con


def col(lista, tup, con, photo, board):
    """col: Proofs that there is or not a colision between the
    ball and someone of the enemy tanks.
    Args:
        lista(list): Contains the positions of all the tanks
        tup(tuple): Tuple with the positions of the ball
        con(bool): True = no colision
        photo: Variable name of the photo for colision
        board: Name of the canvas
    Returns
        con(bool): True = no colision, False = colision
    """
    for cont in lista:
        con = colision(tup, cont, con, photo, board)
        if con is False:
            lista.remove(cont)
            break
    return con

# -----------------------------METHODS------------------------------------
# -------------------------------------------------------------------------


def creaimagen(photo, board):
    """creaimagen: Creates images in the canvas
    Args:
        photo: Name of the photo
        board: Canvas name
    """
    board.create_image(WIDTH//2, HEIGHT//2, image=photo)


def createedges(tup, board):
    """createedges: Creates the edges of the panel.
    Args:
        tup(tuple): Contains positions x1, x2, y1, and, y2
        board: Canvas name
    """
    posx1, posy1, posx2, posy2 = elements_list(tup)
    board.create_rectangle(posx1, posy1, posx2, posy2, fill="cornsilk4")


def createball(tup, name, board):
    """createball: Creates the ball or bullet.
    Args:
        tup(tuple): Contains positions x1, x2, y1, and, y2
        name(str): Identifier of the ball
        board: Canvas name
    """
    posx1, posy1, posx2, posy2 = elements_list(tup)
    board.create_oval(posx1, posy1, posx2, posy2, fill="black", tag=name)


def createtank(tup, name, photo, board):
    """createtank: Creates tanks friends or enemies
    Args:
        tup(tuple): Contains positions x1, x2, y1, and, y2
        name(str): Identifier of the tank
        photo: Variable name of the photo of tanks
        board: Canvas name
    """
    posx = tup[0]
    posy = tup[1]
    board.create_image(posx, posy, image=photo, tag=name)


def crea_enemytanks(number, pos1, photo, board):
    """crea_enemytanks: Creates all enemies in random positions
    Args:
        number(int): Number of enemy tanks
        pos1(int): Initial position of the ball
        photo: Variable name of the photo of tanks
    """
    espaciado = 65
    lista = []
    while len(lista) < number:
        posxi = rm.randint(pos1 + 33, WIDTH - 20 - 33)
        posyi = rm.randint(20 + 35, HEIGHT - 20 - 25)
        enemy = (posxi, posyi)
        if not any(solapamiento(enemy, e, espaciado) for e in lista):
            lista.append(enemy)
            for cont in lista:
                posxf = cont[0]
                posyf = cont[1]
                createtank((posxf, posyf), 'etank'+str(lista.index(cont)),
                           photo, board)


def edgeenemy(lista1, board):
    """edgeenemy: Creates a rectangle around the enemies.
    Args:
        lista1(list): List with all the position of the enemies
        board: Canvas name
    """
    for cont in lista1:
        xtank1, ytank1, xtank2, ytank2 = elements_list(cont)
        board.create_rectangle(xtank1, ytank1, xtank2, ytank2)


def createxplosiont(tup, photo, board):
    """createxplosion: Creates the explosion in the canvas.
    Args:
        tup(tuple): Initial positions for the tank under attack
        photo: Variable name of the photo of colision
        board: Canvas name
    """
    posx = tup[0]
    posy = tup[1]
    board.create_image(posx + WIDTHTANK//2, posy + HEIGHTANK//2, image=photo)


def createxplosione(tup, photo, board):
    """createxplosion: Creates the explosion in the canvas.
    Args:
        tup(tuple): Initial positions for the tank under attack
        photo: Variable name of the photo of colision
        board: Canvas name
    """
    posx = tup[0]
    posy = tup[1]
    board.create_image(posx + WIDTHBALL//2, posy + WIDTHBALL//2, image=photo)


def ballmovement(lista, photo, board, enemy_number, i):
    """ballmovement: Moves the ball around the canvas until a colision.
    Args:
        lista(list): List of enemies
        photo: Variable name for the photo of the tanks
        board: Canvas name
    """
    datmov = parabolicmotion()

    keep = True
    time = 0.0
    xnew = 0.0
    ynew = 0.0
    checkx = 0
    checky = 0
    yold = 0
    xold = 0

    while keep:
        if time <= datmov[0] and checkx <= LIMX and checky <= LIMY:
            xnew = datmov[1]*time
            deltax = xnew - xold
            xold = xnew
            ynew = datmov[2]*time - (0.5*G*time*time)
            deltay = ynew - yold
            yold = ynew
            board.move('ball'+str(i), deltax, -deltay)        # Ball movement
            checkx += deltax
            checky += deltay
            board.after(3)
            board.update()
            time = time + DT
            tup = board.bbox('ball'+str(i))
            keep = col(lista, tup, keep, photo, board)
            if keep is False:
                enemy_number = enemy_number - 1

        else:
            createxplosione(tup, photo, board)
            keep = False
    return enemy_number
# ----------------------------MAIN---------------------------------
# -----------------------------------------------------------------


def main():
    """main: Principal part of the program"""


    # Create the graphic interface and define the photo variables
    window = tk.Tk()
    window.title("War Tanks")
    panel = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    panel.config(background='khaki1')
    photofondo = tk.PhotoImage(file='fondo2.png')
    photomon = tk.PhotoImage(file='mon2.png')
    photo1 = tk.PhotoImage(file='tankwar.png')
    photo2 = tk.PhotoImage(file='etank.png')
    photo3 = tk.PhotoImage(file='bomba2.png')
    photo4 = tk.PhotoImage(file='win.png')
    photo5 = tk.PhotoImage(file='loser.png')
    boton = tk.Button(text='Exit', command=quit)
    panel.pack()
    boton.pack()
    # Create the canvas enviorement
    creaimagen(photofondo, panel)
    creaimagen(photomon, panel)

    # Create each one of the edges of the panel
    # Left
    createedges((0, 0, EDGE, HEIGHT - EDGE), panel)
    # Top
    createedges((EDGE, 0, WIDTH, EDGE), panel)
    # Right
    createedges((WIDTH - EDGE, EDGE, WIDTH, HEIGHT), panel)
    # Down
    createedges((0, HEIGHT - EDGE, WIDTH - EDGE, HEIGHT), panel)

    # Create the friend tank
    createtank((EDGE + WIDTHTANK//2, HEIGHT - EDGE - HEIGHTANK//2),
               'ftank', photo1, panel)

    # Define the number of enemy tanks
    enemy_number = verifynumetanks()
    tiros = enemy_number + 3

    # Create the enemy tanks and their contour
    crea_enemytanks(enemy_number, BALLX1, photo2, panel)
    l_postank = position_enemies(enemy_number, panel)
    edgeenemy(l_postank, panel)

    i = 0
    while i < tiros and enemy_number > 0:
        # Create the bullet
        createball((BALLX0, BALLY0, BALLX1, BALLY1), 'ball'+str(i), panel)
        # Move the ball until colision
        enemy_number = ballmovement(l_postank, photo3, panel, enemy_number, i)
        i += 1
    if enemy_number == 0:
        creaimagen(photo4, panel)
    else:
        creaimagen(photo5, panel)

    window.mainloop()

if __name__ == '__main__':
    main()
