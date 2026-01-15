import random as rand
import time as t
import threading as threads
from copy import deepcopy
import msvcrt as charin

inventory = []
visitedplaces = []
playerplace = [0,2,0]

strength = 1
speed = 1
health = 30
turncounter = 0
timeplayed = 0
totalchests = 0
totalguardedchests = 0
totalswordrooms = 0
totalmagicstones = 0
#WORK IN PROGRESS
proceduralgen = "on-"
#WORK IN PROGRESS
devhacks = False
reset = False
spawnedboss = False

#Colors!!!!!!!!!!!!!
class colors:
    red = '\033[31m'
    yellow = '\033[33m'
    green = '\033[32m'
    blue = '\033[34m'
    purple = '\033[35m'
    reset = '\033[0m'
    clear = '\033c'

stoptitle = threads.Event()
settings = threads.Event()
checkevent = threads.Event()
timerevent = threads.Event()

"""
On each turn, the player will have many options. If they are in a fight, they can choose to attack or block. If they are not, then they can choose where to go and what to interact with.
"""

colorlist = [colors.red, colors.yellow, colors.green, colors.blue, colors.purple]
print(colors.clear)
def printtitle():
    while not stoptitle.is_set():
        for color in colorlist:
            print(f"""{color}-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------ssssssssssss---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------ss------------ss-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------ss-press-s--for-ss------------------------------------------------gg----------------------------------------------------------------------------------------------------------------------
-------ss--------------ss-------------------------------------------gggg-gg---------aaa-aa---------eeee------------------------------------------------------------------------------------------
-------ss---settings---ss-----------------------------------------gg----ggg-------aa---aaa-------ee---ee------mm-mmmmm--mmmmm--------------------------------------------------------------------
--------ss------------ss-----------------------------------------gg------gg-----aa------aa------ee-----ee-----mmm----mmmm---mm-------------------------------------------------------------------
-----------sssssssssss-------------------------------------------gg------gg-----aa------aa------eeeeeeeee-----mm------mm-----mm------------------------------------------------------------------
-----------------------------------------------------------------gg------gg-----aa------aa------ee------------mm------mm-----mm------------------------------------------------------------------
------------------------------------------------------------------gg----ggg-------aa---aaa-------ee-----------mm------mm-----mm------------------------------------------------------------------
-------------------------------------------------------------------gggggggg---------aaa-aa---------eeeeee-----mm-------------mm------------------------------------------------------------------
-------------------------------------------------------------------------gg----------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------gg----------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------gg----------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------gg----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------gg------gg-----------fffffffffffffffffffffffffffffffff--------------------------------------------------------------------------
-----------------------------------------------------------------gg-----gg----------ff---------------------------------ff------------------------------------------------------------------------
-------------------------------------------------------------------ggggg-----------ff-----------------------------------ff-----------------------------------------------------------------------
-----------------------------------------------------------------------------------ff----------press-f-to-play----------ff-----------------------------------------------------------------------
-----------------------------------------------------------------------------------ff-----------------------------------ff-----------------------------------------------------------------------
------------------------------------------------------------------------------------ff---------------------------------ff------------------------------------------------------------------------
--------------------------------------------------------------------------------------fffffffffffffffffffffffffffffffff--------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {colors.reset}""")
            t.sleep(0.25)
            print(colors.clear)
            if stoptitle.is_set():
                break
                pass
            if settings.is_set():
                printsettings(True)
