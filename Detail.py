from PyQt5 import QtCore,  QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from firebase_admin import db
from FirstForm import mainWindow

class details(QDialog):
    def __init__(self):
        super(details,self).__init__()
        loadUi('detail.ui',self)
        self.tableDetail.setColumnCount(2)
        self.tableDetail.setRowCount(0)
        self.setWindowTitle('Fingerprint Details')
        self.setWindowIcon(QIcon('Wallpaper/door.png'))
        self.backBtn.clicked.connect(self.back_Btn)
        try:
            ref = db.reference('/fingerprint')
            snap = ref.order_by_child("name").get()

            for key, val, in snap.items():
                numRow = self.tableDetail.rowCount()
                self.tableDetail.insertRow(numRow)
                email = val['email']
                name = val['name']
                self.tableDetail.setItem(numRow, 0, QtWidgets.QTableWidgetItem(name))
                self.tableDetail.setItem(numRow, 1, QtWidgets.QTableWidgetItem(email))
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('Wallpaper/door.png'))
            msg.setText("Something Went Wrong!")
            msg.setInformativeText("Please Check Your Internet Connection")
            msg.setWindowTitle("Network Error")
            msg.exec_()


    @pyqtSlot()
    def back_Btn(self):
        self.f=mainWindow()
        self.f.show()
        self.hide()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = details()
    ui.setWindowTitle('Entry Details')
    ui.setWindowIcon(QIcon('Wallpaper/door.png'))
    ui.show()
    sys.exit(app.exec_())