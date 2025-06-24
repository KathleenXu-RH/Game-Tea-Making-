##########################################################
# File Name: Final Game Assignment                       #
# Description: This is a program for the final game      #
# Author: Kathleen Xu                                    #
# Date: 12/14/2024                                       #
##########################################################

#---------------------------------------#
# Game Window Initialization            #
#---------------------------------------#
import random
import time
import pygame
pygame.init()

#---------------------------------------#
# constants                             #
#---------------------------------------#
WIDTH = 800
HEIGHT= 600
OUTLINE=0
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

#gravity setting
JUMP = -30
GRAVITY = 2

#scolling BG setting
wall1H = 800
wall1Y = 0
wall1X = 0
wall2H = 800
wall2Y = 0
wall2X = -800
wallSpeed = 5

#time setting
TIMER_LENGTH = 200
FPS = 30
clock = pygame.time.Clock()
start_time = time.time()
referenceTime = start_time
PERIOD = 1
elapsed = 0

#color code
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
YELLOW = (250,250,160)
BLUE = ( 24,171,214)
RED = (210, 44, 44)
GREEN = ( 0,128, 0)
sakuraPink = (255, 182, 193)
budGreen = (189, 252, 201)
lilacPurple = (200, 162, 200)
sunshineYellow = (255, 248, 188)
lavenderPurple = (230, 230, 250)
darkPurple = (110, 78, 115)

#image load
wall = pygame.image.load("pinkkie2.png")
wall = pygame.transform.scale(wall,(800,600))
rack = pygame.image.load("rack.png")
rack = pygame.transform.scale(rack,(800,200))
glassCup = pygame.image.load("glassCupEmpty.png")
glassCup = pygame.transform.scale(glassCup,(100,130))
desk = pygame.image.load("desk.png")
desk = pygame.transform.scale(desk,(800,150))
cupMat = pygame.image.load("cupMat.png")
cupMat = pygame.transform.scale(cupMat,(160,60))
pcupMat = pygame.image.load("pinkCupMat.png")
pcupMat = pygame.transform.scale(pcupMat,(80,30))
waterCupG = pygame.image.load("1waterCup.png")
waterCupG = pygame.transform.scale(waterCupG,(110,70))
teaCupG = pygame.image.load("teaCup.png")
teaCupG = pygame.transform.scale(teaCupG,(110,70))
daisyCupG = pygame.image.load("daisyCup.png")
daisyCupG = pygame.transform.scale(daisyCupG,(110,70))
oolongCupG = pygame.image.load("oolongCup.png")
oolongCupG = pygame.transform.scale(oolongCupG,(110,70))
lavenderCupG = pygame.image.load("lavenderCup.png")
lavenderCupG = pygame.transform.scale(lavenderCupG,(110,70))
berryCupG = pygame.image.load("berryCup.png")
berryCupG = pygame.transform.scale(berryCupG,(110,70))

#tea type list
waterCup = ["cup","water"]
teaCup = ["cup","water","teaLeaf"]
diasyCup = ["cup","water","daisy"]
oolongCup = ["cup","water","oolongLeaf"]
lavenderCup = ["cup","water","lavender"]
rasberryCup = ["cup","water","rasberry"]
berryOolongCup = ["cup","water","oolongLeaf","rasberry"]

          
#---------------------------------------#
# classes                               #
#---------------------------------------#
class Ingredient: 
    def __init__(self, name, image, x, y, width, height, boolean, booleanT):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.b = boolean # check if they should get painted
        self.bt = booleanT # check if they should "jump"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.originY = y 
        self.vy = 0 

    def draw(self, gameWindow):
        gameWindow.blit(self.image, (self.x, self.y))

    def jump(self):
        if self.y == self.originY: # only j if on "ground"
            self.vy = -15 #jump speed

    def update(self): # need ask
        if self.y < self.originY or self.vy < 0:
            self.vy += 2 # gravity effect
            self.y += self.vy
            if self.y >= self.originY: #check if it is back to "ground"
                self.y = self.originY
                self.vy = 0
                self.bt = False

    def change(self):
        for ingredient in ingredients:
            ingredient.b = False

#list for ingredients
ingredients = [
    Ingredient("water", "teaPot.png", 10, 40, 150, 130, False, False),
    Ingredient("teaLeaf", "teaBag.png", 130, 50, 160, 160, False, False),
    Ingredient("daisy", "daisyTea.png", 230, 40, 150, 130, False, False),    
    Ingredient("cup", "glassCupEmpty.png", 340, 45, 100, 130, False, False),
    Ingredient("oolongLeaf", "oolong.png", 430, 40, 110, 130, False, False),
    Ingredient("lavender", "lavender.png", 540, 40, 110, 120, False, False),
    Ingredient("rasberry", "rasberry.png", 660, 40, 110, 120, False, False),]


