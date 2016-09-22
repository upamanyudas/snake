# Snake Game

import random, pygame, sys
from pygame.locals import *

FPS = 8 #Speed of the Snake
WINDOWWIDTH = 320
WINDOWHEIGHT = 240
CELLSIZE = 12
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GRAY = (166, 166, 166)
DARKGRAY = (80, 80, 80)
BGCOLOR = WHITE

pygame.mixer.init()

eat = pygame.mixer.Sound('audio/eat.wav')
eat.set_volume(0.10)

gameover = pygame.mixer.Sound('audio/gameover.wav')
gameover.set_volume(0.10)

pygame.mixer.music.load('audio/theme.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.05)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('8BIT.ttf', 13)
    pygame.display.set_caption('Snake')

    pygame.display.set_icon(pygame.image.load('icon.bmp'))

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoords = [{'x': startx, 'y': starty},
                   {'x': startx - 1, 'y': starty},
                   {'x': startx - 2, 'y': starty}]

    direction = RIGHT

    food = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLWIDTH:
            return
        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                return

        if snakeCoords[HEAD]['x'] == food['x'] and snakeCoords[HEAD]['y'] == food['y']:
            food = getRandomLocation()
            eat.play()
        else:
            del snakeCoords[-1]

        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}

        snakeCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)

        drawSnake(snakeCoords)
        drawFood(food)
        drawScore (len(snakeCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, BLACK, snakeSegmentRect)

def drawFood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLACK, foodRect)

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def drawScore(score):
    scoreSurf = BASICFONT.render('Score %s' % (score), True, GRAY)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play', True, BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 285, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showStartScreen():
    titleFont = pygame.font.Font('8BIT.ttf', 40)
    titleSurf1 = titleFont.render('Snake', True, WHITE, DARKGRAY)
    titleSurf2 = titleFont.render('Snake', True, GRAY)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

def showGameOverScreen():
    gameOverFont = pygame.font.Font('8BIT.ttf', 30)
    gameSurf = gameOverFont.render('Game', True, BLACK)
    overSurf = gameOverFont.render('Over', True, BLACK)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 50)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 50)
    pygame.mixer.music.stop()
    gameover.play()

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

if __name__ == '__main__':
    main()
