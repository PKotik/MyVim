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

class SearchModeController:
        def __init__(self, toEnd: bool, model: MainModel, view: MainView):
            self.__toEnd = toEnd
            self.__model = model
            self.__documentModel = model.documentModel()
            self.__view = view
            self.__run = True
            self.__searchStr = MyString()
            self.__saveSearch = MyString()
            self.__commandsList = {
                "ENTER": self.search,
                "\n": self.search,
                "\r": self.search,
                "ESC": self.exit,
                "\x1b": self.exit,
                "n": self.repSearch,
                "N": self.revSearch
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
            self.__view.draw_interface(InterfaceDto(MyString(f"«{self.__searchStr}» {self.__model.mode().name}"), MyString(self.__documentModel.fileName()), self.__model.currentX(), self.__documentModel.getLinesCount()))
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
                    self.__searchStr += key
                    self.draw(False)

        def exit(self):
            self.__run = False
            self.__model.setMode(Mode.NORMAL)
            

        def search(self):
            if self.__toEnd:
                self.searchToEnd(self.__searchStr)
            else:
                self.searchToStart(self.__searchStr)

        def repSearch(self):
            if self.__toEnd:
                self.searchToEnd(self.__saveSearch)
            else:
                self.searchToStart(self.__saveSearch)

        def revSearch(self):
            if self.__toEnd:
                self.searchToStart(self.__saveSearch)
            else:
                self.searchToEnd(self.__saveSearch)
        
        def searchToEnd(self, str: MyString):
            self.__saveSearch = str
            y = self.__model.currentY()
            x = self.__model.currentX()
            find = -1
            while (x < self.__documentModel.getLinesCount() and find == -1):
                find = self.__documentModel.getLineN(x).find(str, y + 1)
                y = -1
                x += 1
            if find != -1:
                self.__model.gotoLine(x)
                self.__model.setCurrentY(find)
            return False
        
        def searchToStart(self, pattern: MyString):
            self.__saveSearch = pattern

            cur_line = self.__model.currentX()
            cur_col = self.__model.currentY()

            doc = self.__documentModel
            line = doc.getLineN(cur_line)
            pos = self.__rfind_mystring(line, pattern, upto=cur_col)

            if pos != -1:
                self.__model.setCurrentY(pos)
                return True
            x = cur_line - 1
            while x >= 0:
                line = doc.getLineN(x)
                pos = self.__rfind_mystring(line, pattern, upto=None)
                if pos != -1:
                    self.__model.gotoLine(x + 1)
                    self.__model.setCurrentY(pos)
                    return True
                x -= 1

            return False

                
        def __rfind_mystring(self, line: MyString, pattern: MyString, upto: int | None):
            last = -1
            start = 0
            while True:
                pos = line.find(pattern, start)
                if pos == -1:
                    break
                if upto is not None and pos >= upto:
                    break
                last = pos
                start = pos + 1
            return last
