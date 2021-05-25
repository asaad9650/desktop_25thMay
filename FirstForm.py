import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage,QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from firebase_admin import db
from PyQt5.QtCore import pyqtSlot
from persondetection import Pedestrien,ROI
import imutils
from threading import Thread


class mainWindow(QDialog):


    def __init__(self):
        super(mainWindow,self).__init__()
        loadUi('FirstFor.ui',self)
        self.setWindowIcon(QIcon('Wallpaper/door.png'))
        self.setWindowTitle('Recognition')

        self.detailBtn.clicked.connect(self.Detail_Btn)
        self.logoutBtn.clicked.connect(self.Logout_Btn)
        self.startButton.clicked.connect(self.start_webcam)
        self.resetButton.clicked.connect(self.resetIntrusion)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.lockBtn.clicked.connect(self.lock_door)
        self.int_btn.clicked.connect(self.intrusion)
        self.closeBtn.clicked.connect(self.close_button)
        self.check = 0
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(False)

    @pyqtSlot()
    def intrusion(self):
        ROI()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.resetButton.setEnabled(True)

    @pyqtSlot()
    def resetIntrusion(self):
        if self.check == 1:
            self.timer.stop()
            self.check = 0
            self.hide()
            self.show()
        else:
            self.check = 1
            self.hide()
            self.show()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
    def Logout_Btn(self):
        from login import Login
        if self.check == 1:
            self.timer.stop()
            self.check = 0
            self.l = Login()
            self.l.show()
            self.hide()
        else:
            self.check = 1
            self.l = Login()
            self.l.show()
            self.hide()


    @pyqtSlot()
    def Detail_Btn(self):
        from Detail import details
        if self.check == 1:
            self.timer.stop()
            self.check = 0
            self.d = details()
            self.d.show()
            self.hide()
        else:
            self.check = 1
            self.d = details()
            self.d.show()
            self.hide()

    @pyqtSlot()
    def lock_door(self):
        ref = db.reference('/door_lock')
        ref.set({'value': 'The Door is lock'})
    @pyqtSlot()
    def close_button(self):
        ref = db.reference('/door_lock')
        ref.set({'value': 'The Door is unlock'})
    @pyqtSlot()
    def start_webcam(self):

        self.capture = cv2.VideoCapture('1.mp4') #start camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()
        self.check = 1

    @pyqtSlot()
    def update_frame(self):
        ret,self.image=self.capture.read()
        self.image = imutils.resize(self.image, width=900)

        self.d_image = Pedestrien(self.image) #passing to the method
        t1=Thread(target=self.displayImage(self.d_image)) #passing image to the display method
        t1.start()
        t1.join()

    @pyqtSlot()
    def stop_webcam(self):
        self.timer.stop()



    @pyqtSlot()
    def displayImage(self,img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        #BGR>>RGB
        outImage = outImage.rgbSwapped()
        self.processedImgLabel.setPixmap(QPixmap.fromImage(outImage))
        self.processedImgLabel.setScaledContents(True)

if __name__ == "__main__":
    import sys
    # thread1 = threading.Thread(target=mainWindow())

    app = QApplication(sys.argv)
    ui = mainWindow()
    ui.setWindowIcon(QIcon('Wallpaper/door.png'))
    ui.setWindowTitle('Recognition')
    ui.show()
    sys.exit(app.exec_())