import platform
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QIntValidator, QFont, QBrush
from PyQt5.QtCore import Qt, QUrl
from draw_top_k import drawTopkMap, drawRangeMap
from find import findTopK,findTopKWithKeyWord,findRange
from table import MyTable

from math import *
import plotly.plotly as py
from plotly.graph_objs import *
import datetime
from DrawThread import DrawThread


class UI(QMainWindow):
    """docstring for UI"""

    def __init__(self):
        super(UI, self).__init__()
        self.initUI()

    def initUI(self):
        # 将任务栏图标改成 image/StarBucks.png
        if platform.system() == 'Windows':
            # 程序设置和图标一致
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "back1.jpg")

        self.setWindowTitle('Starbucks数据分析')
        self.setWindowIcon(QIcon('back1.jpg'))



        self.mainWidget = QWidget()  # 主窗体控件
        self.mainLayout = QGridLayout()  # 主窗体layout

        self.menuBar()
        self.statusBar()  # 状态栏
        self.setMenu()

        self.setFindTopKWidget()
        self.setWebEngineView()

        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.webEngine, 3, 1, 6, 6)

        self.adjustSize()
        self.center()  # 将窗口居中
        self.show()
        self.file = pd.read_csv('directory00.csv')

    def setWebEngineView(self):
        self.webEngine = QWebEngineView(self)

        # 设置菜单上的按钮

    def setMenu(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)

        buttonMenu = menuBar.addMenu('国家')

        action1 = QAction('星巴克世界分布图', self)
        buttonMenu.addAction(action1)
        action1.triggered.connect(self.drawMap)
        action2 = QAction('国家数量渐变图', self)
        buttonMenu.addAction(action2)
        action2.triggered.connect(self.drawColorMaps)
        action11 = QAction('国家店铺数量柱状图', self)
        buttonMenu.addAction(action11)
        action11.triggered.connect(self.drawCountryBar)
        action12 = QAction('国家店铺数量饼状图', self)
        buttonMenu.addAction(action12)
        action12.triggered.connect(self.drawCountryPie)

        buttonMenu = menuBar.addMenu('时区')

        action3 = QAction('时区散点图', self)
        buttonMenu.addAction(action3)
        action3.triggered.connect(self.drawLongitudeMap)
        action4 = QAction('时区数量渐变图', self)
        buttonMenu.addAction(action4)
        action4.triggered.connect(self.drawTimezonecolor)
        action5 = QAction('时区店铺数量柱状图', self)
        buttonMenu.addAction(action5)
        action5.triggered.connect(self.drawTimezoneBar)
        action6 = QAction('时区店铺数量饼状图', self)
        buttonMenu.addAction(action6)
        action6.triggered.connect(self.drawTimezonePie)

        buttonMenu = menuBar.addMenu('查找top-k')

        action7 = QAction('top-k图', self)
        buttonMenu.addAction(action7)
        action7.triggered.connect(self.findTopkTu)
        action9 = QAction('top-k查找表格', self)
        buttonMenu.addAction(action9)
        action9.triggered.connect(self.setExcelTopk)

        buttonMenu = menuBar.addMenu('查找range')

        action8 = QAction('range图', self)
        buttonMenu.addAction(action8)
        action8.triggered.connect(self.findRangeTu)
        action10 = QAction('range查找表格', self)
        buttonMenu.addAction(action10)
        action10.triggered.connect(self.setExcelRange)

    def setFindTopKWidget(self):
        longitudeLabel = QLabel()
        latitudeLabel = QLabel()
        kLabel = QLabel()
        rangeLabel = QLabel()
        keywordLabel = QLabel()

        longitudeLabel.setText("经度: ")
        latitudeLabel.setText("纬度: ")
        kLabel.setText("k: ")
        rangeLabel.setText("r:")
        keywordLabel.setText("关键字：")

        self.longitudeEdit = QLineEdit()
        self.latitudeEdit = QLineEdit()
        self.kEdit = QLineEdit()
        self.rangeEdit = QLineEdit()
        self.keywordEdit = QLineEdit()

        hBox = QHBoxLayout(self)
        hBox.addWidget(longitudeLabel)
        hBox.addWidget(self.longitudeEdit, 0)
        hBox.addWidget(latitudeLabel)
        hBox.addWidget(self.latitudeEdit, 0)
        hBox.addWidget(kLabel)
        hBox.addWidget(self.kEdit, 0)
        hBox.addWidget(rangeLabel)
        hBox.addWidget(self.rangeEdit, 0)
        hBox.addWidget(keywordLabel)
        hBox.addWidget(self.keywordEdit, 0)
        # hBox.addWidget(self.findTopKButton, 0)
        # hBox.addWidget(self.findRangeButton, 0)
        hWidget = QWidget()
        hWidget.setLayout(hBox)
        self.mainLayout.addWidget(hWidget, 1, 1, 1, 6)

    def setExcelTopk(self):
        if not self.check():
            return
        k = self.kEdit.text()
        keyword = self.keywordEdit.text()

        k = int(k)
        csv_file = self.file.fillna("").astype(str)
        self.data = [" ".join(list(csv_file.iloc[x])) for x in range(len(csv_file))]
        if keyword == '':
            topKInfo = findTopK(self.file, self.longitude, self.latitude, k)
        else:
            topKInfo = findTopKWithKeyWord(self.file,self.longitude,self.latitude,k,keyword,self.data)

        self.table = MyTable(topKInfo, self.file)
        # self.table.show()

    def setExcelRange(self):
        if not self.check():
            return

        r = self.rangeEdit.text()

        if r == "":
            QMessageBox.warning(self, "警告", "请输入range值", QMessageBox.Ok)
            return
        r = int(r)
        rangeInfo = findRange(self.file, self.longitude, self.latitude, r)
        self.table = MyTable(rangeInfo, self.file)

    def check(self):
        self.longitude = self.longitudeEdit.text()
        self.latitude = self.latitudeEdit.text()

        if self.longitude == "":
            QMessageBox.warning(self, "警告", "请输入经度", QMessageBox.Ok)
            return False

        try:
            self.longitude = float(self.longitude)
            if self.longitude > 180 or self.longitude < -180:
                QMessageBox.warning(self, "错误", "经度在-180~180之间", QMessageBox.Ok)
                return False
        except:
            QMessageBox.warning(self, "错误", "请输入数字", QMessageBox.Ok)
            return False

        if self.latitude == "":
            QMessageBox.warning(self, "警告", "请输入纬度", QMessageBox.Ok)
            return False

        try:
            self.latitude = float(self.latitude)
            if self.latitude > 90 or self.latitude < -90:
                QMessageBox.warning(self, "错误", "纬度在-90~90之间", QMessageBox.Ok)
                return False
        except:
            QMessageBox.warning(self, "错误", "请输入数字", QMessageBox.Ok)
            return False
        return True

    def findTopkTu(self):
        if not self.check():
            return
        k = self.kEdit.text()
        keyword = self.keywordEdit.text()

        k = int(k)
        csv_file = self.file.fillna("").astype(str)
        self.data = [" ".join(list(csv_file.iloc[x])) for x in range(len(csv_file))]
        # import pickle
        # with open("html/directory.pickledata", 'rb') as f:
        #     self.data = pickle.load(f)
        self.showInWebEngineView('/html/index.html')
        self.t = DrawThread(target=drawTopkMap,
                            args=(self.file,
                                  self.longitude,
                                  self.latitude,
                                  k,
                                  keyword,
                                  self.data,
                                  'html/topk1.html', 'top图')
                            )
        self.t.endTrigger.connect(lambda: self.showInWebEngineView('/html/topk1.html'))
        self.t.start()

    def findRangeTu(self):
        if not self.check():
            return

        r = self.rangeEdit.text()

        if r == "":
            QMessageBox.warning(self, "警告", "请输入range值", QMessageBox.Ok)
            return

        r = int(r)
        self.showInWebEngineView('/html/index.html')
        self.t = DrawThread(target=drawRangeMap,
                            args=(self.file,
                                  self.longitude,
                                  self.latitude,
                                  r,
                                  'html/RangeMap.html', '距离range图'))
        self.t.endTrigger.connect(lambda: self.showInWebEngineView('/html/RangeMap.html'))
        self.t.start()

    def showInWebEngineView(self, fileName):
        self.webEngine.load(QUrl.fromLocalFile(fileName))

    def drawMap(self):
        self.showInWebEngineView('/html/temp-plot.html')

    def drawColorMaps(self):
        self.showInWebEngineView('/html/guojiashulaing.html')

    def drawLongitudeMap(self):
        self.showInWebEngineView('/html/时区散点图.html')

    def drawTimezonecolor(self):
        self.showInWebEngineView('/html/timezone.html')

    def drawTimezoneBar(self):
        self.showInWebEngineView('/html/bar-timezone.html')

    def drawTimezonePie(self):
        self.showInWebEngineView('/html/timezone_pie_chart.html')

    def drawCountryBar(self):
        self.showInWebEngineView('/html/bar-country.html')

    def drawCountryPie(self):
        self.showInWebEngineView('/html/country_pie_chart.html')

    # 窗口居中
    def center(self):
        self.resize(900, 600)
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - self.width()) // 2
        y = (desktop.height() - self.height()) // 2
        self.move(x, y)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建一个应用对象 ,sys.argv 是提供对脚本控制功能的参数
    # 实例化对象
    ex = UI()
    # 结束应用的主循环，主循环是从窗口系统中接受时间并快速的法网应用窗口，调用exit()方法或者主窗口关闭时，主循环结束
    # sys.exec_()方法是确保关闭干净
    sys.exit(app.exec_())