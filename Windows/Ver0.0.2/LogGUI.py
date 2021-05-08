import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from qt_material import apply_stylesheet
import sqlite3


class LogClassGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


        self.setWindowTitle("DOCFREE(Ver 0.3) - LOG GUI")
    
    def initUI(self):
        self.move(500, 500)
        self.resize(500, 500)
        self.boxLogShow()


    def boxLogShow(self):

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
        self.setLayout(mainLayout) 
       
        self.Widget.show()

    def ReturnSqlData(self):

        # Database에서 로그 받아오기
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        LogData = cur.execute("select * from datelog")
        return LogData





if __name__ == "__main__":

    app = QApplication(sys.argv)
    themeName = "dark_lightgreen.xml"
    apply_stylesheet(app, theme=themeName)
    ex = LogGUI()
    sys.exit(app.exec_())
