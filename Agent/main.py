"""
작성팀: Server-Agent (한지웅, 박준석)
작성일자: 2021.04.02
업데이트 일자: 2021.04.22
이메일: jiungdev@gmail.com
개발환경: python 3.9.2 64bit
참고: https://developer.microsoft.com/ko-kr/windows/downloads/windows-10-sdk
"""

# 해야될거
# save함수 만들어야함(sqllite내용 파일로 저장),db에 있으면 바로 입력하고 없으면 검사 하고 입력, alert.py연결, send.py 연결
# insert용코드만들기
# con = sqlite3.connect('test.db')
#         cur = con.cursor()
#         LogData = cur.execute("insert into ~")


import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from CheckFilesFrame import DocFree, Create

from qt_material import apply_stylesheet
from PyQt5 import sip
from win10toast import ToastNotifier


from CheckFileGui import AppD
from PyQt5.QtCore import Qt
from subprocess import Popen
#from LogGUI import LogClassGUI
import sqlite3
import time
import sys
import os
from win32api import GetSystemMetrics
import Listener


class AppMainFrame:
    
    def __init__(self):
        self.mainPath = os.path.dirname(sys.executable)
        
        self.app = QApplication([])
        self.toaster = ToastNotifier()
        self.initUi()

    def initUi(self):
        
        # self.mainUi()
        # run()
        self.SystemTray()


    def push(self):
        self.action2.setChecked(False)

    # main page(DocuFree) layout set 
    def mainUi(self):
        self.mainWidget = QWidget()

        # 실시간 검사 스레드 생성 및 켜지자마자 바로 실행
        self.listenerThread = Listener.DocuListener()
        self.ListenerThreadStart()
    
        self.mainWidget.setWindowTitle('DocuFree Application')


        # print(self.mainWidget.frameGeometry().height())
    
        # self.mainWidget.setFixedSize(640,400)


        # 640*480
        # if GetSystemMetrics(0) >= 1600 and GetSystemMetrics(1) >= 900:
        #     self.mainWidget.move(300, 300)
        #     self.mainWidget.resize(700, 300)
        # elif GetSystemMetrics(0) < 1600 and GetSystemMetrics(1) < 900:
        #     self.mainWidget.move(200, 200)
        #     self.mainWidget.resize(500, 200) 


        # 좌측: 버튼, 레이블 변수값 설정, CSS 설정
        headText = '문서작업을, 맘편하게'
        projectName = 'DocuFree'
      
        headlineWidget = QLabel(headText) # string: 문서 작업을 맘편하게
        headlineWidget.setStyleSheet('font-weight: 200; font-size: 11px; padding: 0px; margin: 0px;') 
        
        headline_HBoxLayout = QHBoxLayout()
        headline_HBoxLayout.addWidget(headlineWidget)
        headline_HBoxLayout.setContentsMargins(0,0,0,10)
        headline_HBoxLayout.setSpacing(0)

        projectnameWidget = QLabel(projectName) # string: DocuFree
        projectnameWidget.setStyleSheet('font-weight: 900; font-size: 30px; padding: 0px; margin: 0px;')
        
        projectname_HBoxLayout = QHBoxLayout()
        projectname_HBoxLayout.addWidget(projectnameWidget)
        projectname_HBoxLayout.setContentsMargins(0,0,0,0)
        projectname_HBoxLayout.setSpacing(0)


        fileDetectText = 'Office\n파일 검사'

        # 파일 검사 스타일시트 목록
        self.onStyleSheet = 'QPushButton{background-color: #a5d068; color: white; padding: 0px; margin: 0px; border: 0px solid;}'
        self.offStyleSheet = 'QPushButton{background-color: #ea5b60; color: white; padding: 0px; margin: 0px; border: 0px solid;}'


        filescanButton = QPushButton(fileDetectText) # string: Office 파일 검사 
        filescanButton.setStyleSheet('''
        QPushButton{height: 170px; width:200px; background-color:#bef67a; color:#232629; font-size:20px; font-weight:bold; padding: 0px; margin-bottom: 100px; border: 0px solid;}
        QPushButton:hover { background-color: #d9f0be;}
        ''')


        # 파일 검사 버튼 이벤트 핸들러 연결
        filescanButton.clicked.connect(AppD)


        filescan_HBoxLayout = QHBoxLayout()
        filescan_HBoxLayout.addWidget(filescanButton)
        filescan_HBoxLayout.setContentsMargins(0,0,0,0)
        filescan_HBoxLayout.setSpacing(0)
        
        # 좌측: 레이아웃 생성, 설정
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(headline_HBoxLayout)
        leftLayout.addLayout(projectname_HBoxLayout)
        leftLayout.addLayout(filescan_HBoxLayout)
        
        leftLayout.setContentsMargins(0,0,50,0)
        leftLayout.setSpacing(0)

        # 우측 버튼, 레이블 생성, 이미지 경로 설정
        realOffText = '실시간 검사를 사용 중입니다'
        realOnText = '안전한 문서만 볼 수 있습니다'
        labelText = '실시간 검사'

        self.realOnNofiText = '실시간 검사를 사용 중입니다'
        self.realOnNofiSupoText ='안전한 문서만 볼 수 있습니다'
        self.realOffNofiText = '실시간 검사가 중지되었습니다'
        self.realOffNofiSupoText = '안전하지 않은 문서를 확인 할 수도 있습니다'
        self.onText = 'ON'
        self.offText = 'OFF'
        
        imageOffUrl = os.path.join(self.mainPath,'images/shieldOff.png')
        imageOnUrl= os.path.join(self.mainPath, 'images/shieldOn.png')

        LabelWidget = QLabel(labelText)
        LabelWidget.setStyleSheet('font-weight:bold; background-color: #414344; padding-left: 20px; padding-right: 20px; margin: 0px;')

        self.onStyleSheet = 'QPushButton{background-color: #a5d068; width:130px; color: white; padding: 0px; margin: 0px; border: 0px solid;}'
        self.offStyleSheet = 'QPushButton{background-color: #ea5b60; width:130px; color: white; padding: 0px; margin: 0px; border: 0px solid;}'
    
        self.runButton = QPushButton(self.onText)
        self.runButton.setStyleSheet(self.onStyleSheet)
        self.runButton.clicked.connect(self.activeRun)

        self.realOnImage = QPixmap(imageOnUrl).scaledToWidth(100)
        self.realOffImage = QPixmap(imageOffUrl).scaledToWidth(100)

        self.label = QLabel()
        self.label.setPixmap(self.realOnImage)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('margin-top : 70px')

        
        self.OnOffTextLabel = QLabel(self.realOnNofiText)
        self.OnOffTextLabel.setAlignment(Qt.AlignCenter)
        self.OnOffTextLabel.setStyleSheet('padding: 0px; margin: 0px; font-size: 17px; font-weight:1000')
        self.OnOffSupoTextLabel = QLabel(self.realOnNofiSupoText)
        self.OnOffSupoTextLabel.setAlignment(Qt.AlignCenter)
        self.OnOffSupoTextLabel.setStyleSheet('padding: 0px; margin-bottom: 50px;')
        
        

        # 사진 크기 조정
        self.label.resize(50, 50)
        

        # 우측 레이아웃 생성, 설정

        onOffLayout = QHBoxLayout()
        onOffLayout.addWidget(LabelWidget)
        onOffLayout.addWidget(self.runButton)
        onOffLayout.setSpacing(0)
        onOffLayout.setContentsMargins(0,0,0,0)

        rightLayout = QVBoxLayout()
        rightLayout.addLayout(onOffLayout)
        rightLayout.addWidget(self.label)
        rightLayout.addWidget(self.OnOffTextLabel)
        rightLayout.addWidget(self.OnOffSupoTextLabel)
        
        rightLayout.setAlignment(Qt.AlignHCenter)
        # rightLayout.setSpacing(0)
        
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setContentsMargins(30,20,30,20)

        
       
        self.mainWidget.setLayout(mainLayout)
        self.mainWidget.show()

    

    """
    DocuFree의 메인 페이지를 눌렀을 때, 동작하는 함수

    색깔변경, toast 메세지, 실시간 감지 실행, system tray 동기화
    """

    def ListenerThreadStart(self):
        if not self.listenerThread.isRun:
            self.listenerThread.isRun = True
            self.listenerThread.start()
        
    def ListenerThreadStop(self):
        if self.listenerThread.isRun:

            self.listenerThread.isRun = False
            self.listenerThread.ExitMessageToNamedPipe()
                        
    def activeRun(self):
        if self.action2.isChecked():
            self.action2.setChecked(False)
            self.runButton.setText(self.offText)
            self.runButton.setStyleSheet(self.offStyleSheet)
            self.label.setPixmap(self.realOffImage)
            self.OnOffTextLabel.setText(self.realOffNofiText)
            self.OnOffSupoTextLabel.setText(self.realOffNofiSupoText)
            self.ListenerThreadStop()
            # self.OnOffSupoTextLabel.setStyleSheet('margin-bottom: 100px; margin-left: 60px;')
            # self.OnOffTextLabel.setStyleSheet('margin-bottom: 20px; margin-left: 45px; padding-bottom:-40px; font-size: 17px; font-weight:1000')


            time.sleep(0.4)
            self.activeFunc()
            
        else:
            self.action2.setChecked(True)
            self.runButton.setText(self.onText)
            self.runButton.setStyleSheet(self.onStyleSheet)
            self.label.setPixmap(self.realOnImage)
            self.OnOffTextLabel.setText(self.realOnNofiText)
            self.OnOffSupoTextLabel.setText(self.realOnNofiSupoText)
            self.ListenerThreadStart()


            # self.OnOffTextLabel.setStyleSheet('margin-bottom: 20px; margin-left: 68px; padding-bottom:-40px; font-size: 17px; font-weight:1000')
            # self.OnOffSupoTextLabel.setStyleSheet('margin-bottom: 100px; margin-left: 100px;')

            time.sleep(0.4)
            self.activeFunc()
            #self.runButton.clicked.connect(self.activeRun)


    def activeFunc(self):

        toastHeader = "DocuFree Notification"
        offMessage = "실시간 감지가 꺼졌습니다."
        onMessage = "실시간 감지가 실행되고 있습니다."
        
        # pyinstaller 로 빌드하면서 icon_path 관련 이슈 발생, 차후 수정


        if self.action2.isChecked():
            self.toaster.show_toast(toastHeader, onMessage, icon_path = '', threaded=True, duration=1.5)
            
        else:
            self.toaster.show_toast(toastHeader, offMessage, icon_path = '', threaded=True, duration=1.5)



    def logGui(self):

        self.logGUI = QWidget()
    
        # 동적 UI 설정 부분

        
        self.logGUI.setWindowTitle("DOCFREE(Ver 0.3) - LOG GUI")
        # if GetSystemMetrics(0) >= 1600 and GetSystemMetrics(1) >= 900:
        #     self.logGUI.move(600, 300)
        #     self.logGUI.resize(500, 400)
        # elif GetSystemMetrics(0) < 1600 and GetSystemMetrics(1) < 900:
        #     self.logGUI.move(300, 100)
        #     self.logGUI.resize(500, 400)

        # 테이블 위잿 설정        
        tableWidget = QTableWidget()
        tableWidget.setRowCount(12)
        tableWidget.setColumnCount(4)
        tableWidget.setHorizontalHeaderLabels(["id", "로그", "유형", "시간"])
        LogData = self.ReturnSqlData()

        for idx, val in enumerate(LogData):
            tableWidget.setItem(idx, 0, QTableWidgetItem(str(val[0])))
            tableWidget.setItem(idx, 1, QTableWidgetItem(str(val[1])))
            tableWidget.setItem(idx, 2, QTableWidgetItem(str(val[2])))
            tableWidget.setItem(idx, 3, QTableWidgetItem(str(val[3])))

        #버튼 설정
        storeButton = QPushButton("저장")
        cancelButton = QPushButton("취소")
        storeButton.setStyleSheet('QPushButton{ width:40; height:10;}')
        cancelButton.setStyleSheet('QPushButton{ width:40; height: 10;}')
        storeButton.clicked.connect(self.save)
        cancelButton.clicked.connect(self.logGUI.close)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(storeButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)

    
        self.logGUI.setLayout(mainLayout) 
        self.logGUI.show()

    def ReturnSqlData(self):

        # Database에서 로그 받아오기
        con = sqlite3.connect(os.path.join(self.mainPath, 'test.db'))
        cur = con.cursor()
        LogData = cur.execute("select * from datelog")
        return LogData


    """
    System Tray의 버튼을 생성하고 부착하는 함수.
    """
    def SystemTray(self):

        
        
        self.app.setQuitOnLastWindowClosed(False)


        # 아이콘 생성
        iconPath = "images/icon.png"
        icon = QIcon(os.path.join(self.mainPath, iconPath))


        # 트레이 아이콘 생성
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        
    
        # System Tray Creat menu 
        menu = QMenu()
        

        # 파일 검사 실행매뉴 생성
        fileAnalysisName = "파일 검사"
        action1 = QAction(fileAnalysisName)
        action1.triggered.connect(AppD)

        # 실시간 검사 매뉴 체크 생성
        fileRealTimeName = "실시간검사"
        self.action2 = QAction(fileRealTimeName, checkable=True)
        self.action2.setChecked(True)
        self.action2.triggered.connect(self.activeFunc)
        

        # 메인 생성
        projectName = "DocuFree"
        action3 = QAction(projectName)
        action3.triggered.connect(self.mainUi)

        
        DectectLogMenu = "로그 보기"
        self.action4 = QAction(DectectLogMenu)
        self.action4.triggered.connect(self.logGui)


        # 메뉴 부착
        menu.addAction(action3)
        menu.addAction(action1)
        menu.addAction(self.action2)
        menu.addAction(self.action4)

        # Add a Quit option to the menu
        quitName = "종료"
        quit = QAction(quitName)
        quit.triggered.connect(self.app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)
        tray.show()
        


        """
        apply style sheet and run app
        """

        themeName = "dark_lightgreen.xml"
        apply_stylesheet(self.app, theme=themeName)


        self.app.exec_()
     
        

    def save(self):
        con = sqlite3.connect(os.path.join(self.mainPath, 'test.db'))
        cur = con.cursor()
        cur.execute("select * from datelog")
        txt = cur.fetchall()
        Filesave = QFileDialog.getSaveFileName(self.logGUI,'Save file', "", "txt files (*.txt)")
        if Filesave[0] != "":
            with open(Filesave[0], 'w') as f:
                for i in txt:
                    f.write(str(i))
                    f.write("\n")



main = AppMainFrame()
