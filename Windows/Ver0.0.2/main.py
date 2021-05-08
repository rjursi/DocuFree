"""
작성팀: Server-Agent (한지웅, 박준석)
작성일자: 2021.04.02
업데이트 일자: 2021.04.22
이메일: jiungdev@gmail.com
개발환경: python 3.9.2 64bit
참고: https://developer.microsoft.com/ko-kr/windows/downloads/windows-10-sdk
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from CheckFilesFrame import DocFree, Create
from qt_material import apply_stylesheet
from CheckFileGui import Create, AppD
from PyQt5 import sip
from win10toast import ToastNotifier
from LogGUI import LogClassGUI
import sqlite3
import time


class AppMainFrame:
    
    def __init__(self):
        self.app = QApplication([])
        self.toaster = ToastNotifier()
        self.initUi()

    def initUi(self):
        
        self.SystemTray() 

    def push(self):
        self.action2.setChecked(False)

    # main page(DocuFree) layout set 
    def mainUi(self):
        self.mainWidget = QWidget()
        self.mainWidget.setWindowTitle('DocuFree Application')
        self.mainWidget.move(300, 300)
        self.mainWidget.resize(700, 300)
        #self.mainWidget        

        # 좌측: 버튼, 레이블 변수값 설정, CSS 설정
        headText = '문서작업을, 맘편하게'
        projectName = 'DocuFree'
        fileDetectText = 'Office 파일 검사'
        self.onStyleSheet = 'QPushButton{background-color: #a5d068; color: white; border: 0px solid;}'
        self.offStyleSheet = 'QPushButton{background-color: #ea5b60; color: white; border: 0px solid;}'
       
          
        headlineWidget = QLabel(headText)
        headlineWidget.setStyleSheet('font-weight: 500; font-size: 11px;')
        projectWidget = QLabel(projectName)
        projectWidget.setStyleSheet('font-weight: 900; font-size: 30px;')
        
        fileDetecButt = QPushButton(fileDetectText)
        fileDetecButt.setStyleSheet('''
        QPushButton{height: 170px; width:200px; background-color:#bef67a; color:#232629; padding-bottom: 0px; margin-bottom:100px; border: 0px solid;}
        QPushButton:hover { background-color: #d9f0be;}
        ''')
        fileDetecButt.clicked.connect(AppD)

        # 좌측: 레이아웃 생성, 설정
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(headlineWidget)
        leftLayout.addWidget(projectWidget)
        leftLayout.addWidget(fileDetecButt)
        leftLayout.setContentsMargins(10,10,0,50)
        leftLayout.setSpacing(0)

        

        # 우측 버튼, 레이블 생성, 이미지 경로 설정
        realOffText = '실시간 검사를 사용 중입니다'
        realOnText = '안전한 문서만 볼 수 있습니다'
        self.realOnNofiText = '실시간 검사를 사용 중입니다'
        self.realOnNofiSupoText ='안전한 문서만 볼 수 있습니다'
        self.realOffNofiText = '실시간 검사가 동작하지 않습니다'
        self.realOffNofiSupoText = '안전하지 않은 문서를 확인 할 수도 있습니다'
        self.onText = 'ON'
        self.offText = 'OFF'
        labelText = '          실시간 검사'

        imageOffUrl = 'images/shieldOff.png'
        imageOnUrl= 'iamges/shieldON.png'
        LabelWidget = QLabel(labelText)
        LabelWidget.setStyleSheet('font-weight:bold; background-color: #414344')

        self.onStyleSheet = 'QPushButton{background-color: #a5d068; color: white; border: 0px solid;}'
        self.offStyleSheet = 'QPushButton{background-color: #ea5b60; color: white; border: 0px solid;}'
    
        self.runButton = QPushButton(self.onText)
        self.runButton.setStyleSheet(self.onStyleSheet)
        self.runButton.clicked.connect(self.activeRun)

        self.realOnImage = QPixmap(imageOnUrl).scaledToWidth(100)
        self.realOffImage = QPixmap(imageOffUrl).scaledToWidth(100)
        self.label = QLabel()
        self.label.setPixmap(self.realOnImage)
        self.label.setContentsMargins(130,80,0,0)

        self.OnOffTextLabel = QLabel(self.realOnNofiText)
        self.OnOffTextLabel.setStyleSheet('margin-bottom: 20px; margin-left: 68px; padding-bottom:-40px; font-size: 17px; font-weight:1000')
        self.OnOffSupoTextLabel = QLabel(self.realOnNofiSupoText)
        self.OnOffSupoTextLabel.setStyleSheet('margin-bottom: 100px; margin-left: 100px;')
        
        #self.label.resize(50, 50)
        

        # 우측 레이아웃 생성, 설정

        onOffLayout = QHBoxLayout()
        onOffLayout.addWidget(LabelWidget)
        onOffLayout.addWidget(self.runButton)
        onOffLayout.setSpacing(0)
        onOffLayout.setContentsMargins(0,7,0,0)

        rightLayout = QVBoxLayout()
        rightLayout.addLayout(onOffLayout)
        rightLayout.addWidget(self.label)
        rightLayout.addWidget(self.OnOffTextLabel)
        rightLayout.addWidget(self.OnOffSupoTextLabel)
        rightLayout.setSpacing(0)
        
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        self.mainWidget.setLayout(mainLayout)
        self.mainWidget.show()

    

    """
    DocuFree의 메인 페이지를 눌렀을 때, 동작하는 함수

    색깔변경, toast 메세지, 실시간 감지 실행, system tray 동기화
    """

    def activeRun(self):
        if self.action2.isChecked():
            self.action2.setChecked(False)
            self.runButton.setText(self.offText)
            self.runButton.setStyleSheet(self.offStyleSheet)
            self.label.setPixmap(self.realOffImage)
            self.OnOffTextLabel.setText(self.realOffNofiText)
            self.OnOffSupoTextLabel.setText(self.realOffNofiSupoText)
            self.OnOffSupoTextLabel.setStyleSheet('margin-bottom: 100px; margin-left: 60px;')
            self.OnOffTextLabel.setStyleSheet('margin-bottom: 20px; margin-left: 45px; padding-bottom:-40px; font-size: 17px; font-weight:1000')


            time.sleep(0.4)
            self.activeFunc()
            
        else:
            self.action2.setChecked(True)
            self.runButton.setText(self.onText)
            self.runButton.setStyleSheet(self.onStyleSheet)
            self.label.setPixmap(self.realOnImage)
            self.OnOffTextLabel.setText(self.realOnNofiText)
            self.OnOffSupoTextLabel.setText(self.realOnNofiSupoText)
            self.OnOffTextLabel.setStyleSheet('margin-bottom: 20px; margin-left: 68px; padding-bottom:-40px; font-size: 17px; font-weight:1000')
            self.OnOffSupoTextLabel.setStyleSheet('margin-bottom: 100px; margin-left: 100px;')

            time.sleep(0.4)
            self.activeFunc()
            #self.runButton.clicked.connect(self.activeRun)


    def activeFunc(self):

        toastHeader = "DocuFree Notification"
        offMessage = "실시간 감지가 꺼졌습니다."
        onMessage = "실시간 감지가 실행되고 있습니다."


        if self.action2.isChecked():
            self.toaster.show_toast(toastHeader, onMessage, threaded=True, duration=1.5)
        else:
            self.toaster.show_toast(toastHeader, offMessage, threaded=True, duration=1.5)

   


    def logGui(self):

        self.logGUI = QWidget()
    

        self.logGUI.setWindowTitle("DOCFREE(Ver 0.3) - LOG GUI")
        self.logGUI.move(500, 500)
        self.logGUI.resize(700, 500)
        

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
        

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(storeButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(tableWidget)
        mainLayout.addLayout(buttonLayout)
        self.logGUI.setLayout(mainLayout) 
        self.logGUI.show() 

    def ReturnSqlData(self):

        # Database에서 로그 받아오기
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        LogData = cur.execute("select * from datelog")
        return LogData


    """
    System Tray의 버튼을 생성하고 부착하는 함수.
    """
    def SystemTray(self):

        
        #??
        self.app.setQuitOnLastWindowClosed(False)


        # 아이콘 생성
        iconPath = "images/icon.png"
        icon = QIcon(iconPath)


        # 트레이 아이콘 생성
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        
    
        # System Tray Creat menu 
        menu = QMenu()
        

        # 파일 검사 실행매뉴 생성
        fileAnalysisName = "파일 검사"
        action1 = QAction(fileAnalysisName)
        A = action1.triggered.connect(AppD)

        # 실시간 검사 매뉴 체크 생성
        fileRealTimeName = "실시간검사"
        self.action2 = QAction(fileRealTimeName, checkable=True)
        self.action2.setChecked(True)
        self.action2.triggered.connect(self.activeFunc)
        

        # 메인 생성
        projectName = "DocuFree"
        action3 = QAction(projectName)
        action3.triggered.connect(self.MainUI)

        
        DectectLogMenu = "로그 보기"
        action4 = QAction(DectectLogMenu)
        self.action4.triggered.connect(LogGUI)


        # 메뉴 부착
        menu.addAction(action3)
        menu.addAction(action1)
        menu.addAction(self.action2)

        # Add a Quit option to the menu
        quitName = "종료"
        quit = QAction(quitName)
        quit.triggered.connect(self.app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)


        """
        apply style sheet and run app
        """
        themeName = "dark_lightgreen.xml"
        apply_stylesheet(self.app, theme=themeName)
        self.app.exec_()



main = AppMainFrame()
