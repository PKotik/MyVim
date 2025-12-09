import sys
sys.path.append('..')
from controller.MainController import MainController
from model.MainModel import MainModel
from model.MainModel import DocumentModel
from view.MainView import MainView

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else ""
    docModel = DocumentModel(filename)
    model = MainModel(docModel)
    view = MainView()
    controller = MainController(model, view)

    controller.run()
    
if __name__ == "__main__":
    main()