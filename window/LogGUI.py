## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget

#insert하기 위한 값들 id = 증가값(sqllite에서 해결), 로그 =파일이름(파일이름 받아와야함), 유형:안전유무(db비교), 시간: 현재시간(sqllite에서 해결)

class logGC(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()
