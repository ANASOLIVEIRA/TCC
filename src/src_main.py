# pylint: disable=all
import os
import pandas as pd

from PyQt5 import QtWidgets

from ui.ui_main import Ui_Main
from src.src_inspection import InspectionWindow

REPORTS_FILE = 'pcb_reports.cvs'
BOARDS_DIR = 'boards'

class MainWindow(QtWidgets.QMainWindow, Ui_Main):
    def __init__(self, screen):
        super(MainWindow, self).__init__()
        self.screen_widht = screen.size().width()
        self.screen_height = screen.size().height()

        self.setupUi(self)
        self.init_ui()

        self.reports_df = None
        self.load_reports()

        self.show()
    
    def init_ui(self):
        self.btn_run_inspection.clicked.connect(self.run_inspection)
        self.btn_change_status.clicked.connect(self.change_status)
        self.btn_close.clicked.connect(self.close)
        
    def run_inspection(self):
        if not self.table_board_list.selectedItems():
            return
        
        row = self.table_board_list.currentItem().row()
        selected_board = self.table_board_list.item(row, 0).text()
        selected_status = self.table_board_list.item(row, 4).text()

        if selected_status == "Inativo":
            self.show_error_msg(selected_board=selected_board)
            return
        
        self.run_inspection_window = InspectionWindow(main_window=self, selected_board=selected_board)
        self.run_inspection_window.signals.close.connect(self.load_reports)
        self.run_inspection_window.showFullScreen()
        self.hide()
    
    def show_error_msg(self, selected_board):
        message = f"<p style='text-align: center;'>A {selected_board} placa está com status INATIVO.</p>\n"
        message += "<p style='text-align: center;'>Modifique o status para ATIVO antes de iniciar a inspeção."
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("<p style='text-align: center;'>Falha ao iniciar inspeção!</p>")
        msg.setInformativeText(message)
        msg.setWindowTitle("PLACA INATIVA")
        msg.exec_()

    def change_status(self):
        if not self.table_board_list.selectedItems():
            return
        
        self.btn_change_status.setEnabled(False)
        
        row = self.table_board_list.currentItem().row()
        name = self.table_board_list.item(row, 0).text()
        current_status = self.table_board_list.item(row, 4).text()
        new_status = "Ativo" if current_status == "Inativo" else "Inativo"
        
        self.reports_df.loc[self.reports_df["name"] == name, "status"] = new_status
        self.reports_df.to_csv(REPORTS_FILE, index=False)
        
        self.table_board_list.setItem(row, 4, QtWidgets.QTableWidgetItem(new_status))
        self.btn_change_status.setEnabled(True)
    
    def clear_table(self):
        while(self.table_board_list.rowCount() > 0):
            self.table_board_list.removeRow(0)

    def load_reports(self):
        self.clear_table()

        if os.path.isfile(REPORTS_FILE):
            self.reports_df = pd.read_csv(REPORTS_FILE, index_col=False)
        else:
            reports_dict = {
                'name': [],
                'passed': [],
                'failed': [],
                'total': [],
                'status': [] 
            }
            self.reports_df = pd.DataFrame(reports_dict)
            self.reports_df.to_csv(REPORTS_FILE, index=False)
 
        boards_in_folder = sorted([os.path.splitext(filename)[0] for filename in os.listdir(BOARDS_DIR)])
        boards_in_report = sorted(list(self.reports_df['name']))

        if boards_in_folder != boards_in_report:
            for board in boards_in_folder:
                if board not in list(self.reports_df['name']):
                    self.reports_df.loc[len(self.reports_df)] = [board, 0, 0, 0, "Inativo"]
            self.reports_df.to_csv(REPORTS_FILE, index=False)
        
        self.reports_df = self.reports_df.sort_values(by=['status', 'name'])

        for index in range(len(self.reports_df)):
            self.table_board_list.insertRow(index)
            self.table_board_list.setItem(index , 0, QtWidgets.QTableWidgetItem(self.reports_df.iloc[index]['name']))
            self.table_board_list.setItem(index , 1, QtWidgets.QTableWidgetItem(str(self.reports_df.iloc[index]['passed'])))
            self.table_board_list.setItem(index , 2, QtWidgets.QTableWidgetItem(str(self.reports_df.iloc[index]['failed'])))
            self.table_board_list.setItem(index , 3, QtWidgets.QTableWidgetItem(str(self.reports_df.iloc[index]['total'])))
            self.table_board_list.setItem(index , 4, QtWidgets.QTableWidgetItem(self.reports_df.iloc[index]['status']))
    