def printsettings(input):
    global proceduralgen
    global threedimensional
    print(f"""{colors.blue}-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------sssss-----------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------ss----------eeee-------tt--------tt------ii----nn-nnnn-------gggg-gg-----ssss------------------------------------------------------------------------
--------------------------------------------ss--------ee---ee----tttttt----tttttt----------nnn---nn----gg---gggg----ss---------------------------------------------------------------------------
---------------------------------------------ssss-----eeeeeee------tt--------tt------ii----nn----nn----gg----ggg-----ssss------------------------------------------------------------------------
------------------------------------------------ss----ee-----------tt--------tt------ii----nn----nn----gg---gggg--------ss-----------------------------------------------------------------------
------------------------------------------------ss-----eeeeee------tt--------tt------ii----nn----nn------gggg-gg-----ssss------------------------------------------------------------------------
--------------------------------------------sssss------------------------------------------------------g-----gg----------------------------------------------------------------------------------
---------------------------------------------------------11------)------------------------------ooooo---gggggg-----------------------------------------------------------------------------------
--------------------------------------------------------1-1-------)---------------------------oo-----oo------------------------------------------------------------------------------------------
----------------------------------------------------------1-------)-procedural-generation-----oo-{proceduralgen}-oo------------------------------------------------------------------------------------------
----------------------------------------------------------1-------)---------------------------oo-----oo------------------------------------------------------------------------------------------
--------------------------------------------------------11111--.-)------------------------------ooooo--------------------------------------------------------------------------------------------
-------------------------------------------------------------(double-press-1-or-2-to-change-settings)--------------------------------------------------------------------------------------------
------------------------------------------------------##################################################-----------------------------------------------------------------------------------------
------------------------------------------------------##################################################-----------------------------------------------------------------------------------------
------------------------------------------------------##################--UNFINISHED--##################-----------------------------------------------------------------------------------------
------------------------------------------------------##################################################-----------------------------------------------------------------------------------------
------------------------------------------------------##################################################-----------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------sssssssssssssssssssssssssssssss-----------------------------------------------------------------------------------------------
------------------------------------------------------------------ss-----------------------------ss----------------------------------------------------------------------------------------------
-----------------------------------------------------------------ss----press-s-twice-to-return----ss---------------------------------------------------------------------------------------------
-----------------------------------------------------------------ss-------------------------------ss---------------------------------------------------------------------------------------------
------------------------------------------------------------------ss-----------------------------ss----------------------------------------------------------------------------------------------
-------------------------------------------------------------------sssssssssssssssssssssssssssssss-----------------------------------------------------------------------------------------------{colors.reset}""")
    if input == True:
        while True:
            char = ''
            #Make sure a key was pressed before getting the key
            if charin.kbhit():
                char = charin.getch().decode("utf-8")
            if char == "1":
                if proceduralgen == "on-":
                    proceduralgen = "off"
                else:
                    proceduralgen = "on-"
                print(colors.clear)
                printsettings(False)
            if char == "2":
                if threedimensional == "on-":
                    threedimensional = "off"
                else:
                    threedimensional = "on-"
                print(colors.clear)
                printsettings(False)
            if not settings.is_set():
                break
            t.sleep(0.25)

def checkchar():
    while not checkevent.is_set():
        char = ''
        if charin.kbhit():
                char = charin.getch().decode("utf-8")
        if char == "f":
            #Stop the title screen if the settings are not open
            if not settings.is_set():
                stoptitle.set()
        if char == "s":
            #Toggle settings menu
            if not settings.is_set():
                settings.set()
            elif settings.is_set():
                settings.clear()
            print(colors.clear)
        t.sleep(0.25)

"""
def updatetime():
    global timeplayed
    while not timerevent.is_set():
        t.sleep(1)
        timeplayed += 1
"""

checkthread = threads.Thread(target=checkchar)

#Start threads
checkthread.start()

printtitle()
checkevent.set()

