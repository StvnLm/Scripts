from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QComboBox, QPushButton, QGridLayout, QLabel, QSizePolicy, QGroupBox, QVBoxLayout, QDateTimeEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
import sys
import json

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(350, 200)
        self.centre()
        self.setWindowTitle('SLA Calculator')
        self.setWindowIcon(QIcon('calculator-icon.png'))
        self.gridLayoutCreation()
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.groupBox)
        self.setLayout(vboxLayout)
        self.show()

    def showResult(self):
        print('test')

    def gridLayoutCreation(self):

        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()

        calculate_button = QPushButton("Calculate")
        calculate_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        now = QDate.currentDate()
        currentdatetime = QDateTime.currentDateTime()
        start_date_edit = QDateTimeEdit()
        end_date_edit = QDateTimeEdit()
        start_date_edit.setDateTime(currentdatetime)
        end_date_edit.setDateTime(currentdatetime)

        client_combo_box = QComboBox(self)
        sev_combo_box = QComboBox(self)
        with open('data.json') as f:
            data = json.load(f)
        for client in data:
            client_combo_box.addItem(client)
        print(client_combo_box.currentText())
        client_combo_box.currentIndexChanged.connect(self.showResult)
        calculate_button.clicked.connect(self.showResult)

        print('sdfds')
            # sev_combo_box = QComboBox(self)
            # for sev in data[client_combo_box.currentText()]["SEV"]:
            #     sev_combo_box.addItem(sev)




        sev_combo_box.addItem('SEV1')
        sev_combo_box.addItem('SEV2')
        sev_combo_box.addItem('SEV3')

        gridLayout.addWidget(start_date_edit, 0, 2)
        gridLayout.addWidget(end_date_edit, 1, 2)
        gridLayout.addWidget(client_combo_box,2, 2)
        gridLayout.addWidget(sev_combo_box,3, 2)
        gridLayout.addWidget(calculate_button, 4, 2)

        labels = ['Ticket Start', 'Ticket End', 'Severity', 'Client']
        self.labels = [QLabel(label) for label in labels]
        [label.setFont(QFont("OPEN SANS", 9)) for label in self.labels]
        [gridLayout.addWidget(self.labels[i], i, 0) for i in range(len(self.labels))]

        self.groupBox.setLayout(gridLayout)




    def centre(self):
        # Geometry of main window
        window = self.frameGeometry()
        centre = QDesktopWidget().availableGeometry().center()
        window.moveCenter(centre)
        self.move(window.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Interface()
    sys.exit(app.exec_())
