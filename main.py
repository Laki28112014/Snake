from tkinter import *
from time import sleep
from PIL import Image, ImageTk
from random import randint

# Spielfenster wird erstellt, Höhe: 550, Breite: 500, Hintergrundfarbe: beige, Fenstertitel: Snake
window = Tk()
window.title("Snake")
c = Canvas(window, width=700, height=750, bg='beige')
c.pack()

# Laenge des Spielfeldes wird definiert
spielfeldLaenge = 33

#Anzahl der Koerperteile, welche die Schlange am Anfang des Spiels hat
koerperteileAmAnfang = 1

xAchseLinks = 20
yAchseOben = 50
xAchseRechts = xAchseLinks + 20 * spielfeldLaenge
yAchseUnten = yAchseOben + 20 * spielfeldLaenge

# hier wird definiert, an welcher Position sich die Schlange befindet, wenn das Spiel gestartet wird
anfangsPosition = [xAchseLinks + spielfeldLaenge * 0.5 + 20 // 2 * spielfeldLaenge,
                   yAchseOben + spielfeldLaenge * 0.5 + 20 // 2 * spielfeldLaenge]

# die Spielfeldbegrenzung wird erstellt, die Störke der Linie ist 1
c.create_line(xAchseLinks, yAchseUnten, xAchseLinks, yAchseOben, width=1)
c.create_line(xAchseRechts, yAchseUnten, xAchseRechts, yAchseOben, width=1)
c.create_line(xAchseLinks, yAchseOben, xAchseRechts, yAchseOben, width=1)
c.create_line(xAchseLinks, yAchseUnten, xAchseRechts, yAchseUnten, width=1)

# Das Bild fuer die Schlange wird geladen
snakeImage = Image.open("snake.png")
snakeImage = snakeImage.resize((spielfeldLaenge, spielfeldLaenge), Image.LANCZOS)
snakeImage = ImageTk.PhotoImage(snakeImage)

# Das Bild fuer das Futter (Banane) wird geladen
foodImage = Image.open("banana.png")
foodImage = foodImage.resize((spielfeldLaenge, spielfeldLaenge), Image.LANCZOS)
foodImage = ImageTk.PhotoImage(foodImage)
banana = None

koerperteile = []

# Die Bewegung der Schlange
def snakeMoving():
    snakePosition[0] += direction[0] * spielfeldLaenge
    snakePosition[1] += direction[1] * spielfeldLaenge

# Ein neuer Schlangenkoerper wird erstellt
def generateNewSnake():
    koerperteile.append(c.create_image(snakePosition[0], snakePosition[1], image=snakeImage))

# Die Richtung der Schlange kann mittels Pfeiltasten geaendert werden
def changeDirection(event):
    global direction
    if event.keysym == "Up":
        if direction != (0, 1):
            direction = (0, -1)
    elif event.keysym == "Down":
        if direction != (0, -1):
            direction = (0, 1)
    elif event.keysym == "Left":
        if direction != (1, 0):
            direction = (-1, 0)
    elif event.keysym == "Right":
        if direction != (-1, 0):
            direction = (1, 0)


c.bind_all("<Key>", changeDirection)

# Der letzte Koerperteil der Schlange wird aus dem Spielfeld entfernt, wenn die Schlange vorne einen neuen Koerperteil dazubekommt
def letzteSchlangeLoeschen():
    if len(koerperteile) > koerper1:
        c.delete(koerperteile.pop(0))

# wenn die Schlange das Spielfeld verlaesst, dann wird das Spiel neu gestartet und die Schlange kehrt in die Ausgangsposition mit der Laenge 1 zurueck
def spielfeldVerlassen():
    return snakePosition[0] < xAchseLinks or snakePosition[0] > xAchseRechts or snakePosition[1] > yAchseUnten or snakePosition[1] < yAchseOben

# hier wird geprueft, ob die Schlange sich selbst beisst, falls dies der Fall ist kehrt die Schlange zurueck in die Ausgangsposition mit der Laenge 1
def KopfBeisstInSchlange():
    for body in koerperteile:
        x, y = c.coords(body)
        if snakePosition[0] == x and snakePosition[1] == y:
            return True
    return False

# hier wird das Futter-Image irgendwo im Spielfeld platziert
def randomFoodPosition():
    while True:
        banana = [xAchseLinks + spielfeldLaenge * 0.5 + randint(0, 20 - 1) * spielfeldLaenge,
                     yAchseOben + spielfeldLaenge * 0.5 + randint(0, 20 - 1) * spielfeldLaenge]
        banana_valid = True
        for koerper in koerperteile:
            x, y = c.coords(koerper)
            if x == banana[0] and y == banana[1]:
                banana_valid = False
        if banana_valid:
            return banana

# die Schlange isst eine Banane
def snakeEatsBanana():
    return snakePosition[0] == bananaPosition[0] and snakePosition[1] == bananaPosition[1]

# wenn die Banane gegessen wird, dann wird eine neue Banane an einer Random Stelle platziert
def generateNewBanana():
    global banana
    if banana is not None:
        c.delete(banana)
    banana = c.create_image(bananaPosition[0], bananaPosition[1], image=foodImage)


while True:
    koerper1 = koerperteileAmAnfang
    direction = (1, 0)
    snakePosition = list(anfangsPosition)
    bananaPosition = randomFoodPosition()
    generateNewBanana()
    for koerper in koerperteile:
        c.delete(koerper)
    koerperteile = []
    while True:
        snakeMoving()
        if KopfBeisstInSchlange():
            break
        generateNewSnake()
        letzteSchlangeLoeschen()
        if snakeEatsBanana():
            bananaPosition = randomFoodPosition()
            generateNewBanana()
            koerper1 += 1
        if spielfeldVerlassen():
            break
        window.update()
        sleep(0.2)
