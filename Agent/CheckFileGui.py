"""
작성팀: Server-Agent (한지웅, 박준석)
작성일자: 2021.04.02
업데이트 일자: 2021.04.22
이메일: jiungdev@gmail.com
개발환경: python 3.7.9 64bit
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

from DocuListener.DocuFilter import  docufree, alert
from DocuListener.CommApiServer import DocuInfoComm
import CheckLogUpdater

class AppD(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'DocuFree'
        self.listWidget = QListWidget()
        self.statusInfo = QLabel()
        self.phar = QProgressBar()
        self.timer = QBasicTimer()
        self.step = 0
        self.initUI()
        self.files = []    
     
    def initUI(self):

        '''
        내부 함수 영역
        '''

        def AddFunc():
            self.files.extend(self.openFileNamesDialog())
            
            if len(self.files) != 0:
                self.listWidget.clear()

                for index in range(len(self.files)):
                    print(self.files[index])
                    item = QListWidgetItem(self.files[index])
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.listWidget.addItem(item)
            
            
        def RemoveFunc():
        
            removeFiles = []

            for index in range(self.listWidget.count()):
                if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                    removeText = self.listWidget.item(index).text()
                    removeFiles.append(removeText)
                    
            for file in removeFiles:

                index = self.files.index(file)
                self.listWidget.takeItem(index)
                del self.files[index]
                
            print(self.files)

            
        # progressbar 값 변경시키는 것 
    
        def RunFunc():

            mal_count = 0
            prog_stat = 0
            files_count = len(self.files)
            
            if files_count == 0:
                return

            index = 0

            remove_indexs = []

            prog_incre = 100 // files_count

            # 결과값을 dict 형식으로 받음
            # {"파일명": result_object}
            docufree_result = docufree.main(self.files)

            for filename in docufree_result.keys():
                if docufree_result[filename].exit_code == 20:
                    # 데이터베이스에 추가하는 과정 거침
                    DocuInfoComm.add(filename)
                    
                    CheckLogUpdater.InsertLog(filename, docufree_result[filename].name)
                    remove_indexs.append(filename)
                    
                    prog_stat += prog_incre
                    self.phar.setValue(prog_stat)
                else:
                    prog_stat += prog_incre
                    self.phar.setValue(prog_stat)
                    CheckLogUpdater.InsertLog(filename, docufree_result[filename].name)
                    
                    
            mal_count = len(remove_indexs)

            for file in remove_indexs:
                if os.path.exists(file):
                    os.remove(file)
                index = self.files.index(file)
                self.listWidget.takeItem(index)

                del self.files[self.files.index(file)]
                

            self.phar.setValue(100)


            if mal_count == 0:
    
                self.statusInfo.setText("검사가 완료되었습니다. 의심스러운 문서가 없습니다.")
            else:
                self.statusInfo.setText(str(mal_count) + "건의 의심스러운 문서가 발견되었고 조치되었습니다.")
    

        ''' 
        내부 함수 영역 끝
        '''

        '''
        GUI 구성 시작
        '''


        self.setWindowTitle(self.title)
        self.setFixedSize(1000, 500)

        font = QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)

        # Create ProgressBar Layout

        ProgressLayout = QHBoxLayout()
        ProgressLayout.addWidget(self.phar)
        
        StatusLayout = QHBoxLayout()
        StatusLayout.addWidget(self.statusInfo)
        
        #Create add Button
        AddButton = QPushButton("파일추가")
        AddButton.setFont(font)
        
        AddButton.adjustSize()
        AddButton.clicked.connect(AddFunc)
        
        RemoveButton = QPushButton("선택삭제")
        
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
        mainLayout.addLayout(StatusLayout)
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
        fileFilter = "Office Files(*.xls *.xlsm *.doc *.docm *.ppt *.pptm)"
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"파일 검사", "",fileFilter, options=options)

        return files
        
