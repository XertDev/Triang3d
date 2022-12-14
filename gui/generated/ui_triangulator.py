# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'triangulator.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGraphicsView, QGridLayout,
    QHBoxLayout, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSlider,
    QStatusBar, QTreeView, QVBoxLayout, QWidget)

from gui.skeleton_view import SkeletonView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1066, 600)
        self.actionOpen_samples = QAction(MainWindow)
        self.actionOpen_samples.setObjectName(u"actionOpen_samples")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.samples_tree = QTreeView(self.centralwidget)
        self.samples_tree.setObjectName(u"samples_tree")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samples_tree.sizePolicy().hasHeightForWidth())
        self.samples_tree.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.samples_tree)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.camera_tl = QGraphicsView(self.centralwidget)
        self.camera_tl.setObjectName(u"camera_tl")

        self.gridLayout_2.addWidget(self.camera_tl, 0, 0, 1, 1)

        self.camera_tr = QGraphicsView(self.centralwidget)
        self.camera_tr.setObjectName(u"camera_tr")

        self.gridLayout_2.addWidget(self.camera_tr, 0, 2, 1, 1)

        self.camera_bl = QGraphicsView(self.centralwidget)
        self.camera_bl.setObjectName(u"camera_bl")

        self.gridLayout_2.addWidget(self.camera_bl, 1, 0, 1, 1)

        self.camera_br = QGraphicsView(self.centralwidget)
        self.camera_br.setObjectName(u"camera_br")

        self.gridLayout_2.addWidget(self.camera_br, 1, 2, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timeline = QSlider(self.centralwidget)
        self.timeline.setObjectName(u"timeline")
        self.timeline.setEnabled(False)
        self.timeline.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.timeline)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.prev_frame = QPushButton(self.centralwidget)
        self.prev_frame.setObjectName(u"prev_frame")
        self.prev_frame.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.prev_frame)

        self.play_pause = QPushButton(self.centralwidget)
        self.play_pause.setObjectName(u"play_pause")
        self.play_pause.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.play_pause)

        self.next_frame = QPushButton(self.centralwidget)
        self.next_frame.setObjectName(u"next_frame")
        self.next_frame.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.next_frame)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.verticalLayout)


        self.gridLayout_2.addLayout(self.formLayout, 1, 4, 1, 1)

        self.skeletal = SkeletonView(self.centralwidget)
        self.skeletal.setObjectName(u"skeletal")

        self.gridLayout_2.addWidget(self.skeletal, 0, 4, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1066, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen_samples)
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.actionOpen_samples.triggered.connect(MainWindow.openDirectory)
        self.actionExit.triggered.connect(MainWindow.exitApp)
        self.samples_tree.doubleClicked.connect(MainWindow.openSequence)
        self.prev_frame.clicked.connect(MainWindow.prevFrame)
        self.next_frame.clicked.connect(MainWindow.nextFrame)
        self.timeline.valueChanged.connect(MainWindow.setFrame)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_samples.setText(QCoreApplication.translate("MainWindow", u"Load samples", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.prev_frame.setText(QCoreApplication.translate("MainWindow", u"\u23f4\u23f4", None))
        self.play_pause.setText("")
        self.next_frame.setText(QCoreApplication.translate("MainWindow", u"\u23f5\u23f5", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

