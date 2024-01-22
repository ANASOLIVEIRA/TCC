# pylint: disable=all

from PyQt5.QtWidgets import QMessageBox

import cv2

class Camera:

    def __init__(self, camera):
        self.camera = camera
        self.cap = None
        self.vc = None

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        self.vc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        self.vc.set(3, 1280)
        self.vc.set(4, 720)

        if not self.vc.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Falha ao abrir a câmera.")
            msgBox.exec_()
            return
    
    def closeCamera(self):
        if self.vc is not None:
            self.vc.release()
