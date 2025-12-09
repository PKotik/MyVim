import sys
sys.path.append('..')
from service.libs.mystring import MyString as MyString

class StringDto:
    def __init__(self, string: MyString, x: int):
        self.string = string
        self.x = x