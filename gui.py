#based on http://zetcode.com/gui/pyqt5/
#the gui is not very robust, because I haven't used threading
#but it works

import sys
import os
import main
from PyQt5.QtWidgets import QScrollArea, QComboBox, QVBoxLayout, QHBoxLayout, QProgressBar, QApplication, QWidget, QPushButton, QGridLayout, QTextEdit, QLabel, QLineEdit
from PyQt5.QtCore import Qt


class Feischter(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #define all labels
        suchwort = QLabel('Suchwort:')
        dload = QLabel('Download:')
        ord = QLabel('Ordnen:')
        output = QLabel('Output:')
        result = QLabel('')
        #suchfenster
        self.suchwortedit = QLineEdit()
        #use a sublayout to keep it cleaner
        subsuch = QVBoxLayout()
        subsuch.addWidget(suchwort)
        subsuch.addWidget(self.suchwortedit)

        #define the parameters
        titulabel = QLabel('Titeltiefe:')
        houptlabel = QLabel('Haupttiefe:')
        azau = QLabel('Anzahl Ketten:')

        self.titucombo = QComboBox(self)
        self.houptcombo = QComboBox(self)
        self.azaucombo = QComboBox(self)
        #get the boxes range 1 to 8
        for i in range(1, 8):
            self.titucombo.addItem(str(i))
            self.houptcombo.addItem(str(i))
            self.azaucombo.addItem(str(i))

        #make sublayouts for every parameter
        subtitu = QHBoxLayout()
        subtitu.addWidget(titulabel)
        subtitu.addWidget(self.titucombo)

        subhoupt = QHBoxLayout()
        subhoupt.addWidget(houptlabel)
        subhoupt.addWidget(self.houptcombo)

        subazau = QHBoxLayout()
        subazau.addWidget(azau)
        subazau.addWidget(self.azaucombo)

        #define the buttons for the different modes
        naivebut = QPushButton('Naive', self)
        posbut = QPushButton('PoS', self)
        naivebut.clicked.connect(self.naivefun)
        posbut.clicked.connect(self.posfun)

        #define the progressbars
        self.dprog = QProgressBar(self)
        self.dprog.setGeometry(30, 40, 280, 25)

        self.oprog = QProgressBar(self)
        self.oprog.setGeometry(30, 40, 280, 25)

        #put the output in a scrollingarea to read all
        self.resultArea = QScrollArea()
        self.resultArea.setWidget(result)

        #define the gridlayout
        grid = QGridLayout()
        grid.addLayout(subsuch, 0, 0, 1, 6)
        grid.addLayout(subtitu, 2, 0, 1, 2)
        grid.addLayout(subhoupt, 2, 2, 1, 2)
        grid.addLayout(subazau, 2, 4, 1, 2)
        grid.addWidget(naivebut, 3, 0, 1, 3)
        grid.addWidget(posbut, 3, 4, 1, 3)
        grid.addWidget(dload, 4, 0)
        grid.addWidget(self.dprog, 5, 0, 1, 6)
        grid.addWidget(ord, 6, 0)
        grid.addWidget(self.oprog, 7, 0, 1, 6)
        grid.addWidget(output, 8, 0)
        grid.addWidget(self.resultArea, 9, 0, 4, 6)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('NLZMarkov')
        self.show()

    #the function for the PoS button
    def posfun(self):
        #set the progressbar to 0
        self.dprog.setValue(0)
        self.oprog.setValue(0)
        #get the parameters from the user
        query = self.suchwortedit.text()
        sectiondepths = [
            int(self.titucombo.currentText()),
            int(self.houptcombo.currentText())
        ]
        nomere = int(self.azaucombo.currentText())
        #download the queryword, give progress in progbar
        success = main.goGather(query, self.dprog)
        if success == 0:
            #successful
            dicts = main.goposOrder(sectiondepths, query, self.oprog)
            #get the text
            text = main.goposChain(sectiondepths, dicts, nomere)
        elif (success == 1):
            text = 'There are no results for the query.'
        elif (success == 2):
            text = 'Cant reach articles on net.'
        elif (success == 3):
            text = 'No query word given.'
        #make a widget for the result
        resultwidget = QLabel(text)
        #make it copyable
        resultwidget.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        resultwidget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultArea.setWidget(resultwidget)

    #the function for the naive button
    def naivefun(self):
        #set the progressbar to 0
        self.dprog.setValue(0)
        self.oprog.setValue(0)
        #get the parameters from the user
        query = self.suchwortedit.text()
        sectiondepths = [
            int(self.titucombo.currentText()),
            int(self.houptcombo.currentText())
        ]
        nomere = int(self.azaucombo.currentText())
        #download the queryword, give progress in progbar
        success = main.goGather(query, self.dprog)
        if success == 0:
            #successful
            dicts = main.gonOrder(sectiondepths, query, self.oprog)
            #get the text
            text = main.gonChain(sectiondepths, dicts, nomere)
        elif (success == 1):
            text = 'There are no results for the query.'
        elif (success == 2):
            text = 'Cant reach articles on net.'
        elif (success == 3):
            text = 'No query word given.'
        #make a widget for the result
        resultwidget = QLabel(text)
        #make it copyable
        resultwidget.setTextInteractionFlags(Qt.TextSelectableByKeyboard)
        resultwidget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultArea.setWidget(resultwidget)


if __name__ == '__main__':
    #well, start the gui
    app = QApplication(sys.argv)
    ex = Feischter()
    app.exec_()
