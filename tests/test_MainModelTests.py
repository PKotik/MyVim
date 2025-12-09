import pytest
import sys
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from service.libs.mystring import MyString as MyString
from model.DocumentModel import DocumentModel
from model.MainModel import MainModel


def testStartCursor(tmp_path):
    file = tmp_path / "testasdsad.txt"
    file.write_text("hello\nworld\n\n\n\n1212 211 1212 2232 23 2\n\n\n\n\n\n23232323")
    docModel = DocumentModel(str(file))
    model = MainModel(docModel)
    
    assert model.currentX() == 11
    assert model.currentY() == 8

def testGoToStartEndCursor(tmp_path):
    file = tmp_path / "testasdsad.txt"
    file.write_text("hello\nworld\n\n\n\n1212 211 1212 2232 23 2\n\n\n\n\n\n23232323")
    docModel = DocumentModel(str(file))
    model = MainModel(docModel)
    
    model.currentStart()
    assert model.currentX() == 0
    assert model.currentY() == 0

    model.currentEnd()
    assert model.currentX() == 11
    assert model.currentY() == 8

def testGoToLine(tmp_path):
    file = tmp_path / "testasdsad.txt"
    file.write_text("hello\nworld\n\n\n\n1212 211 1212 2232 23 2\n\n\n\n\n\n23232323")
    docModel = DocumentModel(str(file))
    model = MainModel(docModel)

    model.gotoLine(6)
    assert model.currentX() == 5
    assert model.currentY() == 8

    model.gotoLine(4)
    assert model.currentX() == 3
    assert model.currentY() == 0

def testGoToWord(tmp_path):
    file = tmp_path / "testasdsad.txt"
    file.write_text("1d2   2s3 2 3")
    docModel = DocumentModel(str(file))
    model = MainModel(docModel)

    assert model.currentY() == 13
    model.currentYLeftWord()
    assert model.currentY() == 12
    model.currentYLeftWord()
    assert model.currentY() == 10
    model.currentYLeftWord()
    assert model.currentY() == 6
    model.currentYLeftWord()
    assert model.currentY() == 0
    model.currentYLeftWord()
    assert model.currentY() == 0
    
    model.currentYRightWord()
    assert model.currentY() == 3
    model.currentYRightWord()
    assert model.currentY() == 9
    model.currentYRightWord()
    assert model.currentY() == 11
    model.currentYRightWord()
    assert model.currentY() == 13
    model.currentYRightWord()
    assert model.currentY() == 13

    


