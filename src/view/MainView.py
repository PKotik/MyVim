import sys
import threading
import queue
from typing import List  
sys.path.append('..')
from service.graphics.CursesService import CursesService
from service.enums.ColorEnum import Color
from service.libs.mystring import MyString as MyString
from service.dto.InterfaceDto import InterfaceDto
from service.dto.StringDto import StringDto
from service.dto.CursorDto import CursorDto


class MainView:
        def __init__(self):
                self.curses_service = CursesService()
                self.curses_service.init()
                self.__key_queue = queue.Queue(maxsize=10)
                height, width = self.curses_service.get_screen_size() 
                self.__currentHight = height-1
                self.__currentFirst = 0

        def run(self):
                threading.Thread(target=self.__reading_keys, daemon=True).start()

        def __del__(self):
                self.cleanup()

        def cleanup(self):
                self.curses_service.cleanup()
    
        def draw_interface(self, dto : InterfaceDto, needRefresh: bool = False):
                height, width = self.curses_service.get_screen_size() 
                status = f"{dto.modeName.c_str()} MODE | {dto.fileName.c_str()} | string: {dto.currentString}/{dto.countStrings} | page: {self.__currentFirst//self.__currentHight}"
                self.curses_service.add_str(height-1, 0, status.ljust(width), 
                                  Color.BLACK, Color.WHITE)
                if needRefresh:
                        self.curses_service.refresh()

        def clear(self):
                self.curses_service.clear()

        def draw_text(self, dtos: List[StringDto], needRefresh: bool = False):
                for dto in dtos:
                        self.curses_service.add_str(dto.x - self.__currentFirst,0,dto.string.c_str())
                if needRefresh:
                        self.curses_service.refresh()

        def draw_cursor(self, dto: CursorDto, needRefresh: bool = False) :
                self.curses_service.set_cursor(dto.x - self.__currentFirst, dto.y)
                if needRefresh:
                        self.curses_service.refresh()

        def fix_screen(self, dto: CursorDto) -> bool:
                flag = False
                while (dto.x - self.__currentFirst > self.__currentHight - 1):
                        self.page_down()
                        flag = True
                while (dto.x - self.__currentFirst < 0):
                        self.page_up()
                        flag = True
                return flag

        def draw_all(self, dtoDoc : InterfaceDto, dtoStr: List[StringDto], dtoCursor: CursorDto, needRefresh: bool = False):
                self.draw_interface(dtoDoc)
                self.draw_text(dtoStr)
                self.draw_cursor(dtoCursor)
                if needRefresh:
                        self.curses_service.refresh()

        def get_key(self):
                try:
                        key = self.__key_queue.get_nowait()
                except queue.Empty:
                        key = None
                return key
        
        def get_key_await(self):
                return self.__key_queue.get()

        def __reading_keys(self):
                while True:
                        key = self.curses_service.get_key()
                        self.__key_queue.put(key)
        
        def page_down(self):
                self.__currentFirst += self.__currentHight
                return True

        def page_up(self):
                if self.__currentFirst > 0:
                        self.__currentFirst -= self.__currentHight
                        return True
                return False
        
        def page_start(self) -> int:
                return self.__currentFirst
        
        def page_end(self) -> int:
                return self.__currentFirst + self.__currentHight
        
        def page_size(self) -> int:
                return self.__currentHight