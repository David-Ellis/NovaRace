import pygame
import time 
import random
pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
green = (0, 200, 0)
red = (200, 0, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

backgound = (77, 73, 99)

curb = (130, 127, 127)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Nova Race')
clock = pygame.time.Clock()

Logo = pygame.image.load('Logo.png')
Start = pygame.image.load('Start.png')
StartH = pygame.image.load('StartHover.png')
Options = pygame.image.load('Options.png')
OptionsH = pygame.image.load('OptionsHover.png')
Quit = pygame.image.load('Quit.png')
QuitH = pygame.image.load('QuitHover.png')
menuBG = pygame.image.load('menuBG.png')
Music = pygame.image.load('music.png')
MusicH = pygame.image.load('musicHover.png')
Choose = pygame.image.load('Choose.png')
ChooseH = pygame.image.load('ChooseHover.png')    
Return = pygame.image.load('Return.png')
ReturnH = pygame.image.load('ReturnHover.png')  
On = pygame.image.load('On.png')
Off = pygame.image.load('Off.png')

carImg1 = pygame.image.load('Car.png')
carImg2 = pygame.image.load('otherCar1.png')
carImg3 = pygame.image.load('otherCar2.png')
carImg4 = pygame.image.load('otherCar3.png')
carImg = carImg1 # default car image

grassL = pygame.image.load('GrassL.png')
grassR = pygame.image.load('GrassR.png')

carIcon = pygame.image.load('CarIcon.png')
pygame.display.set_icon(carIcon)
car_width = 65
car_height = 111
road_size = 500
grass_width = (display_width-road_size)/2

ding = pygame.mixer.Sound('ding.wav')
crashSound = pygame.mixer.Sound('crash.wav')
clickSound = pygame.mixer.Sound('click.wav')
pygame.mixer.music.load('music.ogg')

paused = False
crashed = False
MusicOn = True

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def things_dodged():
    #global count
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (10,0))

def otherCars(otherx, othery, otherColor):
    for i in range(len(otherx)):
        if otherColor[i] == 1:
            othercar = carImg1
        elif otherColor[i] == 2:
            othercar = carImg2
        elif otherColor[i] == 3:
            othercar = carImg3
        elif otherColor[i] == 4:
            othercar = carImg4       
        gameDisplay.blit(othercar, (otherx[i], othery[i]))

def newCarCheck(newx, newy, otherx, othery):
    #print("Checking new car")
    possible = True
    for i in range(len(otherx)):
        carx = otherx[i]
        cary = othery[i]
        checkx = (newx<(carx-car_width)) or (newx>(carx+car_width))
        checky = (newy>(cary+car_height)) or (newy<(cary-car_height))
        
        if (checkx and checky) == False:
            possible = False
    return possible

def moveCheck(newx, newy, otherx, othery): 
    allowed = True
    for i in range(len(otherx)):
        carx = otherx[i]
        cary = othery[i]
        checkx = (newx<(carx-car_width)) or (newx<(carx+car_width))
        checky = (newy<(cary+car_height))
        
        if (checkx and checky) == False:
            allowed = False
    return allowed

def road(liney,grassy,sidey,thing_speed):
    # Draw the road
    i=0
    for lineyVal in liney:
        lineyVal += thing_speed
        if lineyVal > display_height:
            lineyVal = -150
        liney[i] = lineyVal
        pygame.draw.rect(gameDisplay, white, [display_width/2, lineyVal, 10, 150])
        i+=1
        
    j = 0
    for grassyVal in grassy:
        grassyVal += thing_speed
        if grassyVal > display_height:
            grassyVal = -200
        grassy[j] = grassyVal
        gameDisplay.blit(grassL, (0, grassyVal))
        gameDisplay.blit(grassR, (display_width-grass_width, grassyVal))
        j += 1
        
    k = 0
    for sideyVal in sidey:
        sideyVal += thing_speed
        if sideyVal > display_height:
            sideyVal=-278
        sidey[k] = sideyVal
        pygame.draw.rect(gameDisplay, curb, [grass_width, sideyVal, 
                                              30, 900])
        pygame.draw.rect(gameDisplay, curb, [display_width-grass_width-30, sideyVal, 
                                              30, 900])
        k += 1
        
    return liney, grassy, sidey
        
