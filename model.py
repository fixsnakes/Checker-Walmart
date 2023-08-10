import sys

from main import MainWindow

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from finalui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from live import Ui_Dialog


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())