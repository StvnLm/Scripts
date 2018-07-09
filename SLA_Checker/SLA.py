from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QComboBox, QPushButton, QGridLayout, QLabel, QSizePolicy, QGroupBox, QVBoxLayout, QDateTimeEdit, QMessageBox, QMainWindow, QCheckBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDateTime, Qt
from PyQt5 import QtCore

from datetime import date
import sys, json
from Program import *
from ValidDate import *
import Program

class popup(QWidget):
    def __init__(self, name):
        super().__init__()


class HolidayWindow(QWidget):

    checked_list = []

    def __init__(self):
        super().__init__()
        self.resize(450, 600)
        self.centre()
        self.setWindowTitle('Holidays')
        self.setWindowIcon(QIcon('calculator-icon.png'))
        self.initUI()
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.groupBox)
        self.setLayout(vboxLayout)
        # self.check_counter = 0
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.show()

    def centre(self):
        # Centres the window
        window = self.frameGeometry()
        centre = QDesktopWidget().availableGeometry().center()
        window.moveCenter(centre)
        self.move(window.topLeft())

    def tally_holidays(self, checkbox_list):
        check_counter = 0
        for checkbox in checkbox_list:
            if checkbox.isChecked():
                check_counter  += 1
        Interface.holiday_cnt = check_counter
        SLA.SLA_holiday_cnt = check_counter
        self.close()

    def initUI(self):
        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()

        text_label = QLabel('Select all statutory and provincial holidays that resulted in a business day turning \n'
                            'into a non-working day. Check holidays as they apply to the client local province.\n'
                            'The below displays the corresponding month, applicable prov/territory and holiday name.\n\n'
                            'Do NOT check if the statutory holiday occurs on a Saturday or Sunday as this will skew calculations! ')

        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("OPEN SANS", 8))

        label_list = ['Jan: All - New Years Day',
                    'Feb: PE - Islander Day',
                    'Feb: AB, BC, ON, SK - Family Day',
                    'Feb: NS, YK - Heritage Day',
                    'Feb: MB - Louis Riel Day',
                    'Mar: NL - St. Patricks',
                    'Mar/Apr: All except QC - Good Friday',
                    'Apr: QC - Easter Monday',
                    'Apr: NL - St. Georges Day',
                    'May: All except NB, NL, NS, PE - Victoria Day',
                    'Jun: NT -  National Aboriginal',
                    'Jun: QC - Féte Nationale',
                    'Jun: NL - Discovery Day',
                    'Jul: All - Canada Day',
                    'Jul: NT - Nunavut Day',
                    'Aug: AB, BC, NB, NU, ON, SK - Civic Holiday',
                    'Sep: All - Labour Day',
                    'Oct: All except NB, NL, NS, PE - Thanksgiving',
                    'Nov: All except NL, NS, ON, QC - Remembrance Day',
                    'Dec: All - Christmas Day',
                    'Dec: ON - Boxing Day']

        gridLayout.addWidget(text_label)
        labels = [QLabel(label) for label in label_list]
        # [label.setFont(QFont("OPEN SANS", 9)) for label in labels]

        checkbox_list = []
        for n in range(len(labels)):
            cb = QCheckBox(label_list[n])
            gridLayout.addWidget(cb, n+1, 0)
            checkbox_list.append(cb)


        confirm = QPushButton('Confirm')
        confirm.setStyleSheet('QPushButton {border-style: outset; border-width: 1px; border-radius: 3px; border-color: black; min-width: 10em; padding: 5px}'
                             'QPushButton:hover { background-color: rgba(255, 255, 255, 175) }'
                             'QPushButton:pressed {  background-color: rgba(255, 255, 255, 245) }')

        confirm.clicked.connect(lambda: self.tally_holidays(checkbox_list))

        gridLayout.addWidget(confirm)

        self.groupBox.setLayout(gridLayout)




