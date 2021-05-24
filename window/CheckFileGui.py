"""
작성팀: Server-Agent (한지웅, 박준석)
작성일자: 2021.04.02
업데이트 일자: 2021.04.22
이메일: jiungdev@gmail.com
개발환경: python 3.9.2 64bit
참고: https://developer.microsoft.com/ko-kr/windows/downloads/windows-10-sdk
"""

import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QCheckBox
from PyQt5.Qt import *
from PyQt5.QtCore import QBasicTimer
import PyQt5.QtCore
from qt_material import apply_stylesheet
from PyQt5.QtGui import *
from win32api import GetSystemMetrics

class AppD(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'DocuFree'
        self.listWidget = QListWidget()
        self.phar = QProgressBar()
        self.timer = QBasicTimer()
        self.step = 0
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        if GetSystemMetrics(0) >= 1600 and GetSystemMetrics(1) >= 900:
            self.setGeometry(700, 300, 400 ,300)
        elif GetSystemMetrics(0) < 1600 and GetSystemMetrics(1) < 900:
            self.setGeometry(400, 200, 350, 350)
        def AddFunc():
            files = self.openFileNamesDialog()
            if len(files) != 0:
                for i in range(len(files)):
                    print(files[i])
                    item = QListWidgetItem(files[i])
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.listWidget.addItem(item)

        def RemoveFunc():
            
            A = self.listWidget.count()
            count = 0

            for i in range(self.listWidget.count()):
                if self.listWidget.item(i).checkState() == QtCore.Qt.Checked:
                    count += 1

            while count:
                for i in range(self.listWidget.count()):
                    if self.listWidget.item(i).checkState() == QtCore.Qt.Checked:
                        self.listWidget.takeItem(i)
                        count -= 1
                        print(count)
                        break

        def RunFunc():
            for i in range(1, 101):
                self.phar.setValue(i)
                time.sleep(0.05)

            return None

        font = QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)

        # Create ProgressBar Layout
        self.phar.setGeometry(200, 100, 200, 30)
        ProgressLayout = QHBoxLayout()
        ProgressLayout.addWidget(self.phar)
        

        #Create add Button
        AddButton = QPushButton("파일추가")
        AddButton.setFont(font)
        #AddButton.setGeometry(200, 150, 50, 40)
        AddButton.adjustSize()
        AddButton.clicked.connect(AddFunc)
        
        RemoveButton = QPushButton("선택삭제")
        #RemoveButton.resize(50, 50)
        RemoveButton.setFont(font)
        RemoveButton.clicked.connect(RemoveFunc)

        RunButton = QPushButton()
        RunButton.setText("검사실행")
        RunButton.setFont(font)
        RunButton.clicked.connect(RunFunc)

        CancelButton = QPushButton("닫기")
        CancelButton.setFont(font)
        CancelButton.clicked.connect(self.close)
       
        buttonLayout1 = QVBoxLayout()
        #buttonLayout1.addStretch(2)
        buttonLayout1.addWidget(AddButton)
        buttonLayout1.addWidget(RemoveButton)
        buttonLayout1.addSpacing(400)

        buttonLayout2 = QHBoxLayout()
        buttonLayout2.addStretch(1)
        buttonLayout2.addWidget(RunButton)
        buttonLayout2.addWidget(CancelButton)
            
        # horizontal item, button v stack
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.listWidget)
        horizontalLayout.addLayout(buttonLayout1)
        
        # 메인 레이아웃에 설정한 레이아웃 설정
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addLayout(ProgressLayout)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonLayout2)
        self.show()

    
        

    def timerEvent(self, event):
        pass

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)

        return files
        

def Create():

    extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',
    # Font
    'font-family': 'Roboto',
    'font-size': '5px',
    }   

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_lightgreen.xml", extra=extra)

    ex = AppD()
    #sys.exit(app.exec_())