def car(x,y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def crash():
    if MusicOn == True:
        pygame.mixer.music.stop()
    game_intro()
   
def quit_game():
    pygame.quit()
    quit()

def start(x, y, w, h, func=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h>mouse[1]>y:
        gameDisplay.blit(StartH, (300, 250))
        if click[0]==1 and func != None:
            func()
    else:
        gameDisplay.blit(Start, (300, 250))
        
def button(Norm, Hover, x, y, w, h, func=None):
    global clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h>mouse[1]>y:
        gameDisplay.blit(Hover, (x, y))
        if click[0]==1 and func != None:
            clickSound.play()
            func()
    else:
        gameDisplay.blit(Norm, (x, y))                
   
def unpause():
    global paused 
    paused = False
    if MusicOn == True:
        pygame.mixer.music.unpause()
    
def pause():
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(backgound)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        #button(msg, x, y, w, h, ic, ac)
        
        button("Continue", 200, 400, 100, 50, green, bright_green, unpause)
        button("Quit", 500, 400, 100, 50, red, bright_red, quit_game)
        
        pygame.display.update()
        clock.tick(15)

def game_intro():
    global count
    time.sleep(0.1)
    intro = True
    grassy= [-400, -200, 0, 200, 400]
    sidey = [-278, 0, 278, 556, 834]
    liney = [-150 , 100, 350, 600]
    gameDisplay.fill(gray)
    road(liney,grassy,sidey, 0)
    gameDisplay.blit(menuBG, (190, 50))
    gameDisplay.blit(Logo, (190, 75))
    
    if crashed == True:
        things_dodged()
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if crashed == False:
            button(Start, StartH, 300, 250, 207, 75, game_loop)
        else:
            #Change this to a 'replay button'
            button(Start, StartH, 300, 250, 207, 75, game_loop)
        button(Options, OptionsH, 250, 320, 294, 89, game_options)
        button(Quit, QuitH, 320, 390, 173, 91, quit_game)
        
        pygame.display.update()
        clock.tick(15)
        
def game_options():
    time.sleep(0.1)
    intro = True
    grassy= [-400, -200, 0, 200, 400]
    sidey = [-278, 0, 278, 556, 834]
    liney = [-150 , 100, 350, 600]
    gameDisplay.fill(gray)
    road(liney,grassy,sidey, 0)
    gameDisplay.blit(menuBG, (190, 50))
    gameDisplay.blit(Logo, (190, 75))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button(Music, MusicH, 230, 250, 230, 75, toggleMusic)
        button(Choose, ChooseH, 190, 320, 400, 75, choose_car)
        button(Return, ReturnH, 265, 390, 250, 75, game_intro)
        if MusicOn == True:
            button(On, On, 470, 250, 207, 75, None)
        else:
            button(Off, Off, 470, 250, 207, 75, None)
            
        pygame.display.update()
        clock.tick(15)
        
def choose_car():
    time.sleep(0.1)
    intro = True
    grassy= [-400, -200, 0, 200, 400]
    sidey = [-278, 0, 278, 556, 834]
    liney = [-150 , 100, 350, 600]
    gameDisplay.fill(gray)
    road(liney,grassy,sidey, 0)
    gameDisplay.blit(menuBG, (190, 50))
    gameDisplay.blit(Logo, (190, 75))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button(carImg1, carImg1, 300, 250, 65, 110, car1)
        button(carImg2, carImg2, 450, 250, 65, 110, car2)
        button(carImg3, carImg3, 300, 390, 65, 110, car3)
        button(carImg4, carImg4, 450, 390, 65, 110, car4)            
        pygame.display.update()
        clock.tick(15)

def car1():
    global carImg
    carImg = carImg1
    game_options()
def car2():
    global carImg
    carImg = carImg2
    game_options()
def car3():
    global carImg
    carImg = carImg3
    game_options()
def car4():
    global carImg
    carImg = carImg4
    game_options()
        
def toggleMusic():
    global MusicOn
    if MusicOn == True:
        MusicOn = False
    else:
        MusicOn = True
    game_options()

def game_loop():
    global paused
    global crashed
    global count
    count = 0
    if MusicOn == True:
        pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height *0.7)
    
    speed_change = 0
    x_change = 0
    
    BaseSpeed = 5
    CarSpeed = BaseSpeed
    MaxSpeed = BaseSpeed*2
    other_width = car_width
    other_height = 111
    otherSpeed = [2]
    otherx =  [random.randrange(grass_width+other_width, display_width-grass_width-other_width)]
    othery = [-600]
    otherColor = [random.randint(1,3)]
    grassy= [-400, -200, 0, 200, 400]
    sidey = [-278, 0, 278, 556, 834]
    liney = [-150 , 100, 350, 600]
    
    # testing
    stuck1 = 0
    stuck2 = 0
    
    
    gameExit = False
    
    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    speed_change = 0.2
                if event.key == pygame.K_DOWN:
                    speed_change = -0.3
                if event.key == pygame.K_p:
                    paused = True
                    pause()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP:
                    speed_change = 0
                if event.key == pygame.K_DOWN:
                    speed_change = 0
                    
        gameDisplay.fill(gray)  
        if CarSpeed>0:
            x += x_change
            
        if (speed_change > 0 and CarSpeed<MaxSpeed) or (speed_change < 0 and CarSpeed>BaseSpeed):
            CarSpeed += speed_change

        liney, grassy, sidey = road(liney,grassy,sidey, CarSpeed)
        otherCars(otherx, othery, otherColor)
        
        for i in range(len(othery)):
            newY = othery[i] + CarSpeed - otherSpeed[i]
            othery[i] = newY
        car(x, y)
        things_dodged()
        
        if x > display_width-car_width-grass_width or x < grass_width:
            crashSound.play()
            crashed = True
            crash()
        for i in range(len(othery)):    
            if othery[i] > display_height:
                newx = random.randrange(grass_width+other_width, 
                             display_width-grass_width-other_width)
                newy = random.randrange(-300, 0) - other_height
                possible = newCarCheck(newx, newy, otherx, othery)
                while possible == False:
                     stuck1 += 1
                     newx = random.randrange(grass_width+other_width, 
                                display_width-grass_width-other_width)
                     newy = random.randrange(-300, 0) - other_height
                     possible = newCarCheck(newx, newy, otherx, othery)
                othery[i] = newy
                otherx[i] = newx
                otherSpeed[i] = random.randrange(2, 5)
                otherColor[i] = random.randint(1,4)
                count += 1
                
                if count % 5 == 0:
                    ding.play()
                    BaseSpeed += 0.5
                    MaxSpeed = 2*BaseSpeed
                    if CarSpeed < BaseSpeed:
                        CarSpeed = BaseSpeed
                    if count % 10 == 0 and len(othery)<4:
                        # Add another car
                        newx = random.randrange(grass_width+other_width, 
                                     display_width-grass_width-other_width)
                        newy = random.randrange(-300, 0) - other_height
                        possible = newCarCheck(newx, newy, otherx, othery)
                        attempts = 0
                        while possible == False:
                             stuck2 += 1
                             newx = random.randrange(grass_width+other_width, 
                                        display_width-grass_width-other_width)
                             newy = random.randrange(-300, 0) - other_height
                             possible = newCarCheck(newx, newy, otherx, othery)
                             attempts += 1
                             if attempts == 10:
                                 # If at first you don't succeed, try, try, try 
                                 # again. After 10 tries though, just give up.
                                 possible = True
                        if attempts < 10:
                            otherx.append(newx)
                            othery.append(newy)
                            otherSpeed.append(random.randrange(2, 5))
                            otherColor.append(random.randint(1,3))
                                
            if y < othery[i]+other_height:
                check1 = (x > otherx[i] and x < otherx[i] + other_width)
                check2 =  (x + car_width > otherx[i] and x + car_width < otherx[i] + other_width)
                if check1 or check2:
                    crashSound.play()
                    crashed = True
                    crash()
                
        
        pygame.display.update()
        
        clock.tick(70)

game_intro()
game_loop()
pygame.quit()
quit()

"# NovaRace" 