class Customer:
    def __init__(self, name, waitingI, unhappyI, happyI, x, y, width, height, boolean, booleanT):
        self.name = name
        self.waitingI = pygame.transform.scale(pygame.image.load(waitingI), (width, height))
        self.unhappyI = pygame.transform.scale(pygame.image.load(unhappyI), (width, height))
        self.happyI = pygame.transform.scale(pygame.image.load(happyI), (width, height))
        self.b = boolean # check if they should "wait" or "check process"
        self.bt = booleanT # check if they get correct or wrong tea
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.currentOrder = None  # store order
        self.timer = 0  # timer

    def draw(self, gameWindow):
        if self.b == False: #False = "wait"
            gameWindow.blit(self.waitingI, (self.x, self.y))
        elif self.b == True: #True = finish tea, check
            if self.bt == True: 
                gameWindow.blit(self.happyI, (self.x, self.y))
            elif self.bt == False:
                gameWindow.blit(self.unhappyI, (self.x, self.y))
            else:
                gameWindow.blit(self.waitingI, (self.x, self.y))

    def assignOrder(self, orderList):
        self.currentOrder = random.choice(orderList)
        print(" ",self.name, ":", self.currentOrder.command)


    def resetWaiting(self):
        self.b = False
        self.bt = None

#list for customers
customers = [
    Customer("Mrs Linda", "waiting1.png", "unhappy1.png", "happy1.png", 50,280, 100, 200, False, None),
    Customer("Melissa", "waiting2.png", "unhappy2.png", "happy2.png", 250, 280, 100, 200, False, None),
    Customer("Henry", "waiting3.png", "unhappy3.png", "happy3.png", 450, 280, 100, 200, False, None),
    Customer("Leonardo", "waiting4.png", "unhappy4.png", "happy4.png", 650, 280, 100, 200, False, None)]
    

class Order:
    def __init__(self, command, recipe, product):
        self.command = command
        self.recipe = recipe
        self.product = product

#list for orders
orders = [
    Order("I want no tea leaf in tea.", ["cup","water"], "water"),
    Order("Today is soooo hot.", ["cup","water"], "water"),
    Order("I'm thirsty.", ["cup","water","teaLeaf"], "tea"), 
    Order("HOHO, tea please!", ["cup","water","teaLeaf"], "tea"),
    Order("For me, daisy is the best.", ["cup","water","daisy"], "daisy tea"),
    Order("I would like some yellow flowers in my tea.", ["cup","water","daisy"], "daisy tea"),
    Order("OHH oolong is my mom's favorite!", ["cup","water","oolongLeaf"], "oolong tea"),
    Order("I want oolong.", ["cup","water","oolongLeaf"], "oolong"),
    Order("Need lavender.", ["cup","water","lavender"], "lavender tea"),
    Order("Do you know that lavender will help you get into sleep?", ["cup","water","lavender"], "lavender tea"),
    Order("Rasberry is juicy!", ["cup","water","rasberry"], "rasberry tea"),
    Order("Rasberry is cheap recently!", ["cup","water","rasberry"], "rasberry tea")]

#---------------------------------------#
# functions                             #
#---------------------------------------#
def teaShopPage(C): 
    drawBG() #background graphics
    gameWindow.blit(rack, (0,0))
    for i in range(len(customers)): #customer graphics
        customers[i].draw(gameWindow)
    gameWindow.blit(desk,(0,450))
    gameWindow.blit(pcupMat,(60,460))
    gameWindow.blit(pcupMat,(260,460))
    gameWindow.blit(pcupMat,(460,460))
    gameWindow.blit(pcupMat,(660,460))
    gameWindow.blit(cupMat,(330,530))
    for ingredient in ingredients:
        ingredient.draw(gameWindow)
    pygame.display.update() 

def drawBG():
    gameWindow.blit(wall, (wall1X, wall1Y))
    gameWindow.blit(wall, (wall2X, wall2Y))

def display_points(points):
    graphics = font.render("Points: " + "*️" * points,1,darkPurple)
    gameWindow.blit(graphics,(260,20))

def add_points(points):
    if points < max_points:
        points += 1
    return points

def subtract_points(points):
    if points > 0:
        points -= 1
    return points
    
def drawWater(Area,C):
    pygame.draw.rect(gameWindow, C, (382,Area,48,30), OUTLINE)

