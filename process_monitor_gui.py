from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QTableWidget, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
import sys
from process_monitor import ProcessMonitor
from datetime import datetime

class ProcessMonitorGui(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Process Monitor")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout_widget = QWidget(central_widget)
        main_layout = QHBoxLayout(main_layout_widget)

        vertical_layout_widget = QWidget(main_layout_widget)
        get_input_layout = QVBoxLayout(vertical_layout_widget)
        self.process_name = QTextEdit(parent=vertical_layout_widget)
        self.process_name.setPlaceholderText('Enter process name')
        get_input_layout.addWidget(self.process_name)
        self.monitoring_duration = QTextEdit(parent=vertical_layout_widget)
        self.monitoring_duration.setPlaceholderText('Enter monitoring duration in seconds')        
        get_input_layout.addWidget(self.monitoring_duration)
        self.polling_time = QTextEdit(parent=vertical_layout_widget)
        self.polling_time.setPlaceholderText('Enter polling time in seconds')
        get_input_layout.addWidget(self.polling_time)
        self.confirm_button = QPushButton("Begin process monitoring", vertical_layout_widget)
        self.confirm_button.clicked.connect(self.process_data)
        get_input_layout.addWidget(self.confirm_button)
        self.write_button = QPushButton("Write to CSV", vertical_layout_widget)
        self.write_button.clicked.connect(self.write_to_csv)
        get_input_layout.addWidget(self.write_button)
        main_layout.addWidget(vertical_layout_widget)

        self.table = QTableWidget(1, 4, main_layout_widget)  
        self.table.setItem(0, 0, QTableWidgetItem('Timestamp'))
        self.table.setItem(0, 1, QTableWidgetItem('Cpu Percentage'))
        self.table.setItem(0, 2, QTableWidgetItem('Private Memory'))
        self.table.setItem(0, 3, QTableWidgetItem('File Handles'))
        main_layout.addWidget(self.table) 
        self.showMaximized()

    def process_data(self):  
        process_name = self.process_name.toPlainText()
        monitoring_duration = int(self.monitoring_duration.toPlainText())
        polling_time = int(self.polling_time.toPlainText())
        self.process_utils =  ProcessMonitor(process_name, monitoring_duration, polling_time)
        self.process_utils.gather_data() 

        for index in range(len(self.process_utils.timestamps)):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(self.process_utils.timestamps[index]))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(self.process_utils.cpu_percentages[index])))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(self.process_utils.memory_values[index])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(self.process_utils.file_handles[index])))
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem('timestamp'))
        self.table.setItem(row_position, 1, QTableWidgetItem('Average Cpu Percentage'))
        self.table.setItem(row_position, 2, QTableWidgetItem('Average Private Memory'))
        self.table.setItem(row_position, 3, QTableWidgetItem('Average File Handles'))
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(str(datetime.utcnow())))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(self.process_utils.cpu_average)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(self.process_utils.memory_average)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(self.process_utils.files_average)))
        if self.process_utils.memory_values == sorted(self.process_utils.memory_values):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 2, QTableWidgetItem('Possible memory leak!'))

    def write_to_csv(self):
        self.process_utils.write_to_csv()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProcessMonitorGui()
    sys.exit(app.exec())