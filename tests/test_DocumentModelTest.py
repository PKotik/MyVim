import pytest
import sys
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from service.libs.mystring import MyString as MyString
from model.DocumentModel import DocumentModel
from model.MainModel import MainModel


def testGetLinesCount(tmp_path):
    file = tmp_path / "testasdsad.txt"
    file.write_text("hello\nworld\n\n\n\n1212 211 1212 2232 23 2\n\n\n\n\n\n23232323")
    docModel = DocumentModel(str(file))
    c = docModel.getLinesCount()
    assert c == 12

def testGetLinesLen(tmp_path):
    file = tmp_path / "testasddsadsadsdsa.txt"
    file.write_text("\n1\n22\n333\n4444\n55555\n666666\n7777777\n88888888\n999999999")
    docModel = DocumentModel(str(file))
    c = docModel.getLinesCount()
    assert c == 10
    for i in range(10):
        len = docModel.getLineLen(i)
        assert len == i

def testGetLine(tmp_path):
    file = tmp_path / "testassdfsdfsdsdsa.txt"
    file.write_text("\n1\n22\n333\n4444\n55555\n666666\n7777777\n88888888\n999999999")
    docModel = DocumentModel(str(file))
    c = docModel.getLinesCount()
    assert c == 10
    for i in range(10):
        st = docModel.getLineN(i)
        assert len(st) == i

def testSetLine(tmp_path):
    file = tmp_path / "testdsfsdfsae.txt"
    file.write_text("Hi")
    docModel = DocumentModel(str(file))
    c = docModel.getLinesCount()
    assert c == 1
    st = docModel.getLineN(0)
    print(st)
    assert st.c_str() == "Hi"
    for i in range(1,10):
        docModel.setLine(i, MyString(str(i)))
    for i in range(1,10):
        st = docModel.getLineN(i)
        assert st.c_str() == str(i)
        