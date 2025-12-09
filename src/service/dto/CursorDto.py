import sys
sys.path.append('..')
from service.libs.mystring import MyString as MyString

class CursorDto:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
                