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
from DocuListener.CommApiServer import DocuInfoAdd, DocuInfoSelect
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
            
                self.listWidget.update()

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


                self.listWidget.update()




        # progressbar 값 변경시키는 것 
    
        def RunFunc():

            mal_count = 0
            prog_stat = 0
            files_count = len(self.files)
            
            index = 0

            while index < files_count:
                
                prog_stat = (float(files_count) / 100.0) * 100.0

                self.phar.setValue(index) 
                
                # 여기서 특정 파일에 대하여 파일을 잘 못닫고 있음
                docufree_result = docufree.main(self.files[index])

                if docufree_result.exit_code == 20:
                    
                    mal_count += 1

                    searchResult = DocuInfoSelect.SetSearchFile(self.files[index])
                
                    print(searchResult)

                    if not searchResult: # DB 에 해당 값이 들어가 있지 않을 경우
                        DocuInfoAdd.add(self.files[index])
                                    
                    self.listWidget.takeItem(index)
                    self.listWidget.update()

                   
                    os.remove(self.files[index])
                           
                    files_count -= 1
                
                    CheckLogUpdater.InsertLog(self.files[index], docufree_result.name)
                    del self.files[index]
                else:
                    # 지정 인덱스 파일이 악성 파일이 아니면 바로 다음 인덱스로 넘김
                    CheckLogUpdater.InsertLog(self.files[index], docufree_result.name)
                   
                    index += 1

                time.sleep(0.05)
                self.phar.setValue(prog_stat)

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
        
        StatusLayout = QHBoxLayout()
        StatusLayout.addWidget(self.statusInfo)
        
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
        