class Interface(QWidget):

    holiday_cnt = 0

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
        holiday_cnt = 0
        self.show()


    def centre(self):
        # Centres the window
        window = self.frameGeometry()
        centre = QDesktopWidget().availableGeometry().center()
        window.moveCenter(centre)
        self.move(window.topLeft())


    def repopulateCombo(self, sev_combo_box, client_combo_box):
        sev_combo_box.clear()
        with open('data.json') as f:
            data = json.load(f)
            for key in data[client_combo_box.currentText()]['SEV'].keys():
                sev_combo_box.addItem(key)

    def check_sev(self, sev_combo_box):
        if sev_combo_box == ('severity 1' or 'severity 2'):
            self.holiday_button.setEnabled(False)
        if sev_combo_box == ('severity 3' or 'severity 4'):
            self.holiday_button.setEnabled(True)

    def calculate_press(self, start_datetime, end_datetime, client, sev, prov):
        start_string = start_datetime.dateTime().toString('yyyy M d H m')
        end_string = end_datetime.dateTime().toString('yyyy M d H m')
        st, end = [], []
        [st.append(int(char)) for char in start_string.split(' ')]
        [end.append(int(char)) for char in end_string.split(' ')]
        ticket_info = SLA(client=client, severity=sev, st_year=st[0], st_month=st[1], st_day=st[2], st_hr=st[3], st_min=st[4],
                         end_year=end[0], end_month=end[1], end_day=end[2], end_hr=end[3], end_min=end[4])
        ticket_hours = ticket_info.calculate_ticket_hrs()
        sla_hours, sla_mins = ticket_info.calculate_sla_breach(ticket_hours)
        if (datetime.datetime(st[0], st[1], st[2], st[3], st[4]) - datetime.datetime(end[0], end[1], end[2], end[3], end[4])).total_seconds() > 1:
            sla_check = f'Check start/end date and time.'
        if sla_hours < 0 or sla_mins < 0:
            sla_check = f'SLA BREACHED by {sla_hours} hrs {sla_mins} mins.'
        else:
            sla_check = f'SLA not breached.'
        # Check for holidays
        # start = datetime.date(st[0], st[1], st[3])
        # end = datetime.date(end[0], end[1], end[2])
        # holiday_list = ValidDate().holidaycheck(start, end, prov)
        # Create Pop up window
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(sla_check)
        msg.setWindowTitle('Calculations')
        # msg.setDetailedText('Holidays factored in are based on client-local statutory holidays. \n' +
        #                     'The holidays accounted for are as follows: ' + '\n' + str(holiday_list)[1:-1])
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def holiday_press(self):
        self.holidays = HolidayWindow()

    def openWindow(self):
        self.window = QMainWindow()
        self.ui = True

    def gridLayoutCreation(self):

        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()

        # Labels
        labels = ['Ticket Start [mm-dd-yy]', 'Ticket End [mm-dd-yy]', 'Client', 'Severity', 'Statutory Holidays']
        self.labels = [QLabel(label) for label in labels]
        [label.setFont(QFont("OPEN SANS", 9)) for label in self.labels]
        [gridLayout.addWidget(self.labels[i], i, 0) for i in range(len(self.labels))]

        # Buttons
        calculate_button = QPushButton("Calculate")
        calculate_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.holiday_button = QPushButton("Holidays")
        self.holiday_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        for button in [self.holiday_button, calculate_button]:
            button.setStyleSheet('QPushButton { border-style: outset; border-width: 1px; border-radius: 3px; border-color: black; min-width: 10em; padding: 3px}'
                                 'QPushButton:hover { background-color: rgba(255, 255, 255, 175) }'
                                 'QPushButton:pressed {  background-color: rgba(255, 255, 255, 245) }')


        # DateTime
        currentdatetime = QDateTime.currentDateTime()
        start_date_edit = QDateTimeEdit()
        end_date_edit = QDateTimeEdit()
        start_date_edit.setDateTime(currentdatetime)
        end_date_edit.setDateTime(currentdatetime)

        # Combo boxes
        client_combo_box = QComboBox(self)
        sev_combo_box = QComboBox(self)

        # Populate client combobox
        with open('data.json') as f:
            data = json.load(f)
            for client in data:
                client_combo_box.addItem(client)
            for key in data["AC"]['SEV'].keys():
                    sev_combo_box.addItem(key)
            prov = data[client_combo_box.currentText()]['prov']
            self.holiday_button.setEnabled(False)

        # Change sev combo box when client changes
        client_combo_box.currentIndexChanged.connect(lambda: self.repopulateCombo(sev_combo_box, client_combo_box))
        sev_combo_box.currentIndexChanged.connect(lambda: self.check_sev(sev_combo_box.currentText()))
        # Calculate on button press
        self.holiday_button.clicked.connect(lambda: self.holiday_press())
        calculate_button.clicked.connect(lambda: self.calculate_press(start_date_edit, end_date_edit, client_combo_box.currentText(), sev_combo_box.currentText(), prov))


        # Add to layout
        gridLayout.addWidget(start_date_edit, 0, 2)
        gridLayout.addWidget(end_date_edit, 1, 2)
        gridLayout.addWidget(client_combo_box,2, 2)
        gridLayout.addWidget(sev_combo_box,3, 2)
        gridLayout.addWidget(self.holiday_button, 4, 2)
        gridLayout.addWidget(calculate_button, 5, 2)

        self.groupBox.setLayout(gridLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Interface()
    sys.exit(app.exec_())
