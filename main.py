from PyQt5.QtWidgets import QApplication, QMainWindow


import sys
import logging

import gui

import PySide6.QtCore
from PySide6.QtWidgets import QApplication


logging.basicConfig()
# logging.root.setLevel(logging.INFO)
logging.root.setLevel(logging.DEBUG)

logging.info("Traffic simulator")
logging.info("Version: 0.0.1")

logging.info("Pyside version: " + PySide6.__version__)
logging.info("QtCore version: " + PySide6.QtCore.__version__)

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()