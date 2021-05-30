"""
작성팀: Server-Agent (한지웅, 박준석)
작성일자: 2021.04.02
업데이트 일자: 2021.04.22
이메일: jiungdev@gmail.com
개발환경: python 3.9.2 64bit
참고: https://developer.microsoft.com/ko-kr/windows/downloads/windows-10-sdk
"""

import sys, os
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from PyQt5.QtCore import QBasicTimer
from qt_material import apply_stylesheet
from PyQt5.QtGui import *
from win32api import GetSystemMetrics

from DocuListener.DocuFilter import docufree, alert
from DocuListener.CommApiServer import DocuInfoAdd
import CheckLogUpdater


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


        '''
        내부 함수 영역
        '''

        def AddFunc():
            self.files = self.openFileNamesDialog()
            if len(self.files) != 0:
                for index in range(len(self.files)):
                    print(self.files[index])
                    item = QListWidgetItem(self.files[index])
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.listWidget.addItem(item)

        def RemoveFunc():
        
            count = 0

            for index in range(self.listWidget.count()):
                if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                    count += 1

            while count:
                for index in range(self.listWidget.count()):
                    if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                        self.listWidget.takeItem(index)
                        del self.files[index]
                        count -= 1
                        
                        break

        # progressbar 값 변경시키는 것 
        
        def RunFunc():

            prog_stat = 0
            files_count = len(self.files)
            for index in range(files_count):
                
                prog_stat += 100 // files_count

                self.phar.setValue(index) 

                docufree_result = docufree.main(self.files[index])
                

                # 임시 악성파일 식별 시나리오를 위해 조작
                docufree_result.exit_code = 20
                
                if docufree_result.exit_code == 20:
                    self.AlertObj = alert.alertf(self.files[index])
                    self.AlertObj.MainWindow.show()

                    info_result = DocuInfoAdd.add(self.files[index])
                    
                    if info_result:
                        
                        # os.remove(self.files[index]) # 파일 지우는 명령어
                        pass

                    
                    else:
                        print("Info INsert Error!!")

                CheckLogUpdater.InsertLog(self.files[index], docufree_result.name)

                time.sleep(0.05)

            self.phar.setValue(100)



        ''' 
        내부 함수 영역 끝
        '''

        '''
        GUI 구성 시작
        '''


        self.setWindowTitle(self.title)
        if GetSystemMetrics(0) >= 1600 and GetSystemMetrics(1) >= 900:
            self.setGeometry(700, 300, 400 ,300)
        elif GetSystemMetrics(0) < 1600 and GetSystemMetrics(1) < 900:
            self.setGeometry(400, 200, 350, 350)


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

        '''
        GUI 구성 끝 

        '''

       

    # 파일 검사에 따른 timerEvent, Progressbar 제어
    def timerEvent(self, event):
        pass


    # openFilesDialog 통한 파일 이름 반환
    # 파일명을 리스트 형식으로 반환

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)

        return files
        

'''
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
    app.exec_()
'''