def possmovements():
    possiblemovements = []
    
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] != "puzzle":
        if playerplace[1] != 0: #In case they are on the top, this way the program will not throw an error
            if rooms[playerplace[0]][playerplace[1] - 1][playerplace[2]] != "" and rooms[playerplace[0]][playerplace[1] - 1][playerplace[2]] != "lava": #Check for left
                    possiblemovements.append("go left")
                
    if playerplace[1] != 4: #In case they are on the bottom
        if rooms[playerplace[0]][playerplace[1] + 1][playerplace[2]] != "" and rooms[playerplace[0]][playerplace[1] + 1][playerplace[2]] != "lava": #Check for right
                possiblemovements.append("go right")
            
    if playerplace[2] != 4: #In case they are on the right
        if rooms[playerplace[0]][playerplace[1]][playerplace[2] + 1] != "" and rooms[playerplace[0]][playerplace[1]][playerplace[2] + 1] != "lava": #Check for forwards
                possiblemovements.append("go forwards")
        
    if playerplace[2] != 0: #In case they are on the left
        if rooms[playerplace[0]][playerplace[1]][playerplace[2] - 1] != "" and rooms[playerplace[0]][playerplace[1]][playerplace[2] - 1] != "lava": #Check for backwards
                possiblemovements.append("go backwards")
        
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "stairsup":
        possiblemovements.append("go up")
        
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "stairsdown":
        possiblemovements.append("go down")
        
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "swordroom":
        try:
            index = inventory.index("sword")
        except:
            possiblemovements.append("grab sword")
            
        
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "magicstone":
        try:
            index = inventory.index("magic stone")
        except:
            possiblemovements.append("grab magic stone")
            
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "puzzle":
        possiblemovements.append("try puzzle")
    
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "chest":
        possiblemovements.append("open chest")
    
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "chestguarded":
        possiblemovements.append("fight chest guarder")
    
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "finalboss":
        possiblemovements.append("fight final boss")
    return possiblemovements

def emptyplaces(currentplace):
    #Determine which rooms are empty
    availableplaces = [[currentplace[0], currentplace[1] + 1, currentplace[2]], [currentplace[0], currentplace[1] - 1, currentplace[2]], [currentplace[0], currentplace[1], currentplace[2] + 1], [currentplace[0], currentplace[1], currentplace[2] - 1]]
    
    try: #Check the room in the row above
        if currentplace[1] != 0:
            if rooms[currentplace[0]][currentplace[1] - 1][currentplace[2]] != "":
                availableplaces.remove([currentplace[0],currentplace[1] - 1,currentplace[2]])
        if currentplace[1] == 0:
            availableplaces.remove([currentplace[0],currentplace[1] - 1,currentplace[2]])        
    
    except:
        if currentplace[1] == 0:
            availableplaces.remove([currentplace[0],currentplace[1] - 1,currentplace[2]])

    try: #Check the room in the row below
        if currentplace[1] != 4:
            if rooms[currentplace[0]][currentplace[1] + 1][currentplace[2]] != "":
                availableplaces.remove([currentplace[0],currentplace[1] + 1,currentplace[2]])
        if currentplace[1] == 4:
            availableplaces.remove([currentplace[0],currentplace[1] + 1,currentplace[2]])
            
    except:
        if currentplace[1] == 4:
            availableplaces.remove([currentplace[0],currentplace[1] + 1,currentplace[2]])

    try: #Check the room in the col to the left
        if currentplace[2] != 0:
            if rooms[currentplace[0]][currentplace[1]][currentplace[2] - 1] != "":
                availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] - 1])
        if currentplace[2] == 0:
            availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] - 1])
    
    except:
        if currentplace[2] == 0:
            availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] - 1])

    try: #Check the room in the col to the right
        if currentplace[2] != 4:
            if rooms[currentplace[0]][currentplace[1]][currentplace[2] + 1] != "":
                availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] + 1])
        if currentplace[2] == 4:
            availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] + 1])

    except:
        if currentplace[2] == 4:
            availableplaces.remove([currentplace[0],currentplace[1],currentplace[2] + 1])

    return availableplaces

