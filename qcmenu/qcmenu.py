import curses
from os import get_terminal_size
from qcmenu.exceptions import TerminalError

class QCMenu:
    def __init__(self):
        self.maxCol, self.maxRow = get_terminal_size(1)
        if self.maxCol < 25 or self.maxRow < 10: raise TerminalError('terminal too small')
    
    def _QCMcall_wrapper(self, lTerm, lProc, *args):
        self.localTerm = lTerm
        curses.use_default_colors()
        curses.curs_set(0)
        self.localTerm.immedok(True)
        self.displayWin = curses.newwin(self.maxRow - 1,self.maxCol,1,0)
        self.displayWin.immedok(True)
        self.displayWin.idlok(True)
        self.displayWin.scrollok(True)
        self.titleWin = curses.newwin(1,self.maxCol,0,0)
        self.titleWin.immedok(True)
        self.titleWin.bkgd(' ',curses.A_REVERSE)
        self.QCMtitle()
        lProc(self,*args)

    def QCMstart(self, userProc, *args):
        '''
        Just start curses on terminal by calling the wrapper
        '''
        curses.wrapper(self._QCMcall_wrapper, userProc, *args)
    
    def QCMtitle(self, newTitle = 'Main'):
        '''
        Display a new menu title
        '''
        self.titleWin.clear()
        self.titleWin.insstr(0,0,newTitle,self.maxCol)
    
    def QCMdisplay(self, allLines, newTitle = 'Main'):
        '''
        Display in main window
        '''
        self.QCMtitle(newTitle)
        self.displayWin.keypad(True)
        curRow = 1
        self.displayWin.move(0,0)
        lastLine = True
        for curLine in allLines:
            if lastLine: self.displayWin.clear()
            if curRow == (self.maxRow - 1):
                self.displayWin.addnstr(curLine, self.maxCol)
                curRow = 1
                self.displayWin.getch()
                lastLine = True
            else:
                self.displayWin.addnstr(curLine + '\n' , self.maxCol)
                curRow += 1
                lastLine = False
        if not lastLine: self.displayWin.getch()
    
    def QCMmenu(self, userTopics, newTitle = 'Main'):
        '''
        Manage a menu
        '''
        self.QCMtitle(newTitle)
        menuTopics = userTopics + [ 'Quit' ]
        nbTopics = len(menuTopics)
        maxLength = 0
        for topic in menuTopics:
            if len(topic) > maxLength: maxLength = len(topic)
        maxLength = min(maxLength, self.maxCol - 4)
        subMenu = curses.newwin(min(nbTopics, self.maxRow - 1), maxLength + 2, 1, 2)
        subMenu.immedok(True)
        subMenu.keypad(True)
        subMenu.bkgd(' ', curses.A_REVERSE)
        select = 0
        startTopic = 0
        endTopic = min(nbTopics, self.maxRow - 1)
        for i in range(startTopic, endTopic):
            if i == select: subMenu.insnstr(i, 0, '<' + menuTopics[i] + '>', maxLength + 2, curses.A_BOLD)
            else: subMenu.insnstr(i, 0, ' ' + menuTopics[i], maxLength + 1)
        while True:
            subMenu.move(0, 0)
            userKey = subMenu.getch()
            if userKey == curses.KEY_UP:
                if select == 0:
                    select = nbTopics - 1
                    endTopic = nbTopics
                    startTopic = endTopic - min(nbTopics, self.maxRow - 1)
                else:
                    select -= 1
                    if select < startTopic:
                        startTopic -= 1
                        endTopic -= 1
            elif userKey == curses.KEY_DOWN:
                if select == (nbTopics - 1):
                    select = 0
                    startTopic = 0
                    endTopic = min(nbTopics, self.maxRow - 1)
                else:
                    select += 1
                    if select == endTopic:
                        startTopic += 1
                        endTopic += 1
            elif userKey == curses.KEY_ENTER: break
            elif userKey == curses.KEY_RIGHT: break
            subMenu.clear()
            for i in range(startTopic, endTopic):
                if i == select: subMenu.insnstr(i - startTopic, 0, '<' + menuTopics[i] + '>', maxLength + 2, curses.A_BOLD)
                else: subMenu.insnstr(i - startTopic, 0, ' ' + menuTopics[i], maxLength + 1)
        self.displayWin.redrawwin()
        self.displayWin.refresh()
        return menuTopics[select]
