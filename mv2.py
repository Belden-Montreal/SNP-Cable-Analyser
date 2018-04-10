from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets

import sys

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    
    #DATA
    
    data = [ "one", "two", "three" , "four", "five"]

    listView = QtWidgets.QListView()    
    listView.show()

    model = QtCore.QStringListModel(data)
    
    listView.setModel(model)
    
    
    combobox = QtWidgets.QComboBox()
    combobox.setModel(model)
    combobox.show()
    
    listView2 = QtWidgets.QListView()
    listView2.show()
    listView2.setModel(model)

    print data

    sys.exit(app.exec_())
