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

class CommandModeController:
        def __init__(self, model: MainModel, view: MainView):
            self.__model = model
            self.__documentModel = model.documentModel()
            self.__view = view
            self.__needExit = False
            self.__run = True
            self.__command = MyString("")
            self.__commandsList = {
                "ESC": self.exit,
                "\x1b": self.exit,
                "o ": self.waitFileNameOpen,
                "x\n": self.SaveAndExit,
                "w\n": self.Save,
                "w ": self.waitFileNameSave,
                "q\n": self.closeFile,
                "q!\n": self.closeFileWithoutSave,
                "wq!\n": self.SaveAndExit,
                "h": self.help
            }

        def help(self):
            str = MyString("o - «filename» Открыть файл filename\nx - Записать в текущий файл и выйти\nw - Записать в текущий файл\nw «filename» - Записать в filename\nq - Выйти. Если файл был изменён, то выход возможен только через q!\n"+
                           "q! - Выйти без сохранения\nwq! - Записать в текущий файл и выйти\nnumber - Переход на строку numbe\nh - Вывести справку по командам")
            self.__view.clear()
            dto = StringDto(str, 0)
            text: list[StringDto] = [dto]
            self.__view.draw_text(text)
            self.__view.draw_interface(InterfaceDto(MyString(f"«{self.__command}» {self.__model.mode().name}"), MyString(self.__documentModel.fileName()), self.__model.currentX(), self.__documentModel.getLinesCount()))

        def closeFile(self):
            if self.__documentModel.is_modified():
                return False
            self.__needExit = True
            self.exit()

        def closeFileWithoutSave(self):
            self.__needExit = True
            self.exit()

        def SaveAndExit(self):
            self.__documentModel.save()
            self.__needExit = True
            self.exit()

        def Save(self):
            self.__documentModel.save()
            return False

        def waitFileNameSave(self):
            buf = ''
            while True:
                key = self.__view.get_key_await()
                if key in ("ENTER", "\n", "\r"):
                    break
                buf+=key
                self.__command += key
                self.draw(False)
            self.__documentModel.saveIn(buf)
            return False

        def waitFileNameOpen(self):
            buf = ''
            while True:
                key = self.__view.get_key_await()
                if key in ("ENTER", "\n", "\r"):
                    break
                buf+=key
                self.__command += key
                self.draw(False)
            self.__documentModel.openFile(buf)
            return True

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
            self.__view.draw_interface(InterfaceDto(MyString(f"«{self.__command}» {self.__model.mode().name}"), MyString(self.__documentModel.fileName()), self.__model.currentX(), self.__documentModel.getLinesCount()))
            self.__view.draw_cursor(dtoCursor, True)

        def run(self):
            view = self.__view
            self.__view.run()
            self.draw(True)
            buf = ""
            while self.__run:
                key = view.get_key_await()
                buf += key
                self.__command = buf
                self.draw(False)
                if buf in self.__commandsList:
                    if buf=="h":
                        self.help()
                        buf = ""
                        continue
                    f = self.__commandsList[buf]()
                    self.draw(f)
                    buf = ""
                    continue
                if buf.isdigit():
                    continue
                if buf[:-1].isdigit():
                    if key in ("ENTER", "\n", "\r"):
                        line_num = int(buf[:-1])
                        self.__model.gotoLine(line_num)
                        self.draw(True)
                        buf = ""
                        continue
                    buf = ""
                    continue
                if any(cmd.startswith(buf) for cmd in self.__commandsList):
                    continue
                buf = ""

        def exit(self):
            self.__run = False
            self.__model.setMode(Mode.NORMAL)

        def needExit(self) -> bool:
            return self.__needExit