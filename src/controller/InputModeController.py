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

class InputModeController:
        def __init__(self, model: MainModel, view: MainView):
            self.__model = model
            self.__documentModel = model.documentModel()
            self.__view = view
            self.__run = True
            self.__commandsList = {
                "ESC": self.exit,
                "\x1b": self.exit,
            }


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

        def run(self):
            self.draw(True)
            while self.__run:
                key = self.__view.get_key_await()
                if key in self.__commandsList:
                    f = self.__commandsList[key]()
                    self.__searchStr = ""
                    self.draw(f)
                    continue
                if len(key) == 1:
                    self.inputChar(key)
                    self.draw(True)

        def inputChar(self, key: MyString):
            str = self.__documentModel.getLineN(self.__model.currentX())
            str.insert(self.__model.currentY(), key)
            self.__documentModel.setLine(self.__model.currentX(), str)
            self.__model.currentYRight()
            return True
        
        def exit(self):
            self.__run = False
            self.__model.setMode(Mode.NORMAL)