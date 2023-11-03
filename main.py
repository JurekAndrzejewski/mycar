import pygame
from datetime import datetime
import paho.mqtt.client as mqttClient
from rpm.rpm import RpmGauge
from pygame import mixer
WIDTH, HEIGHT = 1920, 720  # use your screens display information
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
BG = "images/background.png"
BACKGROUND = pygame.image.load(BG).convert_alpha()
FPS = 60

rightturn_state = False
leftturn_state = False
foglight_state = False
illumination_state = False
highbeam_state = False
radio_state = 0
GO = pygame.USEREVENT + 1
STOP = pygame.USEREVENT + 2
LEFT = pygame.USEREVENT + 3
RIGHT = pygame.USEREVENT + 4
GO_SPEED = pygame.USEREVENT + 5
SLOW_SPEED = pygame.USEREVENT + 6
CLOCK_XY = (555, 620)
RPM_XY = (135, 5)
SPEEDO_XY = (1247, 305)

FONT_MEDIUM = 94    #   Clock, MFA, Fuel size
FONT_LARGE = 174

NEON_YELLOW = (236, 253, 147)   #   Speedo Colour
NEON_GREEN = (145, 213, 89)     #   Lower gauge colours, clock, odo etc
DARK_GREY = (9, 52, 50)         #   background of the digits (for the 7segment appearance)

pygame.init()

clock = pygame.time.Clock()

FONT_PATH = "DSEG7Classic-Bold.ttf"
digital_font = pygame.font.Font(FONT_PATH, FONT_MEDIUM)
font_speedunits = pygame.font.Font(FONT_PATH, FONT_LARGE)
rpm = RpmGauge(RPM_XY, 50)
speed = 0

def draw_clock():
    now = datetime.now()
    bgclock_text = digital_font.render("00:00", True, DARK_GREY)
    WIN.blit(bgclock_text, CLOCK_XY)
    digital_text = now.strftime('%H:%M')
    text = digital_font.render(digital_text, True, NEON_GREEN)
    WIN.blit(text, CLOCK_XY)

def draw_indicators():
    
    if leftturn_state == True:
        WIN.blit(pygame.image.load('images/leftturnOn.png'), (605, 460))
    elif leftturn_state == False:
        WIN.blit(pygame.image.load('images/leftturnOff.png'), (605, 460))
    
    if rightturn_state == True:
        WIN.blit(pygame.image.load('images/rightturnOn.png'), (1220, 460))
    elif rightturn_state == False:
        WIN.blit(pygame.image.load('images/rightturnOff.png'), (1220, 460))
    
    if illumination_state == True:
        WIN.blit(pygame.image.load('images/illuminationOn.png'), (45, 460))
    elif illumination_state == False:
        WIN.blit(pygame.image.load('images/illuminationOff.png'), (45, 460))
        
    if foglight_state == True:
        WIN.blit(pygame.image.load('images/foglightOn.png'), (185, 460))
    elif foglight_state == False:
        WIN.blit(pygame.image.load('images/foglightOff.png'), (185, 460))

    if highbeam_state == True:
        WIN.blit(pygame.image.load('images/highbeamOn.png'), (465, 460))
    elif highbeam_state == False:
        WIN.blit(pygame.image.load('images/highbeamOff.png'), (465, 460))

def draw_radio():
    if radio_state == 0:
        WIN.blit(pygame.image.load('images/radio0.png'), (1265, 0))
    elif radio_state == 1:
        WIN.blit(pygame.image.load('images/radio1.png'), (1265, 0))
        #mixer.music.load("songs/song1.mp3")
        #mixer.music.play()
    elif radio_state == 2:
        WIN.blit(pygame.image.load('images/radio2.png'), (1265, 0))
        #mixer.music.load("songs/song2.mp3")
        #mixer.music.play()
    elif radio_state == 3:
        WIN.blit(pygame.image.load('images/radio3.png'), (1265, 0))
        #mixer.music.load("songs/song3.mp3")
        #mixer.music.play()

def draw_speedometer_text():
    speedtext = font_speedunits.render(str(speed), True, NEON_YELLOW)
    text_rect = speedtext.get_rect()
    text_rect.midright = SPEEDO_XY
    WIN.blit(speedtext, text_rect)

def draw_all():
    WIN.blit(BACKGROUND, (0, 0))
    rpm.show(WIN)
    draw_indicators()
    draw_speedometer_text()
    draw_clock()
    draw_radio()

def main():
    global rightturn_state, leftturn_state, speed, illumination_state, foglight_state, highbeam_state, radio_state
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:

                #revometer
                if event.key == pygame.K_w:
                    pygame.time.set_timer(STOP, 0)
                    pygame.time.set_timer(GO, 300)
                    
                    pygame.time.set_timer(SLOW_SPEED, 0)
                    pygame.time.set_timer(GO_SPEED, 100)
                    
                if event.key == pygame.K_s:
                    pygame.time.set_timer(GO, 0)
                    pygame.time.set_timer(STOP, 200)
                    pygame.time.set_timer(GO_SPEED, 0)
                    pygame.time.set_timer(SLOW_SPEED, 50)

                # turn signals
                if event.key == pygame.K_LEFTBRACKET:
                    pygame.time.set_timer(RIGHT, 0)
                    pygame.time.set_timer(LEFT, 500)
                if event.key == pygame.K_RIGHTBRACKET:
                    pygame.time.set_timer(LEFT, 0)
                    pygame.time.set_timer(RIGHT, 500)

                if event.key == pygame.K_j:
                    illumination_state = True if illumination_state == False else False
                if event.key == pygame.K_k:
                    highbeam_state = True if highbeam_state == False else False
                if event.key == pygame.K_l:
                    foglight_state = True if foglight_state == False else False

                if event.key == pygame.K_0:
                    radio_state = 0
                if event.key == pygame.K_1:
                    radio_state = 1
                if event.key == pygame.K_2:
                    radio_state = 2
                if event.key == pygame.K_3:
                    radio_state = 3

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:

                    pygame.time.set_timer(GO, 0)
                    pygame.time.set_timer(STOP, 600)
                    pygame.time.set_timer(GO_SPEED, 0)
                    pygame.time.set_timer(SLOW_SPEED, 200)

                if event.key == pygame.K_s:
                    pygame.time.set_timer(GO, 0)
                    pygame.time.set_timer(STOP, 450)

                    pygame.time.set_timer(GO_SPEED, 0)
                    pygame.time.set_timer(SLOW_SPEED, 150)
            elif event.type == GO:
                rpm.change(1)
                speed += 1
            elif event.type == STOP:
                rpm.change(2)
            elif event.type == SLOW_SPEED:
                if speed > 0:
                    speed -= 1
            elif event.type == GO_SPEED:
                if speed < 120:
                    speed += 1
            elif event.type == LEFT:
                rightturn_state = False
                leftturn_state = True if leftturn_state == False else False
            elif event.type == RIGHT:
                leftturn_state = False
                rightturn_state = True if rightturn_state == False else False
        draw_all()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()