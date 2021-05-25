import sys
from PyQt5 import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.Qt import *
from main import *


class DocuFreeWidget(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()
        

    def initUI(self):

        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()
        

        # 상단 버튼, 레이블 생성, 설정
        onText = 'ON'
        offText = 'OFF'
        labelText = '실시간 검사'
        headText = '문서작업을, 맘편하게'
        projectName = 'DocuFree'

        runButton = QPushButton(onText)
        LabelWidget = QLabel(labelText)
        headlineWidget = QLabel(headText)
        projectWidget = QLabel(projectName)

        runButton.clicked.connect(AppMainFrame().push)

        # 상단 레이아웃 생성, 설정
        headlineLayout = QVBoxLayout()
        headlineLayout.addWidget(headlineWidget)
        headlineLayout.addWidget(projectWidget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(runButton)
        buttonLayout.addWidget(LabelWidget)

        highLayout = QHBoxLayout()
        highLayout.addLayout(headlineLayout)
        highLayout.addLayout(buttonLayout)

        # 밑단 버튼, 레이블 생성, 설정
        realOffText = '실시간 검사를 사용 중입니다'
        realOnText = '안전한 문서만 볼 수 있습니다'
        fileDetectText = 'Office 파일 검사'
        fileDetecBut = QPushButton(fileDetectText)
        imageLabel = QPixmap('')
        

        # 밑단 레이아웃 생성, 설정


        buttonLayout2 = QVBoxLayout()
        imageLayout = QVBoxLayout()
        lowlineLayout = QHBoxLayout()

        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(highLayout)
        self.setLayout(mainLayout)
        self.show()

    def active(self):

        print()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DocuFreeWidget()
    sys.exit(app.exec_())
