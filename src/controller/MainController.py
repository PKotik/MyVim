import sys
sys.path.append('..')
from service.libs.mystring import MyString as MyString
from model.DocumentModel import DocumentModel
from model.MainModel import MainModel
from view.MainView import MainView
from service.libs.mystring import MyString as MyString
from service.dto.InterfaceDto import InterfaceDto
from service.dto.StringDto import StringDto
from service.dto.CursorDto import CursorDto
from service.enums.ModeEnum import Mode
from controller.SearchModeController import SearchModeController
from controller.InputModeController import InputModeController
from controller.CommandModeController import CommandModeController
                    
class MainController:
    def __init__(self, model: MainModel, view: MainView):
        self.__model = model
        self.__documentModel = model.documentModel()
        self.__view = view
        self.__run = True
        self.__view.run()
        self.__commandsList = {
            "f": self.reDraw,
            "KEY_RIGHT": self.__model.currentYRight,
            "KEY_LEFT": self.__model.currentYLeft,
            "KEY_UP": self.__model.currentXUp,
            "KEY_DOWN": self.__model.currentXDown,
            "^": self.__model.currentYMin,
            "0": self.__model.currentYMin,
            "$": self.__model.currentYMax,
            "w": self.__model.currentYRightWord,
            "b": self.__model.currentYLeftWord,
            "gg": self.__model.currentStart,
            "G": self.__model.currentEnd,
            "KEY_PGUP": self.page_up,
            "KEY_PGDN": self.page_down,
            "x": self.deleteChar,
            "diw": self.deleteWord,
            "dd": self.putStr,
            "yy": self.copyStr,
            "yw": self.copyWord,
            "p": self.paste,
            "/": self.goToSearchToEndMode,
            "?": self.goToSearchToStartMode,
            "i": self.goToInputHere,
            "I": self.goToInputStart,
            "A": self.goToInputEnd,
            "S": self.goToInputIns,
            "r": self.goToInputInsChar,
            ":": self.goToCommandMode
        }

    def goToCommandMode(self):
        self.__model.setMode(Mode.COMMAND)
        commandController = CommandModeController(self.__model, self.__view)
        commandController.run()
        if commandController.needExit():
            self.__run = False
            self.__view.cleanup()
            sys.exit(0)
        return True


    def goToInputHere(self):
        self.__model.setMode(Mode.INPUT)
        inputController = InputModeController(self.__model, self.__view)
        inputController.run()
        return True

    def goToInputStart(self):
        self.__model.setMode(Mode.INPUT)
        self.__model.currentYMin()
        inputController = InputModeController(self.__model, self.__view)
        inputController.run()
        return True

    def goToInputEnd(self):
        self.__model.setMode(Mode.INPUT)
        self.__model.currentYMax()
        inputController = InputModeController(self.__model, self.__view)
        inputController.run()
        return True

    def goToInputIns(self):
        self.__model.setMode(Mode.INPUT)
        self.__model.delete(self.__model.currentX(), 0, self.__documentModel.getLineLen(self.__model.currentX()))
        self.__model.currentYMin()
        inputController = InputModeController(self.__model, self.__view)
        inputController.run()
        return True

    def goToInputInsChar(self):
        if self.__model.currentY() >= self.__documentModel.getLineLen(self.__model.currentX()):
            return False
        self.__model.setMode(Mode.INPUT)
        self.draw(False)
        key = self.__view.get_key_await()
        if len(key) == 1:
            str = self.__documentModel.getLineN(self.__model.currentX())
            str[self.__model.currentY()] = key
            self.__documentModel.setLine(self.__model.currentX(), str)
        self.__model.setMode(Mode.NORMAL)
        return True


    def goToSearchToEndMode(self):
        self.__model.setMode(Mode.SEARCH)
        searchController = SearchModeController(True, self.__model, self.__view)
        searchController.run()
        return True

    def goToSearchToStartMode(self):
        self.__model.setMode(Mode.SEARCH)
        searchController = SearchModeController(False, self.__model, self.__view)
        searchController.run()
        return True

    def run(self):
        view = self.__view
        self.draw(True)
        buf = ""
        while self.__run:
            buf += view.get_key_await()
            if buf in self.__commandsList:
                self.draw(self.__commandsList[buf]())
                buf = ""
                continue
            if buf.isdigit():
                continue
            if buf[:-1].isdigit():
                if buf.endswith("G"):
                    line_num = int(buf[:-1])
                    self.draw(self.__model.gotoLine(line_num))
                    buf = ""
                    continue
                buf = ""
                continue
            if any(cmd.startswith(buf) for cmd in self.__commandsList):
                continue
            buf = ""
        
    def reDraw(self):
        self.draw(True)

    def draw(self, needRedrawText: bool = False):
        dtoCursor = CursorDto(self.__model.currentX(), self.__model.currentY())
        if (self.__view.fix_screen(dtoCursor)):
            needRedrawText = True
        if needRedrawText:
            self.__view.clear()
            text: list[StringDto] = []
            for i in range(self.__view.page_start(), self.__view.page_end()):
                if i >= self.__documentModel.getLinesCount():
                    break
                line = self.__documentModel.getLineN(i)
                dto = StringDto(line, i)
                text.append(dto)
            self.__view.draw_text(text)
        self.__view.draw_interface(InterfaceDto(MyString(self.__model.mode().name), MyString(self.__documentModel.fileName()), self.__model.currentX(), self.__documentModel.getLinesCount()))
        self.__view.draw_cursor(dtoCursor, True)
        

    def page_up(self):
        if self.__view.page_up():
            self.__model.gotoLine(self.__model.currentX() - self.__view.page_size() + 1)
            return True
        return False
    
    def page_down(self):
        if self.__view.page_down():
            self.__model.gotoLine(self.__model.currentX() + self.__view.page_size() + 1)
            return True
        return False

    def deleteChar(self):
        if (self.__documentModel.getLineLen(self.__model.currentX()) <= self.__model.currentY()):
            return False
        self.__model.delete(self.__model.currentX(), self.__model.currentY(), 1)
        return True
    
    def deleteWord(self):
        if not(self.__model.currentX() > self.__documentModel.getLinesCount()):
            start, end = self.__model.currentWord(self.__model.currentX())
            if end < self.__documentModel.getLineLen(self.__model.currentX()):
                end+=1
            self.__model.delete(self.__model.currentX(), start, end-start)
            return True
        return False
    
    def putStr(self):
        if (self.__model.currentX() > self.__documentModel.getLinesCount() or self.__documentModel.getLineN(self.__model.currentX()).isNull()):
            return False
        self.__model.pushBuffer(self.__documentModel.getLineN(self.__model.currentX()))
        self.__model.delete(self.__model.currentX(), 0, self.__documentModel.getLineLen(self.__model.currentX()))
        self.__model.currentYMin()
        return True
    
    def copyStr(self):
        if not(self.__model.currentX() > self.__documentModel.getLinesCount()):
            self.__model.pushBuffer(self.__documentModel.getLineN(self.__model.currentX()))
        return False
    
    def copyWord(self):
        if not(self.__model.currentX() > self.__documentModel.getLinesCount()):
            str = self.__model.currentWordStr(self.__model.currentX())
            self.__model.pushBuffer(str)
        return False
    
    def paste(self):
        str = self.__documentModel.getLineN(self.__model.currentX())
        str.insert(self.__model.currentY(), self.__model.getBuffer())
        self.__documentModel.setLine(self.__model.currentX(), str)
        return True
        

                        





