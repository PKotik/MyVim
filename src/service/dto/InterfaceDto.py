import sys
sys.path.append('..')
from service.libs.mystring import MyString as MyString

class InterfaceDto:
    def __init__(self, modeName: MyString, fileName : MyString, currentString : int, countStrings : int):
        self.modeName = modeName
        self.fileName = fileName
        self.currentString = currentString+1
        self.countStrings = countStrings
                