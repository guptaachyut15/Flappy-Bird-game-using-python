import random
import os
import sys
import pygame
from pygame.locals import *
os.chdir("D:\\pythonProject2\\flappy bird game")

# Global Varables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode(size=(SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_AUDIO = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['bird'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = 0
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on close button or escape key close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses space of up key start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['bird'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()
    # list of upper pipes
    UpperPipes = [{"x": SCREENWIDTH+200, "y": newpipe1[0]["y"]},
                  {"x": SCREENWIDTH+200+(SCREENWIDTH/2), "y": newpipe2[0]["y"]}]
    # list for lower pipes
    LowerPipes = [{"x": SCREENWIDTH+200, "y": newpipe1[1]["y"]},
                  {"x": SCREENWIDTH+200+(SCREENWIDTH/2), "y": newpipe2[1]["y"]}]
    pipex = -4
    playervely = -9
    playermaxvel = 10
    playerminvel = -8
    playeraccy = 1

    playerflapvely = -8
    playerflapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerflapped = True
                    playervely = playerflapvely
                    GAME_AUDIO['wing'].play()
        # This function will return whether the player has collided or not
        crashtest = iscollide(playerx, playery, UpperPipes, LowerPipes)
        if crashtest:
            return
        # Check for score
        playermidpos = playerx+(GAME_SPRITES['bird'].get_width()/2)
        for pipe in UpperPipes:
            pipemidpos = pipe['x']+(GAME_SPRITES['pipe'][0].get_width()/2)
            if pipemidpos <= playermidpos < pipemidpos+4:
                score += 1
                print(f"Your score is {score}")
                GAME_AUDIO['point'].play()
        if playervely < playermaxvel and not playerflapped:
            playervely += playeraccy
        if playerflapped:
            playerflapped = False
        playerheight = GAME_SPRITES['bird'].get_height()
        playery = playery+min(playervely, GROUNDY-playerheight-playery)
        # Moving pipes to the left
        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            upperpipe["x"] += pipex
            lowerpipe["x"] += pipex
        # Add a new pipe when the left most pipe is about to get out of the screen
        if 0 < UpperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            UpperPipes.append(newpipe[0])
            LowerPipes.append(newpipe[1])
        # Remove the  pipe once it goes out of the screen
        if UpperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            UpperPipes.pop(0)
            LowerPipes.pop(0)
        # Blitting the files
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (upperpipe["x"], upperpipe["y"]))
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (lowerpipe["x"], lowerpipe["y"]))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['bird'], (playerx, playery))
        #Blit the score
        mydigits=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=(SCREENWIDTH-width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def iscollide(playerx,playery,Upperpipes,Lowerpipes):
    if playery<=0 or playery>GROUNDY-25:
        GAME_AUDIO['hit'].play()
        return True
    pheigt=GAME_SPRITES['pipe'][0].get_height()    
    for pipe in Upperpipes:
        if playery<(pheigt+pipe['y']) and (abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()-20):
            GAME_AUDIO['hit'].play()
            return True
        
    for pipe in Lowerpipes:
        if (playery+GAME_SPRITES['bird'].get_height()>pipe['y']) and (abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()-20):
            GAME_AUDIO['hit'].play()
            return True
    return False    


def getRandomPipe():
    """Gives location of 2 random pipes one rotated and one straight"""
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    # y2 = offset+random.randrange(0, int(SCREENHEIGHT)) - (int(GAME_SPRITES['base'].get_height())-(1.2*offset))
    y2 = offset+random.randrange(0, (int(SCREENHEIGHT)-int(GAME_SPRITES['base'].get_height())-int((1.2*offset))))
    # pipex = SCREENWIDTH+10
    pipex = SCREENWIDTH+25
    # y1 = pipeheight-y2+offset
    y1 = pipeheight-y2+int((0.8*offset))
    pipe = [{"x": pipex, "y": -y1},  # For upper pipe
            {"x": pipex, "y": y2}]  # For lower pipe
    return pipe


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()  # To keep in check the max FPS
    pygame.display.set_caption("Flappy Bird Game Project 2")
    # UPLOADING SPRITES
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(), pygame.image.load('gallery/sprites/1.png').convert_alpha(), pygame.image.load('gallery/sprites/2.png').convert_alpha(), pygame.image.load('gallery/sprites/3.png').convert_alpha(), pygame.image.load('gallery/sprites/4.png').convert_alpha(
        ), pygame.image.load('gallery/sprites/5.png').convert_alpha(), pygame.image.load('gallery/sprites/6.png').convert_alpha(), pygame.image.load('gallery/sprites/7.png').convert_alpha(), pygame.image.load('gallery/sprites/8.png').convert_alpha(), pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'gallery/sprites/message2.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.image.load(PIPE).convert_alpha(), pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180)
                            )
    GAME_SPRITES['base'] = pygame.image.load(
        'gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['bird'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()

    # UPLOADING AUDIO
    GAME_AUDIO['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_AUDIO['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    while True:
        welcomeScreen()
        mainGame()
