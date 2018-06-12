import sys
import pandas as pd
from PyQt5.QtWidgets import *
import threading


class MyTable(QWidget):
    def __init__(self, search_file, csv_file):
        super(MyTable, self).__init__()
        self.search_file = search_file
        self.csv_file = csv_file
        self.setWindowTitle("查询表格")
        self.resize(650, 450)
        self.table = QTableWidget(self)
        self.messageBox = QMessageBox(self)

        self.table.setColumnCount(4)
        self.table.setRowCount(len(self.search_file))

        # 设置表头
        self.table.setHorizontalHeaderLabels(['店铺名', '地址', '评分','评分次数'])

        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        # 设置为选中一行，默认为选中单格
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.btn_save = QPushButton('保存')
        self.btn_save.clicked.connect(self.save)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.table)
        self.vbox.addWidget(self.btn_save)
        self.rowToIndexMap = dict()
        cnt = 0
        for index, file in self.search_file.iterrows():
            # print(index)
            self.rowToIndexMap[cnt] = index#此处的index是查询结果在原来表中的索引号，而不是根据列数形成的默认从0开始的索引号
            self.table.setItem(cnt, 0, QTableWidgetItem(file['Store Name']))
            self.table.setItem(cnt, 1, QTableWidgetItem(str(file['Street Address'])))
            # print(file['index'], file['Store Name'])
            if ( file['Score'] != ''):
                gradeItem = QTableWidgetItem(str(file['Score']))
                self.table.setItem(cnt, 2, gradeItem)
            else :
                self.table.setItem(cnt, 2, QTableWidgetItem(''))
            self.table.setItem(cnt, 3, QTableWidgetItem(str(file['Time'])))
            cnt += 1

        self.setLayout(self.vbox)
        self.table.cellChanged.connect(self.contentClicked)
        self.show()

    def save(self):
        # threading.Thread(target=self.delegateSave).start()
    # def delegateSave(self):
        self.csv_file.to_csv('directory00.csv', index=False)

    def contentClicked(self,row,col):
        item = self.table.item(row, col)
        txt = item.text()
        if float(txt) > 10 or float(txt) < 0 :
            self.messageBox.warning(self, "警告", "评分分值应在0到10之间", QMessageBox.Ok)
            return False
        else:
            if col == 2:
                threading.Thread(target=self.score, args=(row, txt)).start()

    def score(self, row, txt):
        index = int(self.rowToIndexMap[row])
        times = float(self.csv_file.loc[index, 'Time'])
        currentScore = float(self.csv_file.loc[index, 'Score']) * times
        times += 1
        self.csv_file.loc[index, 'Score'] = round((currentScore + float(txt)) / times,2)
        self.csv_file.loc[index, 'Time'] = times