def createrooms():
    #Create a random set of rooms
    global timeplayed, totalchests, totalguardedchests, totalswordrooms, totalmagicstones, spawnedboss
    reqrooms = 2

    #Empty places around the player
    availableplaces = emptyplaces(playerplace)
    
    if len(availableplaces) < 2:
        #Make sure only available rooms will be created on
        reqrooms = len(availableplaces)
    while reqrooms > 0:
        #Check which places are available so that we don't try to place 2 rooms on top of one another
        availableplaces = emptyplaces(playerplace)
        for place in availableplaces:

            if reqrooms == 0:
                break
            
            existsornot = rand.randint(0,1) #Determines whether or not to create a new room
            
            if existsornot == 1:
                reqrooms -= 1

                typesofrooms = ["nothing"]
                
                if playerplace[0] > 0:
                    typesofrooms.append("stairsdown")
                if playerplace[0] < 2:
                    typesofrooms.append("stairsup")
                if totalchests < 3:
                    typesofrooms.append("chest")
                    totalchests += 1
                if totalguardedchests < 5:
                    typesofrooms.append("guardedchest")
                    totalguardedchests += 1
                if totalswordrooms < 1:
                    typesofrooms.append("swordroom")
                    totalswordrooms += 1
                if totalmagicstones < 1:
                    typesofrooms.append("magicstone")
                    totalmagicstones += 1
                if turncounter >= 10 and spawnedboss == False:
                    startboss = rand.randint(1,5) #1 = start, anything else = doesn't
                    if startboss == 1:
                        typesofrooms = ["finalboss", "finalboss"]
                        spawnedboss = True
                
                room = rand.randint(0, len(typesofrooms) - 1) #The type of the room that is to be created
                try:
                    rooms[place[0]][place[1]][place[2]] = typesofrooms[room]
                except:
                    continue

            #Turn the above/below rooms into stairs going up/down if you are at a staircase
            if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "stairsdown":
                rooms[playerplace[0] - 1][playerplace[1]][playerplace[2]] = "stairsup"

            if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "stairsup":
                rooms[playerplace[0] + 1][playerplace[1]][playerplace[2]] = "stairsdown"

def dochoice(possiblemovements, choice):
    global strength, speed, health
    if possiblemovements[choice - 1] == "go left":
        playerplace[1] -= 1
    if possiblemovements[choice - 1] == "go right":
        playerplace[1] += 1
    if possiblemovements[choice - 1] == "go forwards":
        playerplace[2] += 1
    if possiblemovements[choice - 1] == "go backwards":
        playerplace[2] -= 1
    if possiblemovements[choice - 1] == "go up":
        playerplace[0] += 1
    if possiblemovements[choice - 1] == "go down":
        playerplace[0] -= 1

    if possiblemovements[choice - 1] == "grab sword":
        inventory.append("sword")
        print("Sword acquired!")
        print("Strength will permanantly be doubled during fights.")
        
    if possiblemovements[choice - 1] == "grab magic stone":
        inventory.append("magic stone")
        print("Magic stone acquired!")
        print("The magic stone can deal 5 damage at a time, but has a cooldown of 3 turns.")
        
    if possiblemovements[choice - 1] == "try puzzle":
        print("The puzzle is:")
        print("\nGo to the incorrect path.\n") #Incorrect = not right, which is left
        print("Go left or right?")
        print("1.) LEFT")
        print("2.) FORWARD")
        try:
            side = int(input("> "))
        except:
            side = -1
        while side < 1 or side > 2:
            print("Invalid input. Enter again:")
            try:
                side = int(input("> "))
            except:
                side = -1
                
        if side == 1:
            playerplace[1] -= 1
        else:
            playerplace[2] += 1
            
    if rooms[playerplace[0]][playerplace[1]][playerplace[2]] == "lava":
        print("You fell into the lava.")
        return 1
        
    if possiblemovements[choice - 1] == "open chest":
        potionnum = rand.randint(1,3)
        if potionnum == 1:
            potion = "strength"
        elif potionnum == 2:
            potion = "speed"
        else:
            potion = "health"
        print(f"You got a {potion} potion.")
        if potion == "strength":
            strength += 1
            print(f"New strength: {strength}")
        elif potion == "speed":
            speed += 1
            print(f"New speed: {speed}")
        else:
            health += 3
            print(f"New health: {health}")
        
        rooms[playerplace[0]][playerplace[1]][playerplace[2]] = "openedchest"
            
    if possiblemovements[choice - 1] == "fight chest guarder":
        wonfight = fight("chest guarder", 20, 1, False, health)
        if wonfight:
            print("The chest guarder was protecting a chest. Inside the chest, there was:")
            potionnum = rand.randint(1,3)
            if potionnum == 1:
                potion = "strength"
            elif potionnum == 2:
                potion = "speed"
            else:
                potion = "health"
            print(f"A {potion} potion.")
            if potion == "strength":
                strength += 1
                print(f"New strength: {strength}")
            elif potion == "speed":
                speed += 1
                print(f"New speed: {speed}")
            else:
                health += 3
                print(f"New health: {health}")
            
            rooms[playerplace[0]][playerplace[1]][playerplace[2]] = "openedchest"
        else:
            return 1
    
    if possiblemovements[choice - 1] == "fight final boss":
        wonfight = fight("King Goblin", 25, 1, False, health)
        if wonfight:
            print("You defeated the final boss! Behind it, there was a room full of treasure. You got $1,000,000,000,000,000,000,000,000!")
            return 1

    return 0

