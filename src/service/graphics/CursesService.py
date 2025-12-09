import sys
sys.path.append('..')
import curses
import locale
from typing import List, Tuple

from service.enums.ColorEnum import Color

class CursesService():
    def __init__(self):
        self.screen = None
    
    def init(self) -> None:
        locale.setlocale(locale.LC_ALL, '')
        self.screen = curses.initscr()
        curses.curs_set(1)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
    
    def cleanup(self) -> None:
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
    
    def get_screen_size(self) -> Tuple[int, int]:
        return self.screen.getmaxyx()
    
    def clear(self) -> None:
        self.screen.clear()
    
    def refresh(self) -> None:
        self.screen.refresh()
    
    def add_str(self, y: int, x: int, text: str, 
                fg: Color = Color.WHITE, bg: Color = Color.BLACK, 
                attributes: List[str] = None) -> None:
        try:
            self.screen.addstr(y, x, text)
        except:
            pass
    
    def add_str_centered(self, y: int, text: str,
                        fg: Color = Color.WHITE, bg: Color = Color.BLACK,
                        attributes: List[str] = None) -> None:
        height, width = self.get_screen_size()
        x = (width - len(text)) // 2
        self.add_str(y, x, text, fg, bg, attributes)
    
    def draw_box(self, y: int, x: int, height: int, width: int,
                fg: Color = Color.WHITE, bg: Color = Color.BLACK) -> None:
        pass
    
    def get_key(self) -> str:
        key = self.screen.get_wch()
        if isinstance(key, int):
            return self.__keycode_to_name(key)
        return key
    
    def set_cursor(self, y: int, x: int) -> None:
        self.screen.move(y, x)
    
    def hide_cursor(self) -> None:
        curses.curs_set(0)
    
    def show_cursor(self) -> None:
        curses.curs_set(1)

    def __keycode_to_name(self, code: int) -> str:
        mapping = {
            curses.KEY_UP: "KEY_UP",
            curses.KEY_DOWN: "KEY_DOWN",
            curses.KEY_LEFT: "KEY_LEFT",
            curses.KEY_RIGHT: "KEY_RIGHT",
            curses.KEY_NPAGE: "KEY_PGDN",
            curses.KEY_PPAGE: "KEY_PGUP",
            curses.KEY_HOME: "KEY_HOME",
            curses.KEY_END: "KEY_END",
            27: "ESC",
            10: "ENTER",
            13: "ENTER",
        }

        return mapping.get(code, f"KEY_{code}")