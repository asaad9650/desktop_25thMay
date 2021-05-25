import firebase_admin
from PyQt5.QtWidgets import QApplication, QDialog,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from firebase_admin import db, credentials
from PyQt5.QtGui import QIcon


import sys


class Signup(QDialog):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi('signup.ui', self)
        self.setWindowIcon(QIcon('Wallpaper/door.png'))
        self.setWindowTitle('Sign Up')
        self.val_2.setText('')
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.loginBtn.clicked.connect(self.on_login)

    @pyqtSlot()
    def on_login(self):
        from login import Login
        self.l=Login()
        self.l.show()
        self.hide()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        ref = db.reference("/user").child(self.n_txtbox.text()).get()
        if str(self.n_txtbox.text()) == "":
            self.val_2.setText('*Required User Name!')
        elif ref == self.n_txtbox.text() != "":
            # ref = db.reference("/user").child(self.n_txtbox.text()).get()
            # if ref== self.n_txtbox.text():
            self.val_2.setText('User Name Already Exist!')

        elif str(self.lineEdit_2.text()) == "" or str(self.lineEdit_3.text()) == "":
            self.val_2.setText('*Required Password!')
            # vt.text2speech('Enter Password')
        elif str(self.lineEdit_2.text()) != str(self.lineEdit_3.text()):
            self.val_2.setText('*Password Should Be Same!')

        else:
            try:
                entry = db.reference("/user").child(self.n_txtbox.text())
                entry.set({'username': self.n_txtbox.text(), 'password': self.lineEdit_2.text()})
                # print(self.n_txtbox.text())
                # self.n_txtbox.setText("")
                # self.lineEdit_2.setText("")
                # self.lineEdit_3.setText("")
                from login import Login
                self.l = Login()
                self.l.show()
                self.hide()



                # self.msg = QMessageBox()
                # self.msg.setIcon(QMessageBox.Information)
                # self.msg.setWindowIcon(QIcon('Wallpaper/door.png'))
                # self.msg.setText("Account Created!")
                # self.msg.setInformativeText("Your Account has been created successfully.")
                # self.msg.setWindowTitle("Account Created")
                # self.msg.exec_()
                # self.val_2.setText('')




            except:
                self.val_2.setText('Network Error!')
                # vt.text2speech('Network Error, Please check your internet connection')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Signup()
    ui.setWindowIcon(QIcon('Wallpaper/door.png'))
    ui.setWindowTitle('Sign Up')
    ui.show()
    sys.exit(app.exec_())