import sys
from ui3 import UI
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = UI()

    sys.exit(app.exec_())