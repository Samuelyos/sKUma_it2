import sys
from PyQt6 import QtWidgets
from AdminRequestGUI import AdminRequestGUI

def admin_main():
    app = QtWidgets.QApplication(sys.argv)
    admin_window = AdminRequestGUI()
    app.exec()

if __name__ == '__main__':
    admin_main()