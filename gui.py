#based on http://zetcode.com/gui/pyqt5/
#the gui is not very robust, because I haven't used threading
#but it works

import sys
import os
from gatherer import goGather
from naiveOrderer import goOrderNaive
from naiveChainer import goChainNaive
from posOrderer import goOrderPOS
from posChainer import goChainPOS
from PyQt5.QtWidgets import QScrollArea, QComboBox, QVBoxLayout, QHBoxLayout, QProgressBar, QApplication, QWidget, QPushButton, QGridLayout, QTextEdit, QLabel, QLineEdit
from PyQt5.QtCore import Qt

Successful = 0
NoResults = 1
NoArticlesFound = 2
NoQuery = 3


class Feischter(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #define all labels
        suchwort = QLabel('Suchwort:')
        dLoad = QLabel('Download:')
        ord = QLabel('Ordnen:')
        output = QLabel('Output:')
        result = QLabel('')
        #suchfenster
        self.suchwortedit = QLineEdit()
        #use a sublayout to keep it cleaner
        subSuch = QVBoxLayout()
        subSuch.addWidget(suchwort)
        subSuch.addWidget(self.suchwortedit)

        #define the parameters
        tituLabel = QLabel('Titeltiefe:')
        houptLabel = QLabel('Haupttiefe:')
        azau = QLabel('Anzahl Ketten:')

        self.tituCombo = QComboBox(self)
        self.houptCombo = QComboBox(self)
        self.azauCombo = QComboBox(self)
        #get the boxes range 1 to 8
        for i in range(1, 8):
            self.tituCombo.addItem(str(i))
            self.houptCombo.addItem(str(i))
            self.azauCombo.addItem(str(i))

        #make sublayouts for every parameter
        subTitu = QHBoxLayout()
        subTitu.addWidget(tituLabel)
        subTitu.addWidget(self.tituCombo)

        subHoupt = QHBoxLayout()
        subHoupt.addWidget(houptLabel)
        subHoupt.addWidget(self.houptCombo)

        subAzau = QHBoxLayout()
        subAzau.addWidget(azau)
        subAzau.addWidget(self.azauCombo)

        #define the buttons for the different modes
        subButton = QHBoxLayout()
        naiveButton = QPushButton('Naive', self)
        posButton = QPushButton('PoS', self)
        naiveButton.clicked.connect(self.naiveGo)
        posButton.clicked.connect(self.posGo)
        subButton.addWidget(naiveButton)
        subButton.addWidget(posButton)
        #define the progressbars
        self.dLoadProgress = QProgressBar(self)
        self.dLoadProgress.setGeometry(30, 40, 280, 25)

        self.orderProgress = QProgressBar(self)
        self.orderProgress.setGeometry(30, 40, 280, 25)

        #put the output in a scrollingarea to read all
        self.resultArea = QScrollArea()
        self.resultArea.setWidget(result)

        #define the gridlayout
        grid = QGridLayout()
        grid.addLayout(subSuch, 0, 0, 1, 6)
        grid.addLayout(subTitu, 2, 0, 1, 2)
        grid.addLayout(subHoupt, 2, 2, 1, 2)
        grid.addLayout(subAzau, 2, 4, 1, 2)
        grid.addLayout(subButton, 3, 0, 1, 6)
        grid.addWidget(dLoad, 4, 0)
        grid.addWidget(self.dLoadProgress, 5, 0, 1, 6)
        grid.addWidget(ord, 6, 0)
        grid.addWidget(self.orderProgress, 7, 0, 1, 6)
        grid.addWidget(output, 8, 0)
        grid.addWidget(self.resultArea, 9, 0, 4, 6)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('NLZMarkov')
        self.show()

    #the function for the PoS button
    def posGo(self):
        #set the progressbar to 0
        self.dLoadProgress.setValue(0)
        self.orderProgress.setValue(0)
        #get the parameters from the user
        query = self.suchwortedit.text()
        sectionDepths = [
            int(self.tituCombo.currentText()),
            int(self.houptCombo.currentText())
        ]
        nomere = int(self.azauCombo.currentText())
        #download the queryword, give progress in progbar
        success = goGather(query, self.dLoadProgress)
        if success == Successful:
            #successful
            dicts = goOrderPOS(sectionDepths, query, self.orderProgress)
            #get the text
            text = goChainPOS(sectionDepths, dicts, nomere)
        elif (success == NoResults):
            text = 'There are no results for the query.'
        elif (success == NoArticlesFound):
            text = 'Cant reach articles on net.'
        elif (success == NoQuery):
            text = 'No query word given.'
        #make a widget for the result
        resultWidget = QLabel(text)
        #make it copyable
        resultWidget.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        resultWidget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultArea.setWidget(resultWidget)

    #the function for the naive button
    def naiveGo(self):
        #set the progressbar to 0
        self.dLoadProgress.setValue(0)
        self.orderProgress.setValue(0)
        #get the parameters from the user
        query = self.suchwortedit.text()
        sectionDepths = [
            int(self.tituCombo.currentText()),
            int(self.houptCombo.currentText())
        ]
        nomere = int(self.azauCombo.currentText())
        #download the queryword, give progress in progbar
        success = goGather(query, self.dLoadProgress)
        if success == Successful:
            #successful
            dicts = goOrderNaive(sectionDepths, query, self.orderProgress)
            #get the text
            text = goChainNaive(sectionDepths, dicts, nomere)
        elif (success == NoResults):
            text = 'There are no results for the query.'
        elif (success == NoArticlesFound):
            text = 'Cant reach articles on net.'
        elif (success == NoQuery):
            text = 'No query word given.'
        #make a widget for the result
        resultWidget = QLabel(text)
        #make it copyable
        resultWidget.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        resultWidget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultArea.setWidget(resultWidget)


if __name__ == '__main__':
    #well, start the gui
    app = QApplication(sys.argv)
    ex = Feischter()
    app.exec_()
