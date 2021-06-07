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
    
        self.filename = full_filepath.split('/')[-1]
        self.filename.replace("\"","")
        
        self.setupUi()

    def setupUi(self):

        # 메인 윈도우
        self.MainWindow = QWidget()
       
        self.MainWindow.setFixedSize(700, 300)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        self.MainWindow.setFont(font)
        self.MainWindow.setStyleSheet("background-color:rgb(56, 61, 67)")

        # 확인 버튼
        self.pushButton = QtWidgets.QPushButton("확인")
        self.pushButton.setStyleSheet('QPushButton{width:250px; height:50px}')
      
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(121, 174, 81); color:rgb(255, 255, 255)")
    
        # 삭제 되었습니다 안내 텍스트
        self.label_deleteInfo = QtWidgets.QLabel()
        self.label_deleteInfo.setText("해당파일이 삭제되었습니다")
    
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.label_deleteInfo.setFont(font)
        self.label_deleteInfo.setStyleSheet("color:rgb(255, 255, 255)")
        self.label_deleteInfo.setAlignment(QtCore.Qt.AlignCenter)
    

        self.alertImage = QtWidgets.QLabel()
       
        # 이미지

        self.alertImage.setText("")
        self.alertImage.setPixmap(QtGui.QPixmap(os.path.join(self.mainPath, "images/alert.png")))    #이미지
        self.alertImage.resize(50, 25)
        self.alertImage.setScaledContents(True)
      

        self.filenameInfo = QtWidgets.QLabel(self.filename)
    
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.filenameInfo.setFont(font)
        self.filenameInfo.setStyleSheet("color:rgb(255, 255, 255);")
        self.filenameInfo.setAlignment(QtCore.Qt.AlignCenter)
        
        # 악성 행위 확인 라벨
        self.malInfo = QtWidgets.QLabel("해당 문서에서 악성 행위가 확인되었습니다")
    
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        self.malInfo.setFont(font)
        self.malInfo.setStyleSheet("color:rgb(255, 255, 255);")
        self.malInfo.setAlignment(QtCore.Qt.AlignCenter)
    
        self.pushButton.clicked.connect(self.MainWindow.close)    # 클릭시 연결되는부분 click은 함수
      
        mainLayout = QHBoxLayout()
        image_vBoxLayout = QVBoxLayout()
        image_vBoxLayout.addWidget(self.alertImage)

        info_button_vBoxLayout = QVBoxLayout()
        
        info_button_vBoxLayout.addWidget(self.label_deleteInfo)
        info_button_vBoxLayout.addWidget(self.filenameInfo)
        info_button_vBoxLayout.addWidget(self.malInfo)
        info_button_vBoxLayout.addWidget(self.pushButton)


        mainLayout.addLayout(image_vBoxLayout)
        mainLayout.addLayout(info_button_vBoxLayout)
        
        self.MainWindow.setLayout(mainLayout)

    
def alertf(full_filepath):

    ui = alert(full_filepath)
    
    return ui

