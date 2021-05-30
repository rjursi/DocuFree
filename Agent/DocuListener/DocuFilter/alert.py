# alert 창 띄워주는 클래스
# 객체 생성자로 파일명과 파일경로 보내주면 됨

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

import sys
import os


class alert():

    def __init__(self, full_filepath):
        super().__init__()
        self.mainPath = os.path.dirname(sys.executable)
    
        self.filename = full_filepath.split("\\")[-1]
        self.filename.replace("\"","")
        
        self.setupUi()

    def setupUi(self):
        self.MainWindow = QtWidgets.QMainWindow()

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(451, 218)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.MainWindow.setFont(font)
        self.MainWindow.setStyleSheet("background-color:rgb(56, 61, 67)")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 140, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(121, 174, 81)")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 100, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:rgb(255, 255, 255)")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 141, 131))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(self.mainPath, "images/alert.png")))    #이미지
        print(os.path.join(self.mainPath, "images/alert.png"))


        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.fillename = QtWidgets.QLabel(self.centralwidget)
        self.fillename.setGeometry(QtCore.QRect(180, 70, 231, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.fillename.setFont(font)
        self.fillename.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.fillename.setStyleSheet("color:rgb(255, 255, 255)")
        self.fillename.setAlignment(QtCore.Qt.AlignCenter)
        self.fillename.setObjectName("fillename")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 40, 261, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 255, 255)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.MainWindow.close)    # 클릭시 연결되는부분 click은 함수
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "확인"))         #클릭버튼
        self.label_2.setText(_translate("MainWindow", "해당파일이 삭제되었습니다"))
        self.fillename.setText(_translate("MainWindow", self.filename))    #파일이름변수로 교체해야됨
        self.label.setText(_translate("MainWindow", "해당 문서에서 악성 행위가 확인되었습니다"))

    



def alertf(full_filepath):


    ui = alert(full_filepath)
    
    return ui

