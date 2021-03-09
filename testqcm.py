#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:26:54 2020

"""

from qcmenu import QCMenu

def myMain(myMenu):
    exTxt = []
    
    mainMenu = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eigth', 'nine', 'ten' ]
    menuLevel = 'Main'
    exTxt = []
    for i in range(1,100): exTxt.append('Line {0}'.format(i))

    while True:
        if menuLevel == 'Main': curMenu = mainMenu
        userSelect = myMenu.QCMmenu(curMenu, menuLevel)
        if menuLevel == 'Main':
            if userSelect == 'Quit': break
            else:
                myMenu.QCMdisplay(exTxt,menuLevel + '>' + userSelect)

# Main

gMenu = QCMenu()
gMenu.QCMstart(myMain)