def fight(whatisfighting, theirhealth, theirstrength, theyhavesword, health):
    print(f"Fighting {whatisfighting.lower()}.")
    try:
        index = inventory.index("sword")
        hassword = True
    except:
        hassword = False
    turn = "player"
    cooldown = 0
    blocking = False
    theyareblocking = False
    startinghealth = health
    theirstartinghealth = theirhealth
    while theirhealth > 0 and health > 0:
        print("Your health:")
        print("<", end = "")
        for hp in range(health):
            if hp <= startinghealth:
                print("-", end = "")
            else:
                print("X", end = "")
        print(">")
        
        print("Their health:")
        print("<", end = "")
        for hp in range(theirhealth):
            print("-", end = "")
        print(">")
        
        if turn == "player":
            if cooldown != 0:
                cooldown -= 1
            blocking = False
            while True:
                try:
                    index = inventory.index("magic stone")
                    options = ["block", "attack", "magic"]
                except:
                    options = ["block", "attack"]
                print("What would you like to do? You can do:")
                for i,option in enumerate(options):
                    print(f"{i + 1}: {option.upper()}")
                
                try:
                    choice = int(input("> "))
                except:
                    choice = -1
        
                while choice > len(options) or choice <= 0:
                    print("Invalid choice. Enter again:")
                    for i, option in enumerate(options):
                        print(f"{i + 1}.) {option.upper()}")
                    try:
                        choice = int(input("> "))
                    except:
                        choice = -1
                
                if options[choice - 1] == "block":
                    blocking = True
                    
                if options[choice - 1] == "attack":
                    if theyareblocking == False:
                        if hassword == True:
                            theirhealth -= strength * 2 * speed
                        else:
                            theirhealth -= strength * speed
                    else:
                        print(f"{whatisfighting} blocked you!")
                        
                if options[choice - 1] == "magic":
                    if cooldown == 0:
                        cooldown = 3
                        theirhealth -= 5
                    else:
                        print("Cooldown has not finished yet.")
                        continue
                break
            turn = "monster"
        else:
            theyareblocking = False
            options = ["block", "attack"]
            choice = rand.choice(options)
            if choice == "block":
                theyareblocking = True
                print("They attacked you!") #Just to throw off the player, otherwise the player would know when they are blocking
            else:
                if blocking == False:
                    print("They attacked you!")
                    if theyhavesword == True:
                        health -= theirstrength * 2
                    else:
                        health -= theirstrength
                else:
                    print(f"You blocked {whatisfighting}!")
            turn = "player"
                
    if theirhealth <= 0:
        print("You won! Congratulations!")
        return True
    else:
        print("You lost. Better luck next time!")
        return False