#---------------------------------------#
# initialize variables                  #
#---------------------------------------#
font = pygame.font.SysFont("Courier New",15)
mouseX,mouseY = pygame.mouse.get_pos()
buttons = pygame.mouse.get_pressed()
running = True #check the loop
finishedDrinkG = None #check if there is a finished drink and what is it
areaNotOccupied = True #check if the make tea mat is occupied
makeOrder = True #check if it is time to make a new order
orderFinished = 0
color = sunshineYellow
points = 0
max_points = 10
#tea rect
tea_X = 360
tea_Y = 500
tea_Speed = 5
teaRect = pygame.Rect(tea_X, tea_Y, 110, 70)

#define makingTea
teaOrder = []
makeTea = []


#---------------------------------------#
# main program                          #
#---------------------------------------#
print("Hit ESC to exit")
print("Read Shell DURING GAME")
print("PRESS KEYS: c - CUP, w - WATER, t - TEA, d - DAISY, o - OOLONG, l - LAVENDER, r - RASBERRY")
print("USE ARROWS: to MOVE the tea! \nUSE LEFT and RIGHT first, then USE THE UP.")
print("REMINDER: we only offer water, daisy tea, tea, oolong tea, lavender tea, and rasberry tea!")
level = int(input("Which LEVEL would you like? give me 1 or 2 or 3"))
if level == 1:
    TIMER_LENGTH = 100
    print("Your level is LEVEL ONE! \nFinish FOUR tea in 100s!")
elif level ==2:
    TIMER_LENGTH = 90
    print("Your level is LEVEL TWO! \nFinish NINE tea in 90s!")
elif level ==3:
    TIMER_LENGTH = 60
    print("Your level is LEVEL THREE! \nFinish NINE tea in 60s!")


