# pylint: disable=all
import cv2
import json
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QImage, QFont

from ui.ui_inspection import Ui_InspectionWindow
from src.camera import Camera

REPORTS_FILE = 'pcb_reports.cvs'
BOARDS_DIR = 'boards'
LED_TOP = 17
LED_BOTTOM = 27


class Signals(QObject):
    close = pyqtSignal()


class InspectionWindow(QtWidgets.QMainWindow, Ui_InspectionWindow):
    def __init__(self, main_window, selected_board):
        super(InspectionWindow, self).__init__()
        self.selected_board = selected_board
        self.main_window = main_window
        self.screen_widht = main_window.size().width()
        self.screen_height = main_window.size().height()
        self.main_image_width = self.screen_widht//2
        self.main_image_height = self.screen_height//2
        
        self.setupUi(self)
        self.init_ui()

        self.reports_df = None
        self.load_reports()

        self.signals = Signals()
        self.camera = Camera(0)
        self.timer = QTimer()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_TOP, GPIO.OUT)
        GPIO.setup(LED_BOTTOM, GPIO.OUT)

        self.timer.timeout.connect(self.nextFrameSlot)
        self.frame = None

        self.show()
    
    def init_ui(self):
        self.btn_start_camera.clicked.connect(self.start)
        self.btn_stop_camera.clicked.connect(self.stop)
        self.btn_capturar_imagem.clicked.connect(self.process_image)
        self.btn_back.clicked.connect(self.back_window)

        self.btn_stop_camera.setEnabled(False)
        self.btn_capturar_imagem.setEnabled(False)
    
    def back_window(self):
        self.main_window.show()
        self.hide()

        self.signals.close.emit()
    
    def start(self):
        for i in reversed(range(self.scrollLayout.count())): 
            self.scrollLayout.itemAt(i).widget().setParent(None)
    
        self.btn_start_camera.setEnabled(False)
        self.btn_capturar_imagem.setEnabled(True)
        self.btn_stop_camera.setEnabled(True)
        
        GPIO.output(LED_TOP, GPIO.HIGH)
        GPIO.output(LED_BOTTOM, GPIO.HIGH)

        self.camera.openCamera()
        self.timer.start(int(1000. / 24))

    def stop(self):
        self.btn_start_camera.setEnabled(True)
        self.btn_capturar_imagem.setEnabled(False)
        self.btn_stop_camera.setEnabled(False)
        
        GPIO.output(LED_TOP, GPIO.LOW)
        GPIO.output(LED_BOTTOM, GPIO.LOW)

        self.camera.closeCamera()
        self.timer.stop()
        self.label.clear()

    def load_reports(self):
        self.reports_df = pd.read_csv(REPORTS_FILE, index_col=False)

    def nextFrameSlot(self):
        rval, frame = self.camera.vc.read()
        if rval:
            frame = cv2.flip(frame, 180)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = frame

            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(self.main_image_width, self.main_image_height, Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
        else:
            self.stop()
            print("Falha ao capturar obter imagem da câmera.")
    
    def array_to_label(self, input_array, output_label):
        output_label.setFixedHeight(self.qframe_for_list.height()//4)
        
        if len(input_array.shape) == 3:
            height, width, channels = input_array.shape
            bytesPerLine = channels * width
            qImg = QImage(input_array.data, width, height, bytesPerLine, QImage.Format_RGB888)
        else:
            height, width = input_array.shape
            qImg = QImage(input_array.data, width, height, width, QImage.Format_Grayscale8)

        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)

        output_label.setPixmap(pixmap_image.scaled(output_label.width(), output_label.height(), Qt.KeepAspectRatio))
    
    def process_filters(self, method_name, input_params, input_img):
        if method_name == 'dilate':
            output_img = cv2.dilate(
                input_img,
                kernel=np.ones((input_params[0], input_params[0]), np.uint8),
                iterations=input_params[1]
            )
        else:
            method = getattr(cv2, method_name)
            if type(input_params) == list:
                input_params = list(map(int, input_params))
                output_img = method(input_img, *input_params)
            else:
                param = getattr(cv2, input_params)
                output_img = method(input_img, param)

        return output_img

    def process_identifier(self, method_name, equal, min, max, input_img):
        method = getattr(cv2, method_name)
        result = method(input_img)

        if equal is not None:
            return (result == equal)
        else:
            return (min <= result <= max)
    
    def process_item(self, script, input_img):
        output_img = None
        
        for i, filter in enumerate(script['filters']):
            if output_img is None:
                output_img = self.process_filters(
                    method_name=filter['method'],
                    input_params=filter['params'],
                    input_img=input_img
                )
            else:
                output_img = self.process_filters(filter['method'], filter['params'], output_img)
        
        identifier = script['identifier']
        result = self.process_identifier(
            method_name=identifier['method'],
            equal=identifier['equal'],
            min=identifier['min'],
            max=identifier['max'],
            input_img=output_img
        )
        
        return output_img, result

    def process_image(self):
        self.stop()

        data = json.load(open(f"{BOARDS_DIR}/{self.selected_board}.json"))
        general_result = True
        f = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite("img_1.png", f)

        for item_name in data.keys():
            res_widget = QtWidgets.QWidget()
            res_layout = QtWidgets.QHBoxLayout()
            res_lbl_name = QtWidgets.QLabel(text=item_name)
            res_lbl_name.setFont(QFont('Arial', 14))
            res_lbl_input_img = QtWidgets.QLabel()
            res_lbl_resul_img = QtWidgets.QLabel()
            res_lbl_result = QtWidgets.QLabel()
            res_lbl_result.setFont(QFont('Arial', 14))

            x1 = data[item_name]['pos'][0]
            x2 = data[item_name]['pos'][2]
            y1 = data[item_name]['pos'][1]
            y2 = data[item_name]['pos'][3]
            
            cropped_img = np.array(self.frame[y1:y2, x1:x2])

            output_img, result = self.process_item(script=data[item_name], input_img=cropped_img)
            if result:
                res_lbl_result.setText("Aprovado")
                res_lbl_result.setStyleSheet('color: green')
            else:
                general_result = False
                res_lbl_result.setText("Reprovado")
                res_lbl_result.setStyleSheet('color: red')

            self.array_to_label(cropped_img, res_lbl_input_img)
            self.array_to_label(output_img, res_lbl_resul_img)

            res_layout.addWidget(res_lbl_name)
            res_layout.addWidget(res_lbl_input_img)
            res_layout.addWidget(res_lbl_resul_img)
            res_layout.addWidget(res_lbl_result)
            res_widget.setLayout(res_layout)
            res_widget.setFixedWidth(self.qframe_for_list.width())
            
            self.scrollLayout.addWidget(res_widget)     

        if general_result:
            self.reports_df.loc[self.reports_df["name"] == self.selected_board, "passed"] += 1
        else:
            self.reports_df.loc[self.reports_df["name"] == self.selected_board, "failed"] += 1
        self.reports_df.loc[self.reports_df["name"] == self.selected_board, "total"] += 1

        self.reports_df.to_csv(REPORTS_FILE, index=False)
