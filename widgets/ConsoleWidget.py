from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QListWidgetItem, QPushButton, QLineEdit
from PyQt5.QtGui import QFontMetrics, QTextCursor

from UI import ConsoleWidget as CW

class ConsoleWidget():
    def __init__(self, parent):
        self.parent = parent
        self.widget = CW.Ui_Form()
        self.widget.setupUi(self.parent)
        self.console =  self.widget.console



        self.setMinHeight(1)
        self.setMaxHeight(15)
        self.setFont()


    def setMinHeight(self, nRows):
        self.lineEditRef = QLineEdit(self.parent)
        self.lineEditRef.setStyleSheet("")
        height = self.lineEditRef.geometry().height() 
        self.lineEditRef.setParent(None)
        #metric = QFontMetrics(self.console.font())
        #rowHeight = metric.lineSpacing()
        #self.console.setMinimumHeight(nRows * textMargins[1])
        self.console.setMinimumHeight( height )


    def setMaxHeight(self, nRows):
        metric = QFontMetrics(self.console.font())
        rowHeight = metric.lineSpacing()
        self.console.setMaximumHeight(nRows * rowHeight)
        self.parent.setMaximumHeight(nRows * rowHeight)
    
    def setFont(self):
        font = QLineEdit().font()  
        self.console.setCurrentFont(font)

    def writeToConsole(self, text):
       """Append text to the QTextEdit."""
       cursor = self.console.textCursor()
       cursor.movePosition(QTextCursor.End)
       cursor.insertText(text)
       self.console.setTextCursor(cursor)
       self.console.ensureCursorVisible()



        