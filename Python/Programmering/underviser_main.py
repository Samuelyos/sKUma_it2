import sys
from PyQt6 import QtWidgets
from TeacherRequestGUI import TeacherRequestGUI

def teacher_main():
    app = QtWidgets.QApplication(sys.argv)
    TR_window = TeacherRequestGUI()
    app.exec()

if __name__ == '__main__':
    teacher_main()