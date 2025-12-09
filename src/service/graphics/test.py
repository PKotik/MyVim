import curses

class Screen:
    def clear(self): ...
    def refresh(self): ...
    def draw_text(self, x, y, text): ...
    def move_cursor(self, x, y): ...
    def read_key(self): ...
    def size(self): ...

class CursesScreen(Screen):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1)
        self.stdscr.keypad(True)

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def draw_text(self, x, y, text):
        try:
            self.stdscr.addstr(y, x, text)
        except curses.error:
            pass  # игнор, если выходит за границы

    def move_cursor(self, x, y):
        try:
            self.stdscr.move(y, x)
        except curses.error:
            pass

    def read_key(self):
        return self.stdscr.getch()

    def size(self):
        return self.stdscr.getmaxyx()


class KeyInput:
    ESC = 27
    ENTER = 10
    BACKSPACE = 127

    ARROW_UP = "UP"
    ARROW_DOWN = "DOWN"
    ARROW_LEFT = "LEFT"
    ARROW_RIGHT = "RIGHT"

    @staticmethod
    def normalize(key):
        if key == curses.KEY_UP: return KeyInput.ARROW_UP
        if key == curses.KEY_DOWN: return KeyInput.ARROW_DOWN
        if key == curses.KEY_LEFT: return KeyInput.ARROW_LEFT
        if key == curses.KEY_RIGHT: return KeyInput.ARROW_RIGHT

        if key == 10: return KeyInput.ENTER
        if key in (8, 127): return KeyInput.BACKSPACE

        if key == 27: return KeyInput.ESC

        try:
            return chr(key)
        except:
            return None


class StatusBar:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.text = ""

    def set(self, mode, filename, line, total):
        self.text = f"-- {mode} --  {filename}  {line}/{total}"

    def draw(self):
        h, w = self.screen.size()
        line = self.text[:w]
        self.screen.draw_text(0, h - 1, line)

class TextWindow:
    def __init__(self, screen: Screen):
        self.screen = screen

    def draw_buffer(self, lines, cursor_x, cursor_y):
        self.screen.clear()

        for i, line in enumerate(lines):
            self.screen.draw_text(0, i, line)

        self.screen.move_cursor(cursor_x, cursor_y)

def main(stdscr):
    screen = CursesScreen(stdscr)
    status = StatusBar(screen)
    window = TextWindow(screen)

    lines = ["Hello", "world"]
    cursor_x = 0
    cursor_y = 0

    while True:
        window.draw_buffer(lines, cursor_x, cursor_y)
        status.set("NORMAL", "demo.txt", cursor_y + 1, len(lines))
        status.draw()
        screen.refresh()

        key = KeyInput.normalize(screen.read_key())

        if key == KeyInput.ESC:
            break

        if key == KeyInput.ARROW_DOWN and cursor_y < len(lines) - 1:
            cursor_y += 1

        if key == KeyInput.ARROW_UP and cursor_y > 0:
            cursor_y -= 1

        if key == KeyInput.ARROW_RIGHT:
            cursor_x += 1

        if key == KeyInput.ARROW_LEFT and cursor_x > 0:
            cursor_x -= 1


curses.wrapper(main)