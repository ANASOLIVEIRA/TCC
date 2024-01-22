# pylint: disable=all

import os
import sys
    
from PyQt5 import QtWidgets

from src.src_main import MainWindow

execution_dir = os.getcwd()
sys.path.append(execution_dir)

app = QtWidgets.QApplication([])
window = MainWindow(app.primaryScreen())
app.exec_()
