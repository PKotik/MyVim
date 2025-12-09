import sys
sys.path.append('..')
from service.libs.mystring import MyString as MyString

class DocumentModel:
    def __init__(self, fileName: str):
        self.__fileName = fileName
        self.__currentString = -1
        self.__modified = False
        try:
            with open(fileName, "r", encoding="utf-8") as f:
                self.__lines = f.read().splitlines()
        except FileNotFoundError:
            self.__lines = []
        if (len(self.__lines)==0):
            self.__lines.append(MyString())
        self.__countLines = len(self.__lines)

    def getLine(self) -> MyString:
        text = self.__lines[self.__currentString]
        return MyString(text)
    
    def getLineN(self, num: int) -> MyString:
        idx = num
        if idx < 0 or idx >= len(self.__lines):
            return MyString()
        return MyString(self.__lines[idx])
    
    def getLineLen(self, num: int) -> int:
        idx = num
        if idx < 0 or idx >= len(self.__lines):
            return 0
        return len(self.__lines[idx])

    def getNumLine(self) -> int:
        return self.__currentString
    
    def getLinesCount(self) -> int:
        return self.__countLines

    def setLine(self, numString: int, newStr: MyString) -> MyString:
        idx = numString
        if idx < self.__countLines:
            self.__lines[idx] = newStr.c_str()
        elif idx >= self.__countLines:
            while len(self.__lines) < idx:
                self.__lines.append("")
                self.__countLines+=1
            self.__lines.append(newStr.c_str())
            self.__countLines+=1
        self.__currentString = numString
        self.__modified = True

    def nextLine(self) -> MyString:
        if self.__currentString < self.__countLines-1:
            self.__currentString += 1
            return self.getLine()
        else:
            return None

    def prevLine(self) -> MyString:
        if self.__currentString >= 0:
            self.__currentString -= 1
            return self.getLine()
        else:
            return None

    
    def save(self) -> None:
        try:
            with open(self.__fileName, "w", encoding="utf-8") as f:
                f.write("\n".join(self.__lines))
            self.__modified = False
        except:
            None

    def saveIn(self, fileName: str) -> None:
        try:
            with open(fileName, "w", encoding="utf-8") as f:
                f.write("\n".join(self.__lines))
        except:
            None

    def is_modified(self) -> bool:
        return self.__modified
    
    def fileName(self) -> bool:
        return self.__fileName
    
    def openFile(self, fileName: str):
        self.__fileName = fileName
        self.__currentString = -1
        try:
            with open(fileName, "r", encoding="utf-8") as f:
                self.__lines = f.read().splitlines()
        except FileNotFoundError:
            self.__lines = []

        self.__countLines = len(self.__lines)