#loop start
while running:
    clock.tick(FPS)

    # scroll the background
    wall1X = wall1X + wallSpeed
    wall2X = wall2X + wallSpeed
    if wall1X > wall1H: 
        wall1X = -wall2H
        wall2X = 0
    elif wall2X > wall2H:
        wall2X = -wall1H
        wall1X = 0

    #redraw BG 
    teaShopPage(color)
    #draw finished drink
    if finishedDrinkG != None:
        gameWindow.blit(finishedDrinkG, (tea_X, tea_Y))
        for i in range(len(customers)):
            customers[i].b = True
    
    #keys setting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    #move cup
    if keys[pygame.K_RIGHT]:
        tea_X += tea_Speed
    elif keys[pygame.K_LEFT]:
        tea_X -= tea_Speed
    elif keys[pygame.K_UP]:
        tea_Y -= tea_Speed
    elif keys[pygame.K_DOWN]:
        tea_Y += tea_Speed

        
    #customer order setting
    if makeOrder:
        print("Customer Order! \nNames correspond to the seat!")
        for customer in customers:
            customer.assignOrder(orders)
            customer.b = False           
            customer.bt = None
            customer.timer = 0
        makeOrder = False  
 
    teaRect = pygame.Rect(tea_X, tea_Y, 110, 70)
    #customer reaction setting
    for i in range(len(customers)):
        customerRect = pygame.Rect(customers[i].x, customers[i].y, customers[i].width, customers[i].height)
        if customerRect.colliderect(teaRect) and customers[i].b and finishedDrinkG!= None:  # detect collision
            # check tea and order
            if sorted(makeTea) == sorted(customers[i].currentOrder.recipe):
                customers[i].b = True
                customers[i].bt = True
                print(customers[i].name,": Correct drink! Thankyou!")
                points = add_points(points)  
            elif sorted(makeTea) != sorted(customers[i].currentOrder.recipe):
                customers[i].b = True
                customers[i].bt = False
                print(customers[i].name,": Wrong drink! Sad!")
                points = subtract_points(points)
                
            customers[i].timer = time.time()
            finishedDrinkG = None
            areaNotOccupied = True
            makeTea.clear()

    # check if all the customers are served and if graphic effect time has passed for 2 seconds 
    allServed = all(customer.bt != None for customer in customers)
    timePassed = all(customer.b and time.time() - customer.timer > 2 for customer in customers)
    if allServed and timePassed:
        makeOrder = True
      


    #check MAKETEA actions
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and ingredients[3].b and not ingredients[0].b:
                ingredients[0].b = True
                ingredients[0].bt = True
                makeTea.append("water")
            if event.key == pygame.K_t and ingredients[3].b and not ingredients[1].b:
                ingredients[1].b = True
                ingredients[1].bt = True
                makeTea.append("teaLeaf")
            if event.key == pygame.K_d and ingredients[3].b and not ingredients[2].b: 
                ingredients[2].b = True
                ingredients[2].bt = True
                makeTea.append("daisy")
            if event.key == pygame.K_o and ingredients[3].b and not ingredients[4].b: 
                ingredients[4].b = True
                ingredients[4].bt = True
                makeTea.append("oolongLeaf")
            if event.key == pygame.K_l and ingredients[3].b and not ingredients[5].b: 
                ingredients[5].b = True
                ingredients[5].bt = True
                makeTea.append("lavender")
            if event.key == pygame.K_r and ingredients[3].b and not ingredients[6].b: 
                ingredients[6].b = True
                ingredients[6].bt = True
                makeTea.append("rasberry")
            if event.key == pygame.K_c and areaNotOccupied and not ingredients[3].b: 
                ingredients[3].b = True
                ingredients[3].bt = True
                makeTea.append("cup")


            #button for finishing
            if event.key == pygame.K_f and ingredients[3].b:
                tea_X, tea_Y = 360, 500
                print("Finished!")
                print("Your recipe: ",makeTea)
                areaNotOccupied = False
                finishedDrinkG = None #reset to None
                
                #check tea type
                if sorted(makeTea) == ["cup"]:
                    print("just a cup!")
                    areaNotOccupied = True
                    makeTea.clear()
                elif sorted(makeTea) == sorted(waterCup):
                    print("water drink!")
                    finishedDrinkG = waterCupG
                elif sorted(makeTea) == sorted(teaCup):
                    print("tea drink!")
                    finishedDrinkG = teaCupG
                elif sorted(makeTea) == sorted(diasyCup):
                    print("daisy tea drink!")
                    finishedDrinkG = daisyCupG
                elif sorted(makeTea) == sorted(oolongCup):
                    print("oolong tea drink!")
                    finishedDrinkG = oolongCupG
                elif sorted(makeTea) == sorted(lavenderCup):
                    print("lavender tea drink!")
                    finishedDrinkG = lavenderCupG
                elif sorted(makeTea) == sorted(rasberryCup):
                    print("rasberry tea drink!")
                    finishedDrinkG = berryCupG
                else:
                    print("Random drink!")
                    areaNotOccupied = True
                    makeTea.clear()

                for i in range(len(ingredients)):
                    ingredients[i].b = False
                for i in range(len(customers)):
                    customers[i].b = True


    #tea material JUMP action
    for i in range(len(ingredients)):
        if ingredients[i].bt == True:
            ingredients[i].draw(gameWindow)
            ingredients[i].jump()
            ingredients[i].update()
            teaShopPage(color)
            

    #after cup is placed
    if ingredients[3].b and areaNotOccupied:
        gameWindow.blit(glassCup, (350, 430))
        if ingredients[0].b:#pot
            drawWater(513,BLUE)
        if ingredients[1].b:#tea
            drawWater(485,GREEN)
        if ingredients[2].b:#daisy
            drawWater(485,sunshineYellow)
        if ingredients[4].b:#oolong
            drawWater(485,budGreen)
        if ingredients[5].b:#lavender
            drawWater(485,lilacPurple)
        if ingredients[6].b:#rasberry
            drawWater(485,sakuraPink)

    #timer setting
    elapsed_time = time.time() - start_time
    remain_time = TIMER_LENGTH - int(elapsed_time)
    elapsed = round((time.time() - referenceTime),1)
    if remain_time >= 0:
        pygame.draw.rect(gameWindow, color, (45,20,205,20), OUTLINE)
        pygame.draw.rect(gameWindow, color, (260,20,200,20), OUTLINE)
        graphics = font.render("The remain time is " + str(remain_time), 1,darkPurple) 
        gameWindow.blit(graphics, (50, 20))
        display_points(points)
    else:
        print( "time's up! game over! ")
        running = False

    #update
    display_points(points)
    referenceTime = time.time()
    pygame.display.update()

#---------------------------------------#

#check the level and the score
if level == 1:
    if max_points < 4:
        print(points)
        print("YOU FAILED!")
    elif points == 4:
        print(points)
        print("YOU WIN!")
    elif points > 4:
        print(points)
        print("GREAT JOB! YOU WIN A BONUS!")
elif level ==2:
    if points < 9:
        print(points)
        print("YOU FAILED!")
    elif points == 9:
        print(points)
        print("YOU WIN!")
    elif points > 9:
        print(points)
        print("FANTASTIC! YOU WIN A BONUS!")
elif level ==3:
    if points < 9:
        print(points)
        print("YOU FAILED!")
    elif points == 9:
        print(points)
        print("YOU WIN!")
    elif points > 9:
        print(points)
        print("GENIUS! YOU WIN A BONUS!")
    
pygame.quit()


