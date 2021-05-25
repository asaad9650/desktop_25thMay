
from PyQt5 import QtCore,  QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow,QLabel,QLineEdit,QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PyQt5.QtGui import QIcon
from FirstForm import mainWindow

import sys

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('Log.ui',self)
        self.setWindowIcon(QIcon('Wallpaper/door.png'))
        self.setWindowTitle('Log In')
        self.val_2.setText('')
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.signupBtn.clicked.connect(self.on_signup)


    @pyqtSlot()
    def on_signup(self):
        from signup import Signup
        self.s=Signup()
        self.s.show()
        self.hide()




    @pyqtSlot()
    def on_pushButton_clicked(self):

        if str(self.n_txtbox.text())=="" :

            self.val_2.setText('Required User Name!')
            # vt.text2speech('Enter User Name')
        elif str(self.lineEdit_2.text())=="":
            self.val_2.setText('Required Password!')
            # vt.text2speech('Enter Password')
        else:
            try:
                ref = db.reference('/user').child(self.n_txtbox.text())
                self.u_name = ref.child('username').get()
                self.pas = ref.child('password').get()
                # print(self.u_name,self.pas)
                if (self.n_txtbox.text()==self.u_name) and (self.lineEdit_2.text()==self.pas):
                    # print(self.n_txtbox.text(),self.lineEdit_2.text())
                    self.f=mainWindow()
                    self.f.show()
                    self.hide()

                else:
                    self.val_2.setText('User Name OR Password Is Incorrect')
                    # vt.text2speech('User Name OR Password Is Incorrect')

            except:
                self.val_2.setText('Network Error!')
                # vt.text2speech('Network Error, Please check your internet connection')



if __name__ == "__main__":
    import sys


    app = QApplication(sys.argv)
    ui = Login()
    ui.setWindowIcon(QIcon('Wallpaper/door.png'))
    ui.setWindowTitle('Log In')
    ui.show()
    # vt.text2speech("Please Enter Your User Name And Password")
    sys.exit(app.exec_())