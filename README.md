qcmenu
======

This package offers a simple menu interface build on top of curses library.

Install
-------

Manually download and install the last version from github
```bash
$ git clone https://github.com/corwin-31/qcmenu.git
$ python setup.py install
```

Get started
-----------
```python
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
```
Have a look on the [testqcm.py] (https://github.com/corwin-31/qcmenu/blob/master/testqcm.py) for a more complete overview

