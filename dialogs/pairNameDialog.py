#from settings import Settings

from UI import PortNaming as PN


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox


class PairNameDialog:

    def __init__(self, pairs_names, num_pairs):
        #super(self.__class__, self).__init__()


        self.dialog = QtWidgets.QDialog()
        self.pairNameDialog = PN.Ui_PairNaming()
        self.pairNameDialog.setupUi(self.dialog)
    
        self.pairNameDialog.accept.clicked.connect(self.getPairNames)
        self.pairNameDialog.cancel.clicked.connect(self.cancel)

        self.setPairNames(pairs_names, num_pairs) 
        self.dialog.exec_()

    def getPairNames(self):
        try:
            pairs = []
            for i in range(0,16):
                pair_text_box = getattr(self.pairNameDialog, "pair_"+str(i+1))
                if pair_text_box.isEnabled():
                    pairs.append(pair_text_box.text())   
            
            self.dialog.close()

            return pairs
        
        except Exception as e:
            print("getPairNames Error : ", e)
            

        
    def setPairNames(self, pairs_names, num_pairs):
        try:
            for i in range(0,16):
                pair_text_box = getattr(self.pairNameDialog, "pair_"+str(i+1))
                if i >= num_pairs:
                    pair_text_box.setEnabled(False)
                else:
                    pair_text_box.setEnabled(True)
                    pair_text_box.setText(pairs_names[i])   
        
        except Exception as e:
            print("setPairNames Error : ", e)

    def cancel(self):
        self.dialog.close()


def main():
    app = QtWidgets.Dialog()  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()


    form = PairNameDialog()  # We set the  form to be our ExampleApp (design)

    #form.show()  # Show the form
    form.show()

    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
