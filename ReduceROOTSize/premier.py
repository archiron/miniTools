#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import math as m

version = '1.3.0'

def screen_clear():
    # The screen clear function
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')

def changeColor(color):
    # 30:noir ; 31:rouge; 32:vert; 33:orange; 34:bleu; 35:violet; 36:turquoise; 37:blanc
    # other references at https://misc.flogisoft.com/bash/tip_colors_and_formatting
    if (color == 'black'):
        return '[30m'
    elif (color == 'red'):
        return '[31m'
    elif (color == 'green'):
        return '[32m'
    elif (color == 'orange'):
        return '[33m'
    elif (color == 'blue'):
        return '[34m'
    elif (color == ''):
        return '[35m'
    elif (color == 'purple'):
        return '[36m'
    elif (color == 'turquoise'):
        return '[37m'
    elif (color == 'lightyellow'):
        return '[93m'
    else:
        return '[30m'

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

class Premier():
    def __init__(self, txt):
        print('begin to run with version %s' % colorText(str(version), 'blue'))
        #print('texte : %s' % txt)
    def premier_1(self): # , txt
        N = 2021
        N2 = int(m.sqrt(N))
        for i in range(2, N2):
            a = int(N/i)
            b = N % i
            if (b == 0):
                #print('\ni = %d' % i)
                #print('%d = %d * %d + %d' % (N, a, i, b))
                print('%d = %d * %d' % (N, a, i))
                print('decomposition')

if __name__ == '__main__':
    P = Premier(version)
    P.premier_1() # version
    print('... End')

