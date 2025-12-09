import sys
sys.path.append('..')
from model.DocumentModel import DocumentModel
from service.enums.ModeEnum import Mode
from service.libs.mystring import MyString as MyString
from typing import Tuple

class MainModel:
        def __init__(self, documentModel: DocumentModel):
                self.__documentModel = documentModel
                self.__currentX = documentModel.getLinesCount() - 1
                self.__currentY = documentModel.getLineLen(self.__currentX)
                self.__mode = Mode.NORMAL
                self.__sysBuffer = MyString()

        def pushBuffer(self, str: MyString):
                self.__sysBuffer = str

        def getBuffer(self) -> MyString:
                return self.__sysBuffer

        def documentModel(self) -> DocumentModel:
                return self.__documentModel

        def currentX(self) -> int:
                return self.__currentX
        
        def currentY(self) -> int:
                return self.__currentY
        
        def setCurrentY(self, y: int):
                self.__currentY = y
                if self.__currentY < 0:
                        self.__currentY = 0
                elif self.__currentY > self.__documentModel.getLineLen(self.__currentX):
                        self.__currentY = self.__documentModel.getLineLen(self.__currentX)
        
        def currentXUp(self):
                if self.__currentX > 0:
                        self.__currentX-=1
                if self.__currentY > self.__documentModel.getLineLen(self.__currentX)-1:
                        self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                if self.__currentY<0:
                        self.__currentY = 0
                return False

        def currentXDown(self):
                if self.__currentX < self.__documentModel.getLinesCount()-1:
                        self.__currentX+=1
                else:
                        self.__currentX+=1
                if self.__currentY > self.__documentModel.getLineLen(self.__currentX)-1:
                        self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                if self.__currentY<0:
                        self.__currentY = 0
                return False
        
        def currentYLeft(self):
                if self.__currentY > 0:
                        self.__currentY-=1
                return False

        def currentYRight(self):
                if self.__currentY < self.__documentModel.getLineLen(self.__currentX):
                        self.__currentY+=1
                return False

        def currentYMin(self):
                self.__currentY = 0
                return False

        def currentYMax(self):
                self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                return False

        def currentYRightWord(self):
                save = self.__currentY
                self.__currentY = self.__documentModel.getLineN(self.__currentX).find(' ', self.__currentY + 1)
                if save == self.__currentY or self.__currentY == -1:
                        self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                        return False
                while self.__documentModel.getLineN(self.__currentX)[self.__currentY - 1] == ' ':
                        self.__currentY = self.__documentModel.getLineN(self.__currentX).find(' ', self.__currentY + 1)
                        if self.__currentY == -1:
                                self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                return False

        def currentYLeftWord(self):
                while self.__currentY > 0 and self.__documentModel.getLineN(self.__currentX)[self.__currentY - 1] == ' ':
                        self.__currentY-=1
                while self.__currentY > 0 and self.__documentModel.getLineN(self.__currentX)[self.__currentY - 1] != ' ':
                        self.__currentY-=1
                return False
        
        def currentWord(self, num: int) -> Tuple[int, int]:
                index = self.__currentY
                start = index
                end = index
                str = self.__documentModel.getLineN(self.__currentX)
                while start != 0 and str[start] != ' ':
                        start -= 1
                while end < self.__documentModel.getLineLen(self.__currentX) and str[end] != ' ':
                        end += 1
                if start != 0:
                        start+=1
                return (start, end)
        
        def currentWordStr(self, num: int) -> MyString:
                start, end = self.currentWord(num)
                return MyString(self.__documentModel.getLineN(self.__currentX).c_str()[start:end])
        
        def delete(self, currentStr: int, startDel: int, countDel: int):
                if (currentStr >= self.__documentModel.getLinesCount() or self.__documentModel.getLineN(currentStr).empty()):
                        return
                str = self.__documentModel.getLineN(currentStr)
                str.erase(startDel, countDel)
                self.__documentModel.setLine(currentStr,str)
                
        def currentStart(self):
                self.__currentX=0
                self.__currentY=0
                return False

        def currentEnd(self):
                self.__currentX=self.__documentModel.getLinesCount()-1
                self.__currentY=self.__documentModel.getLineLen(self.__currentX)
                return False
        
        def gotoLine(self, num: int):
                self.__currentX = num - 1
                if self.__currentX < 0:
                        self.__currentX = 0
                        return False
                if self.__currentY > self.__documentModel.getLineLen(self.__currentX)-1:
                        self.__currentY = self.__documentModel.getLineLen(self.__currentX)
                if self.__currentY < 0:
                        self.__currentY = 0
                return False
                
        def mode(self) -> Mode:
                return self.__mode
        
        def setMode(self, mode: Mode):
                self.__mode = mode
        