if proceduralgen == "on-":
    rooms = [
        [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["nothing", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
        ],
        
        [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
        ],
        
        [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
        ]
    ] 
elif proceduralgen == "off":
    rooms = [
        [
        ["nothing", "nothing", "nothing", "", ""],
        ["nothing", "", "", "", ""],
        ["nothing", "nothing", "nothing", "nothing", ""],
        ["", "", "stairsup", "", ""],
        ["chestguarded", "nothing", "nothing", "", ""]
        ],
        
        [
        ["", "nothing", "nothing", "chest", ""],
        ["", "nothing", "", "", ""],
        ["", "chestguarded", "nothing", "", "nothing"],
        ["magicstone", "", "stairsdown", "nothing", "swordroom"],
        ["stairsup", "", "", "", "stairsup"]
        ],
        
        [
        ["chest", "", "", "", ""],
        ["puzzle", "lava", "", "", ""],
        ["nothing", "nothing", "nothing", "finalboss", "finalreward"],
        ["nothing", "", "", "", ""],
        ["stairsdown", "nothing", "nothing", "nothing", "stairsdown"]
        ]
    ] 

while True:
    turncounter += 1

    if (turncounter >= 20 and spawnedboss == True) or turncounter >= 50:
        print("The King Goblin confronted you, because you were taking so long that he just got bored")
        wonfight = fight("King Goblin", 25, 1, False, health)
        if wonfight:
            print("You defeated the final boss! Behind it, there was a room full of treasure. You got $1,000,000,000,000,000,000,000,000!")
            break
    
    """
    if devhacks == True:
        health = 100000
        speed = 100000
        strength = 100000
        
        if reset == False:
            print("Procedural generation")
            choice = input("> ")
            if choice == "on":
                proceduralgen == "on-"
                playerplace = [0, 2, 0]
                rooms = [
                    [
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["nothing", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""]
                    ],
                    
                    [
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""]
                    ],
                    
                    [
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "", "", ""]
                    ]
                ] 
            else:
                proceduralgen == "off"
                playerplace = [0, 2, 0]
                rooms = [
                    [
                    ["nothing", "nothing", "nothing", "", ""],
                    ["nothing", "", "", "", ""],
                    ["nothing", "nothing", "nothing", "nothing", ""],
                    ["", "", "stairsup", "", ""],
                    ["chestguarded", "nothing", "nothing", "", ""]
                    ],
                    
                    [
                    ["", "nothing", "nothing", "chest", ""],
                    ["", "nothing", "", "", ""],
                    ["", "chestguarded", "nothing", "", "nothing"],
                    ["magicstone", "", "stairsdown", "nothing", "swordroom"],
                    ["stairsup", "", "", "", "stairsup"]
                    ],
                    
                    [
                    ["chest", "", "", "", ""],
                    ["puzzle", "lava", "", "", ""],
                    ["nothing", "nothing", "nothing", "finalboss", "finalreward"],
                    ["nothing", "", "", "", ""],
                    ["stairsdown", "nothing", "nothing", "nothing", "stairsdown"]
                    ]
                ] 
            reset = True
    """
            
    #Create rooms
    if proceduralgen == "on-":
        if playerplace not in visitedplaces:
            createrooms()
            visitedplaces.append(deepcopy(playerplace))
    """
    #Print rooms
    for floor in rooms:
        for row in floor:
            print(row)
        print()
    """
    #Figuring out what moves we can make
    possiblemovements = possmovements()
    
    #Ask what the player wants to do
    print("What would you like to do? You can do:")
    for i, movement in enumerate(possiblemovements):
        print(f"{i + 1}.) {movement.upper()}")
    
    try:
        choice = int(input("> "))
    except:
        choice = -1
    """
    if choice == 1234567890:
        devhacks = True
        print("Dev hacks enabled")
    else:
    """
    #Check if the choice is valid
    while choice > len(possiblemovements) or choice <= 0:
        print("Invalid choice. Enter again:")
        for i, movement in enumerate(possiblemovements):
            print(f"{i + 1}.) {movement.upper()}")
        try:
            choice = int(input("> "))
        except:
            choice = -1

    #Do what the player asked for
    if dochoice(possiblemovements, choice) == 1:
        break
