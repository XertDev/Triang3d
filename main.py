import matplotlib
from PyQt5.QtWidgets import QApplication, QMainWindow


import sys
import logging

from PySide6 import QtCore

import gui

import PySide6.QtCore
from PySide6.QtWidgets import QApplication


logging.basicConfig()
# logging.root.setLevel(logging.INFO)
logging.root.setLevel(logging.DEBUG)
matplotlib.use('Qt5Agg')

logging.info("Traffic simulator")
logging.info("Version: 0.0.1")

logging.info("Pyside version: " + PySide6.__version__)
logging.info("QtCore version: " + PySide6.QtCore.__version__)

app = QApplication(sys.argv)

window = gui.MainWindow()
window.setWindowState(QtCore.Qt.WindowMaximized)
window.show()

app.exec()