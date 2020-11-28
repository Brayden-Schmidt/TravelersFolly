#Python Text RPG
#Brayden Schmidt
screen_width = 100
import cmd
import textwrap
import sys
import os
import time
import random
from os import system, name
from time import sleep
from colorama import Fore, Back, Style
import msvcrt
import numpy 
##### Text-Settings ####
def typ(text,speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    return
    #xxslow- .05
    #xslow - .04
    #medium - .03
    #fast - .01
    #xfast - .005
def c():
    if name == 'nt':
        _ = system('cls')

##### Player Set UP ####
class player:
    def __init__(self):
        self.name = ''
        self.hp = 0
        self.mp = 0
        self.status = []
        self.location = 24
class inventory:
    def __init__(self):
        self.items = [" "]
    def printinventory(self):
        typ("+ -Backpack-\n",.01)
        for item in self.items:
            typ ("   "+ item +"",.01)
Myplayer = player()
Myinventory = inventory()
##### Title Screen #####
def title_screen_selections():
    option = input(">")
    if option.lower() == ("play"):
        start_game()
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("menu"):
        title_screen()
    elif option.lower() == ("quit"):
        sys.exit()  
    else:
        print ('INVALID')
        title_screen_selections()
def title_screen():
    c()
    '_____________________________________________________  \n|  #########################            _.._  __     | \n|   Welcome to the Text RPG         .--{    }/  "~-._| \n|  #########################       /    ^++^/       /| \n|           - Play -               {        (0     / | \n|                                  \\=.___ .//\\___+"  | \n|                                   \\   .//\'     /    | \n|           - Help -                )  _//\'    _(     | \n|                                   (HHHHH[]HHHH)     | \n|                                  / \\   ..  / \\     | \n|           - Quit -              /   }  .. {    \\    | \n|                                 ^+._/\\ .. /\\_.+^   | \n|        copyright 2020                 \\__/         | \n|____________________________________________________| \n'
                       
    title_screen_selections()
def help_menu():
    c()
    print('############################               ')
    print('#       -' + Fore.CYAN + ' HELP' + Fore.WHITE +' -          #')
    print('############################               ')
    print('                                           ')
    print('Use up down left right to move\n           ')
    print('Type commands to use them\n                ')
    print('Use "look" to inspect\n                    ')
    print('And most importantly be careful out there\n')
    print('type menu to go back ---->\n')
    title_screen_selections()

##### GAME FUNCTIONALITY #####
location = 24
def start_game():
    c()
    print("             ")
    print("             ")
    print("             ")
    print("      " + Fore.YELLOW + "@"+ Fore.WHITE +"      ")
    print("             ")
    print("             ")
    print("             ")
    World_screen()
def World_screen():
    global location
    rightlocations = [6,13,20,27,34,41,48,49,53]
    leftlocations =  [-5,-1,0,7,14,21,28,35,42,43,47]
    option = str(msvcrt.getwch())
    if option.lower() == ("w"):
        location -= 7
        if location < 0:
            print("")
            location +=7
            World()
        else:
            World()
    elif option.lower() == ("s"):
        location += 7
        if location > 48:
            print("")
            location -=7
            World()
        else:
            World()
    elif option.lower() == ("a"):
        if location not in leftlocations:
            location -= 1
            World()
        elif location in leftlocations:
            location -= 0
            World()
        else:
            print('INVALID')
            World_screen()
    elif option.lower() == ("d"):
        if location not in rightlocations:
            location += 1
            World()
        elif location in rightlocations:
            location -= 0
            World()
        else:
            print ('INVALID')
            World_screen()
    else:
        print ('INVALID')
        World_screen()
def World():
    c()
    global location
    amount = location
    World = ['0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               '0','0','0','0','0','0','0',
               ]
    RiverLocations = [2,10,11,19,27]
    river = Fore.BLUE + '~' + Fore.WHITE
    World[2] = river
    World[10] = river
    World[11] = river
    World[19] = river
    World[27] = river

    World[amount] = Fore.YELLOW +'@'+ Fore.WHITE
    for i in range(len(World)):
        print(World[i])

    print (World[0], World[1], World[2], World[3], World[4], World[5], World[6],)
    print (World[7], World[8], World[9], World[10],World[11],World[12],World[13],)    
    print (World[14],World[15],World[16],World[17],World[18],World[19],World[20],)
    print (World[21],World[22],World[23],World[24],World[25],World[26],World[27],)
    print (World[28],World[29],World[30],World[31],World[32],World[33],World[34],)
    print (World[35],World[36],World[37],World[38],World[39],World[40],World[41],)
    print (World[42],World[43],World[44],World[45],World[46],World[47],World[48],)
    Fore.WHITE
    if location in RiverLocations:
        RIVER()
    World_screen()
def Actions():
    global location
    rightlocations = [6,13,20,27,34,41,48,49,53]
    leftlocations =  [-5,-1,0,7,14,21,28,35,42,43,47]
    option = input("Action->")
    if option.lower() == ("examine"):
        print('you look around')
    elif option.lower() == ("up"):
        location -= 7
        if location < 0:
            print("")
            location +=7
            World()
        else:
            World()
    elif option.lower() == ("down"):
        location += 7
        if location > 48:
            print("")
            location -=7
            World()
        else:
            World()
    elif option.lower() == ("left"):
        if location not in leftlocations:
            location -= 1
            World()
        elif location in leftlocations:
            location -= 0
            World()
        else:
            print('INVALID')
            World_screen()
    elif option.lower() == ("right"):
        if location not in rightlocations:
            location += 1
            World()
        elif location in rightlocations:
            location -= 0
            World()
        else:
            print ('INVALID')
            World_screen()
    else:
        print ('INVALID')
        World_screen()
##### CONTENT #####
def RIVER():
    print("A river of sizeable width sparkles back at you ")
    Actions()
###################
title_screen()


######## MONSTER OF THE DEEPEST DEPTHS ########
#                        ,_   .'.    ,
#                   __..'`;`-' | `--;|
#                  `\._ `\.`.  `\   |`._./:
#                   /_.`>.-~"""`~-. |   ;'   _,
#             `\..-' .-',/  <_|<| |>-.  | `""/
#               |`"7'/'  _.----..<  <|`.;   /:
#            __.' /,/ ./'        `\.` ; `. ;  `>
#           `\--":/ .'              ` \`\ \  .'
#          .__. :;.'     .-"""-.     _..   \/
#   ,/'     | / /   ,  :       `. /'.--'   |
# /'/       <; /    |`\ \    _.._:|/   /\  |
# :  :       / /     :  `-'" <     \ ' (_o|/
# :`\.\-._.-' '   j  `\.      `\.__  _  \  |
#  \`-.        _.' `.__/          \/'._\,  `\
#   /  ,  _.-""                    `\\ 7-. o `>
#  :  /,-'                          ,/ `\ `--'
#   \ ||                            `-~-" 
#    `\_\ 