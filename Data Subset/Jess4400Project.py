#CS 4400
# Team 2

import pymysql
import sys
from collections import namedtuple
from datetime import (datetime,date,time)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QLabel,
    qApp,
    QAction,
    QSplitter,
    QListView,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QTextEdit,
    QListWidget,
    QGridLayout,
    QListWidgetItem
)
connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = '',
                                db = 'trip_planner',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
cursor = connection.cursor()

def addAttraction(name,address,desc,dayOfWeek,openingTime,closingTime,reservedAttraction,price):
    if reservedAttraction == 'Y':
        reservedAttraction = 1
    elif reservedAttraction == 'N':
        reservedAttraction = 0
    price = int(price)
    openingTime = datetime.strptime(openingTime,'%H:%M').time()
    closingTime = datetime.strptime(closingTime,'%H:%M').time()
    sql = "INSERT INTO attraction (name,address,description,dayOfWeek,openingTime,closingTime,reservedAttraction,price) values ('{}','{}','{}','{}','{}','{}',{},{});".format(name,address,desc,dayOfWeek,openingTime,closingTime,reservedAttraction,price)
    cursor.execute(sql)

def updateAttraction(name,address, postal_code,city,country,desc,dayOfWeek,openingTime,closingTime,reservedAttraction,price):
    if reservedAttraction == 'Y':
        reservedAttraction = 1
    elif reservedAttraction == 'N':
        reservedAttraction = 0
    openingTime = datetime.strptime(openingTime,'%H:%M').time()
    closingTime = datetime.strptime(closingTime,'%H:%M').time()
    price = int(price)
    addresstotal = "{}, {}, {}, {}".format(address,postal_code,city,country)
    sql = "UPDATE attraction SET description = '{}', dayOfWeek = '{}', openingTime = '{}', closingTime = '{}', reservedAttraction = {}, price = {} where name = '{}' and address = '{}';".format(desc,dayOfWeek,openingTime,closingTime,reservedAttraction,price,name,addresstotal)
    cursor.execute(sql)

def suspendUser(email):
    try:
        sql = 'UPDATE user SET suspended = b"/x01" where email = "{}";'.format(email)
        cursor.execute(sql)
    except:
        error_window.exec()

def deleteUser(email):
    try:
        sql = 'DELETE from user where email ="{}";'.format(email)
        cursor.execute(sql)
    except:
        error_window.exec()

def addUser(firstname,lastname,email,password,address_number,address_street,address_city,address_state,address_zip,address_country,ccNumber,expiry,cvv):
        address_number = address_street.split(" ")[0]
        address_street = address_street.split(' ')[1]
        name = "{} {}".format(firstname,lastname)
        usersql = "INSERT INTO user values (0,'{}','{}','{}',0,'{}','{}','{}','{}','{}','{}');".format(name,email,password,address_number,address_street,address_city,address_state,address_zip,address_country)
        addresstotal = '{} {} {} {} {} {}'.format(address_number,address_street,address_city,address_state,address_zip,address_country)
        ccsql = " INSERT INTO creditCard values ('{}','{}','{}','{}');".format(ccNumber,addresstotal,expiry,cvv)
        cursor.execute(usersql)
        cursor.execute(ccsql)
        print("User and CC Info Added")

def editUser(firstname,lastname,email,password,address_number,address_street,address_city,address_state,address_zip,address_country,ccNumber,expiry,cvv):
        address_number = address_street.split(" ")[0]
        address_street = address_street.split(' ')[1]
        name = "{} {}".format(firstname,lastname)
        addresstotal = '{} {} {} {} {} {}'.format(address_number,address_street,address_city,address_state,address_zip,address_country)
        usersql = "UPDATE user set name = '{}', password = '{}', address_number = '{}', address_street = '{}', address_city = '{}', address_state = '{}', address_zip = '{}', address_country = '{}' WHERE email = '{}';".format(name,password,address_number,address_street,address_city,address_state,address_zip,address_country,email)
        cursor.execute(usersql)


class DbNewAttraction(QDialog):
    def __init__(self):
        super(DbNewAttraction, self).__init__()
        self.setModal(True)
        self.setWindowTitle("New Attraction")

        self.name = QLineEdit()
        self.description = QLineEdit()
        self.address = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()
        self.postal_code = QLineEdit()
        self.daysOpen = ['M','T','W','R','F','S','U']
        self.dayOpen = QComboBox(self)
        self.dayOpen.addItems(self.daysOpen)
        self.openhours = ['0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','24:00']
        self.openhour = QComboBox(self)
        self.openhour.addItems(self.openhours)
        self.closehour = QComboBox(self)
        self.closehour.addItems(self.openhours)
        self.options = ['Y','N']
        self.reservation = QComboBox(self)
        self.reservation.addItems(self.options)
        self.transport = QLineEdit()
        self.price = QLineEdit()

        form_group_box = QGroupBox("New Attraction")
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name)
        layout.addRow(QLabel("Description"), self.description)
        layout.addRow(QLabel("Address"), self.address)
        layout.addRow(QLabel("City"), self.city)
        layout.addRow(QLabel("Country"), self.country)
        layout.addRow(QLabel("Postal Code"), self.postal_code)
        layout.addRow(QLabel("Day Open"), self.dayOpen)
        layout.addRow(QLabel("Opening Time"), self.openhour)
        layout.addRow(QLabel('Closing Time'), self.closehour)
        layout.addRow(QLabel("Nearest Public Trasport"), self.transport)
        layout.addRow(QLabel("Price"), self.price)
        layout.addRow(QLabel('Reservation Compulsory'),self.reservation)
        form_group_box.setLayout(layout)
        commit_button = QPushButton("Commit")
        layout.addWidget(commit_button)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        commit_button.clicked.connect(lambda: addAttraction(self.name.text(),self.address.text(),self.description.text(),self.dayOpen.currentText(),self.openhour.currentText(),self.closehour.currentText(),self.reservation.currentText(),self.price.text()))

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)


class DbEditAttraction(QDialog):
    def __init__(self):
        super(DbEditAttraction, self).__init__()
        self.setModal(True)
        self.setWindowTitle("New Attraction")

        self.name = QLineEdit()
        self.description = QLineEdit()
        self.address = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()
        self.postal_code = QLineEdit()
        self.daysOpen = ['M','T','W','R','F','S','U']
        self.dayOpen = QComboBox(self)
        self.dayOpen.addItems(self.daysOpen)
        self.openhours = ['0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','24:00']
        self.openhour = QComboBox(self)
        self.openhour.addItems(self.openhours)
        self.closehour = QComboBox(self)
        self.closehour.addItems(self.openhours)
        self.options = ['Y','N']
        self.reservation = QComboBox(self)
        self.reservation.addItems(self.options)
        self.transport = QLineEdit()
        self.price = QLineEdit()

        form_group_box = QGroupBox("New Attraction")
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name)
        layout.addRow(QLabel("Description"), self.description)
        layout.addRow(QLabel("Address"), self.address)
        layout.addRow(QLabel("City"), self.city)
        layout.addRow(QLabel("Country"), self.country)
        layout.addRow(QLabel("Postal Code"), self.postal_code)
        layout.addRow(QLabel("Day Open"), self.dayOpen)
        layout.addRow(QLabel("Opening Time"), self.openhour)
        layout.addRow(QLabel('Closing Time'), self.closehour)
        layout.addRow(QLabel("Nearest Public Trasport"), self.transport)
        layout.addRow(QLabel("Price"), self.price)
        layout.addRow(QLabel('Reservation Compulsory'),self.reservation)
        form_group_box.setLayout(layout)
        commit_button = QPushButton('Commit')
        commit_button.clicked.connect(lambda: updateAttraction(self.name.text(),self.address.text(), self.postal_code.text(), self.city.text(),self.country.text(),self.description.text(),self.dayOpen.currentText(),self.openhour.currentText(),self.closehour.currentText(),self.reservation.currentText(),self.price.text()))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox_layout = QVBoxLayout()
        layout.addWidget(commit_button)
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)









class DbEditUser(QDialog):
    def __init__(self):
        super(DbEditUser, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Edit User")

        # left side
        self.email = QLineEdit()
        self.confirm_email = QLineEdit()
        self.password = QLineEdit()
        self.confirm_password = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.address1 = QLineEdit()
        self.address2 = QLineEdit()
        self.city = QLineEdit()
        self.state = QLineEdit()
        self.postal_code = QLineEdit()
        self.countries = ['US','FR']
        self.country = QComboBox(self)
        self.country.addItems(self.countries)

        # right side
        self.credit_card = QLineEdit()
        self.cvv = QLineEdit()

        self.months1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.month1 = QComboBox(self)
        self.month1.addItems(self.months1)
        self.years1 = ['2020','2021','2022','2023','2024']
        self.year1 = QComboBox(self)
        self.year1.addItems(self.years1)

        # self.birthdates = ['Select a Birthdate','01/01/98','02/02/98','03/03/98','04/04/98','05/05/98']
        # self.birthdate = QComboBox(self)
        # self.birthdate.addItems(self.birthdates)

        self.months2 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.month2 = QComboBox(self)
        self.month2.addItems(self.months2)
        self.days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.day = QComboBox(self)
        self.day.addItems(self.days)
        self.years2 = ['1995','1996','1997','1998','1999']
        self.year2 = QComboBox(self)
        self.year2.addItems(self.years2)
        self.expirystr = '{}-{}-01'.format(self.year1.currentText(),self.month1.currentText())
        self.expiry = datetime.strptime(self.expirystr, '%Y-%m-01')

        create_button = QPushButton("Edit User")


        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("*Email:"), self.email)
        layout.addRow(QLabel("*Confirm Email"), self.confirm_email)
        layout.addRow(QLabel("*Password:"), self.password)
        layout.addRow(QLabel("*Confirm Password:"), self.confirm_password)
        layout.addRow(QLabel("*First Name"), self.first_name)
        layout.addRow(QLabel("*Last Name"), self.last_name)
        layout.addRow(QLabel("*Address 1"), self.address1)
        layout.addRow(QLabel("Address 2"), self.address2)
        layout.addRow(QLabel("*City"), self.city)
        layout.addRow(QLabel("*State"), self.state)
        layout.addRow(QLabel("*Postal Code"), self.postal_code)
        layout.addRow(QLabel("*Country"), self.country)
        layout.addRow(QLabel("*Credit Card #"), self.credit_card)
        layout.addRow(QLabel("*CC Expiry"), self.month1)
        layout.addRow(QLabel(" "), self.year1)
        layout.addRow(QLabel("CVV"),self.cvv)
        layout.addRow(QLabel("*Birthdate"), self.month2)
        layout.addRow(QLabel(" "), self.day)
        layout.addRow(QLabel(" "), self.year2)
        layout.addWidget(create_button)
        form_group_box.setLayout(layout)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog

        create_button.clicked.connect(lambda: editUser(self.first_name.text(),self.last_name.text(), self.email.text(),self.password.text(),0,self.address1.text(),self.city.text(),self.state.text(),self.postal_code.text(),self.country.currentText(),self.credit_card.text(),self.expiry,self.cvv.text()))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
        self.password.setFocus()









class DbRegistration(QDialog):
    def __init__(self):
        super(DbRegistration, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Registration")

        # left side
        self.email = QLineEdit()
        self.confirm_email = QLineEdit()
        self.password = QLineEdit()
        self.confirm_password = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.address1 = QLineEdit()
        self.address2 = QLineEdit()
        self.city = QLineEdit()
        self.state = QLineEdit()
        self.postal_code = QLineEdit()
        self.countries = ['US','FR']
        self.country = QComboBox(self)
        self.country.addItems(self.countries)

        # right side
        self.credit_card = QLineEdit()
        self.cvv = QLineEdit()

        self.months1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.month1 = QComboBox(self)
        self.month1.addItems(self.months1)
        self.years1 = ['2020','2021','2022','2023','2024']
        self.year1 = QComboBox(self)
        self.year1.addItems(self.years1)

        # self.birthdates = ['Select a Birthdate','01/01/98','02/02/98','03/03/98','04/04/98','05/05/98']
        # self.birthdate = QComboBox(self)
        # self.birthdate.addItems(self.birthdates)

        self.months2 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.month2 = QComboBox(self)
        self.month2.addItems(self.months2)
        self.days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.day = QComboBox(self)
        self.day.addItems(self.days)
        self.years2 = ['1995','1996','1997','1998','1999']
        self.year2 = QComboBox(self)
        self.year2.addItems(self.years2)
        self.expirystr = '{}-{}-01'.format(self.year1.currentText(),self.month1.currentText())
        self.expiry = datetime.strptime(self.expirystr, '%Y-%m-01')

        create_button = QPushButton("Create User")


        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("*Email:"), self.email)
        layout.addRow(QLabel("*Confirm Email"), self.confirm_email)
        layout.addRow(QLabel("*Password:"), self.password)
        layout.addRow(QLabel("*Confirm Password:"), self.confirm_password)
        layout.addRow(QLabel("*First Name"), self.first_name)
        layout.addRow(QLabel("*Last Name"), self.last_name)
        layout.addRow(QLabel("*Address 1"), self.address1)
        layout.addRow(QLabel("Address 2"), self.address2)
        layout.addRow(QLabel("*City"), self.city)
        layout.addRow(QLabel("*State"), self.state)
        layout.addRow(QLabel("*Postal Code"), self.postal_code)
        layout.addRow(QLabel("*Country"), self.country)
        layout.addRow(QLabel("*Credit Card #"), self.credit_card)
        layout.addRow(QLabel("*CC Expiry"), self.month1)
        layout.addRow(QLabel(" "), self.year1)
        layout.addRow(QLabel("CVV"),self.cvv)
        layout.addRow(QLabel("*Birthdate"), self.month2)
        layout.addRow(QLabel(" "), self.day)
        layout.addRow(QLabel(" "), self.year2)
        layout.addWidget(create_button)
        form_group_box.setLayout(layout)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog

        create_button.clicked.connect(lambda: addUser(self.first_name.text(),self.last_name.text(), self.email.text(),self.password.text(),0,self.address1.text(),self.city.text(),self.state.text(),self.postal_code.text(),self.country.currentText(),self.credit_card.text(),self.expiry,self.cvv.text()))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
        self.password.setFocus()


class DbReportsDialog(QDialog):        # we workin here
    def __init__(self):
        super(DbReportsDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Attraction Reports")

        # this gets a list of the attractions
        cursor = connection.cursor()
        cursor.execute('select name from attraction')
        self.attractions = cursor.fetchall()
        i = 0
        attractionList = [];
        while i < len(self.attractions):
            temp = self.attractions[i].values()
            temp2 = list(temp)[0]
            attractionList.append(temp2)
            i += 1


        # Create and fill the combo box to choose the attraction
        self.attractionComboBox = QComboBox(self) # This is the pulldown object
        self.attractionComboBox.addItems(attractionList)

        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

        self.monthsComboBox = QComboBox(self)
        self.monthsComboBox.addItems(months)
        self.daysComboBox = QComboBox(self)
        self.daysComboBox.addItems(days)
        self.yearsComboBox = QComboBox(self)
        self.yearsComboBox.addItems(years)

        # self.connect(self.ui.attractionComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), self.updateBaudRate)

        # def updateBaudRate(self, rate):
        #    ser.baudRate(str(rate)) # again convert to string as it my not accept a QString

        self.timeslots = QTextEdit()
        self.timeslots.setReadOnly(True)

        self.timeslotsTable = QTableWidget()
        self.timeslotsTable.setColumnCount(2)
        self.timeslotsTable.setHorizontalHeaderLabels(['Start Times', 'End Times'])
        self.timeslotsTable.setEditTriggers(QTableWidget.NoEditTriggers) # Makes so the user cant edit
        self.timeslotsTable.setRowCount(10)

        self.rosterList = QListWidget()
        self.roster = QTextEdit()
        self.roster.setReadOnly(True)

        search_but = QPushButton('Search')
        def find_time_slots():
            name = self.attractionComboBox.currentText()
            dt = date(int(self.yearsComboBox.currentText()),
                int(self.monthsComboBox.currentIndex() + 1),
                int(self.daysComboBox.currentIndex() + 1))
            cursor.execute('''
               SELECT DISTINCT startDateTime, endDateTime FROM timeSlot where name = "{}" and startDate = "{}";
            '''.format(name,str(dt)))
            # TimeSlot is a temporary class to hold the Time Slots
            TimeSlot = namedtuple('TimeSlot',['start','end'])
            self.timeslots = [TimeSlot(start = value['startDateTime'],end = value['endDateTime']) for value in cursor.fetchall()]
            if len(self.timeslots) >= 1:
                self.timeslotsTable.setRowCount(len(self.timeslots))
                for i, slot in enumerate(self.timeslots):
                    self.timeslotsTable.setItem(i,0,QTableWidgetItem(str(slot.start)))
                    self.timeslotsTable.setItem(i,1,QTableWidgetItem(str(slot.end)))
                    self.timeslotsTable.resizeColumnsToContents()
            else:
                pass
                # add in message box saying nothing found
        def find_roster():
            current_row = self.timeslotsTable.currentRow()
            self.rosterList.clear()
            cursor.execute('''
                SELECT DISTINCT email FROM timeSlot WHERE startDateTime = '{}' and endDateTime = '{}'
                '''.format(self.timeslots[current_row].start,self.timeslots[current_row].end))
            self.user_items = [] # container for the users as qlist objects
            for i, value in enumerate(cursor.fetchall()):
                #creates a user list item and appends it to teh self.user_itmes list
                self.user_items.append(QListWidgetItem(value['email']))
                # this lline adds the item to the roster list
                self.rosterList.addItem(QListWidgetItem(self.user_items[i]))
        search_but.clicked.connect(find_time_slots)
        self.timeslotsTable.clicked.connect(find_roster)

        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel('Attractions:'), self.attractionComboBox)
        layout.addRow(QLabel('Month:'), self.monthsComboBox)
        layout.addRow(QLabel('Day:'), self.daysComboBox)
        layout.addRow(QLabel('Year:'), self.yearsComboBox)
        layout.addRow(search_but)
        layout.addRow(QLabel("Timeslots"), self.timeslotsTable)
        layout.addRow(QLabel("Roster"), self.rosterList)


        form_group_box.setLayout(layout)

        dismiss_button = QPushButton('Dismiss')  # This button will send you back to the admin dash
        def close():
            pass
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(dismiss_button)
        dismiss_button.clicked.connect(self.reject)
        self.setLayout(vbox_layout)
        self.roster.setFocus()

class DbAdminDash(QDialog):
    def __init__(self):
        super(DbAdminDash, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Admin Dashboard")

        cursor = connection.cursor()
        cursor.execute('select name from attraction')
        self.attractions = cursor.fetchall()
        i = 0
        attractionList = [];
        attractLength = len(self.attractions)
        while i < attractLength:
            temp = self.attractions[i].values()
            temp2 = list(temp)[0]
            attractionList.append(temp2)
            i += 1
        self.attractionComboBox = QComboBox(self) # This is the pulldown object
        self.attractionComboBox.addItems(attractionList)

        cursor = connection.cursor()
        cursor.execute('select email from user')
        self.users = cursor.fetchall()
        i = 0
        userList = [];
        userLength = len(self.users)
        while i < userLength:
            temp = self.users[i].values()
            temp2 = list(temp)[0]
            userList.append(temp2)
            i += 1
        self.userComboBox = QComboBox(self) # This is the pulldown object
        self.userComboBox.addItems(userList)



        # self.users = ['Select a User', 'User1', 'User2', 'User3']
        # self.user = QComboBox(self)
        # self.user.addItems(self.users)

        form_group_box = QGroupBox("")
        layout = QFormLayout()

        layout.addRow(QLabel("Attraction"), self.attractionComboBox)
        layout.addRow(QLabel("User"), self.userComboBox)

        form_group_box.setLayout(layout)

        btn1 = QPushButton('New')
        btn2 = QPushButton('Edit')
        btn3 = QPushButton('Reports')
        btn4 = QPushButton('New')
        btn5 = QPushButton('Delete')
        btn6 = QPushButton('Suspend')

        btn1.clicked.connect(lambda: new_attraction.exec())
        btn2.clicked.connect(lambda: edit_attraction.exec())
        btn3.clicked.connect(lambda: reports.exec())
        btn4.clicked.connect(lambda: register.exec())
        btn5.clicked.connect(lambda: deleteUser(self.userComboBox.currentText()))
        btn6.clicked.connect(lambda: suspendUser(self.userComboBox.currentText()))


        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()

        vbox_layout.addWidget(btn1)
        vbox_layout.addWidget(btn2)
        vbox_layout.addWidget(btn3)
        vbox_layout.addWidget(btn4)
        vbox_layout.addWidget(btn5)
        vbox_layout.addWidget(btn6)


        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
class DbCustomerDash(QDialog):

    def __init__(self):
        super(DbCustomerDash, self).__init__()
        self.setWindowTitle('Customer Dashboard')
        cursor = connection.cursor()

        #grab user info from db
        self.user = "Marty McFly"
        cursor.execute("select * from user where name = '{}'".format(self.user))
        result = cursor.fetchall()
        result = result[0].values()
        self.email_label = QLabel('Email: ')
        self.email = QLabel(list(result)[2])
        self.email_str = list(result)[2]
        name = list(result)[1]
        self.lastName_label = QLabel('Last Name: ')
        self.lastName = QLabel(name.split(' ')[1])
        self.firstName_label = QLabel('First Name: ')
        self.firstName = QLabel(name.split(' ')[0])
        self.address1_label = QLabel('Address 1: ')
        self.address1 = QLabel('{} {}'.format(list(result)[5],list(result)[6]))
        self.address2_label = QLabel('Address 2: ')
        self.address2 = QLabel('')
        self.city_label = QLabel('City: ')
        self.city = QLabel(list(result)[7])
        self.state_label = QLabel('State: ')
        self.state = QLabel(list(result)[8])
        self.postalCode_label = QLabel('Postal Code: ')
        self.postalCode = QLabel(list(result)[9])
        self.country_label = QLabel('Country: ')
        self.country = QLabel(list(result)[10])
        self.space = QLabel('              ')

        #grab cc info from db
        cursor.execute("select * from owns join creditCard using (ccNumber) where email = '{}'".format(self.email_str))
        result = cursor.fetchall()
        result = result[0].values()
        self.creditCard_label = QLabel('Credit Card: ')
        self.creditCard = QLabel(list(result)[0])
        self.expriry_label = QLabel('Expiry: ')
        self.expriry = QLabel(list(result)[3].strftime('%Y-%m-%d'))

        #buttons and stuff
        self.profile_label = QLabel('Profile')
        self.trip_label = QLabel('Trips: ')
        self.edit_btn = QPushButton('Edit Profile')
        self.edit_btn.clicked.connect(lambda: edit_user.exec())
        self.new_trip_btn = QPushButton('New Trip')
        self.new_trip_btn.clicked.connect(lambda: reviews.exec())

        #table
        self.table = QTableWidget()
        self.table.setEditTriggers( QTableWidget.NoEditTriggers )
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Begin Date','End Date','City','Country','Edit'])


        #trip data
        cursor.execute("select * from trip where email = '{}'".format(self.email_str))
        result = cursor.fetchall()
        self.x = len(result)
        self.table.setRowCount(self.x)
        self.btns = [0]*self.x
        for i in range (self.x):
            self.btns[i] = QPushButton('edit')
            self.table.setCellWidget(i,4,self.btns[i])
            self.btns[i].clicked.connect(lambda ignore, i=i: reviews.exec())

            #fill in trips
            result_temp = result[i].values()
            self.table.setItem(i,0,QTableWidgetItem(list(result_temp)[1].strftime('%Y-%m-%d')))
            self.table.setItem(i,1,QTableWidgetItem(list(result_temp)[1].strftime('%Y-%m-%d')))
            self.table.setItem(i,2,QTableWidgetItem(list(result_temp)[0]))
            self.table.setItem(i,3,QTableWidgetItem('France'))

        def refresh():
            cursor.execute("select * from trip where email = '{}'".format(self.email_str))
            result = cursor.fetchall()
            self.x = len(result)
            self.table.setRowCount(self.x)
            self.btns = [0]*self.x
            for i in range (self.x):
                self.btns[i] = QPushButton('edit')
                self.table.setCellWidget(i,4,self.btns[i])
                self.btns[i].clicked.connect(lambda ignore, i=i: reviews.exec())

                #fill in trips
                result_temp = result[i].values()
                self.table.setItem(i,0,QTableWidgetItem(list(result_temp)[1].strftime('%Y-%m-%d')))
                self.table.setItem(i,1,QTableWidgetItem(list(result_temp)[1].strftime('%Y-%m-%d')))
                self.table.setItem(i,2,QTableWidgetItem(list(result_temp)[0]))
                self.table.setItem(i,3,QTableWidgetItem('France'))

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(refresh)

        #formatting
        self.horizontalGroupBox = QGroupBox("Grid")
        self.layout = QGridLayout()
        self.layout.addWidget(self.profile_label,0,0)
        self.layout.addWidget(self.edit_btn,0,1)
        self.layout.addWidget(self.email_label,1,0)
        self.layout.addWidget(self.email,1,1)
        self.layout.addWidget(self.address1_label,1,2)
        self.layout.addWidget(self.address1,1,3)
        self.layout.addWidget(self.lastName_label,2,0)
        self.layout.addWidget(self.lastName,2,1)
        self.layout.addWidget(self.address2_label,2,2)
        self.layout.addWidget(self.address2,2,3)
        self.layout.addWidget(self.firstName_label,3,0)
        self.layout.addWidget(self.firstName,3,1)
        self.layout.addWidget(self.city_label,3,2)
        self.layout.addWidget(self.city,3,3)
        self.layout.addWidget(self.state_label,4,2)
        self.layout.addWidget(self.state,4,3)
        self.layout.addWidget(self.creditCard_label,4,0)
        self.layout.addWidget(self.creditCard,4,1)
        self.layout.addWidget(self.postalCode_label,5,2)
        self.layout.addWidget(self.postalCode,5,3)
        self.layout.addWidget(self.expriry_label,5,0)
        self.layout.addWidget(self.expriry,5,1)
        self.layout.addWidget(self.country_label,6,2)
        self.layout.addWidget(self.country,6,3)
        self.layout.addWidget(self.space,0,4)
        self.layout.addWidget(self.table,7,0,7,6)
        self.layout.addWidget(self.new_trip_btn,16,0)
        self.layout.addWidget(self.refresh_btn,6,0)

        self.setLayout(self.layout)


class DbReviewsDialog(QDialog):
    def __init__(self):
        super(DbReviewsDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Review Attraction")

        # this is a list of the attractions
        self.cities = ['Select a City',
                            'Paris',
                            'Metz',
                            'Nice']
        self.stars = ['How many Stars?',
                        '5 Stars',
                        '4 Stars',
                        '3 Stars',
                        '2 Stars',
                        '1 Star']

        # Create and fill the combo box to choose the attraction
        self.citiesComboBox = QComboBox(self) # This is the pulldown object
        self.citiesComboBox.addItems(self.cities)
        self.attractionList = QListWidget()

        self.starsComboBox = QComboBox(self)
        self.starsComboBox.addItems(self.stars)

        self.reviewBody = QTextEdit()

        form_group_box = QGroupBox()
        layout = QFormLayout()

        layout.addRow(QLabel('Cities:'), self.citiesComboBox)
        layout.addRow(QLabel('Attraction List:'), self.attractionList)
        layout.addRow(QLabel("Stars"), self.starsComboBox)
        layout.addRow(QLabel("Type your review here"), self.reviewBody)


        form_group_box.setLayout(layout)

        cancel_button = QPushButton('Cancel')  # This button will send you back to the admin dash
        ok_button = QPushButton('OK')

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(ok_button)
        vbox_layout.addWidget(cancel_button)
        self.setLayout(vbox_layout)
        self.reviewBody.setFocus()


class DbEditTrip(QDialog):
    def __init__(self):
        super(DbEditTrip, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Edit Trip")

        cursor = connection.cursor()
        cursor.execute('select name from attraction')
        self.attractions = cursor.fetchall()
        i = 0
        attractionList = [];
        attractLength = len(self.attractions)
        while i < attractLength:
            temp = self.attractions[i].values()
            temp2 = list(temp)[0]
            attractionList.append(temp2)
            i += 1
        self.attractionComboBox = QComboBox(self) # This is the pulldown object
        self.attractionComboBox.addItems(attractionList)

        self.cities = ['Select a City','Paris','Metz','Nice']

        # self.dates
        self.months = ['Month','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        self.days = ['Day','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.years = ['Year','2018','2019','2020']


        self.city = QComboBox(self)
        self.city.addItems(self.cities)

        self.month = QComboBox(self)
        self.month.addItems(self.months)
        self.day = QComboBox(self)
        self.day.addItems(self.days)
        self.year = QComboBox(self)
        self.year.addItems(self.years)


        self.timeslots = QTextEdit()
        self.timeslots.setReadOnly(True)

        self.timeslotsTable = QTableWidget()
        self.timeslotsTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.timeslotsTable.setColumnCount(2)
        self.timeslotsTable.setHorizontalHeaderLabels(['Begin Time','End Time'])
        self.timeslotsTable.setEditTriggers(QTableWidget.NoEditTriggers) # Makes so the user cant edit
        self.timeslotsTable.setRowCount(10)


        self.trip = QTextEdit()
        self.trip.setReadOnly(True)

        self.tripTable = QTableWidget()

        self.tripTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tripTable.setColumnCount(4)
        self.tripTable.setHorizontalHeaderLabels(['Date','Attraction','Start','End'])
        self.tripTable.setEditTriggers(QTableWidget.NoEditTriggers) # Makes so the user cant edit
        self.tripTable.setRowCount(10)
        self.tripTable.resizeColumnsToContents()

        self.rosterList = QListWidget()
        self.roster = QTextEdit()
        self.roster.setReadOnly(True)

        view_info_button = QPushButton('View Info')
        def find_time_slots():
            name = self.attractionComboBox.currentText()
            city = self.city.currentText()
            dt = date(int(self.year.currentText()),
                int(self.month.currentIndex()),
                int(self.day.currentIndex()))
            cursor.execute('''
               SELECT DISTINCT startDateTime, endDateTime FROM timeSlot where name = "{}" and startDate = "{}";
            '''.format(name,str(dt)))
            print('''
               SELECT DISTINCT startDateTime, endDateTime FROM timeSlot where name = "{}" and startDate = "{}";
            '''.format(name,str(dt)))
            TimeSlot = namedtuple('TimeSlot',['start','end'])
            self.timeslots = [TimeSlot(start = value['startDateTime'],end = value['endDateTime']) for value in cursor.fetchall()]
            if len(self.timeslots) >= 1:
                self.timeslotsTable.setRowCount(len(self.timeslots))
                for i, slot in enumerate(self.timeslots):
                    self.timeslotsTable.setItem(i,0,QTableWidgetItem(str(slot.start)))
                    self.timeslotsTable.setItem(i,1,QTableWidgetItem(str(slot.end)))
                    self.timeslotsTable.resizeColumnsToContents()
            else:
                pass


        add_to_trip_button = QPushButton('Add to Trip')
        def find_trip():
            name = self.attractionComboBox.currentText()
            current_row = self.timeslotsTable.currentRow()
            dt = date(int(self.year.currentText()),
                int(self.month.currentIndex()),
                int(self.day.currentIndex()))
            self.rosterList.clear()
            Trip = namedtuple('Trip',['date','attraction','start','end'])
            self.trips = ['none']*4
            cursor.execute('''
                SELECT DISTINCT startDate FROM timeSlot where startDateTime = '{}' and endDateTime = '{}';
            '''.format(self.timeslots[current_row].start,self.timeslots[current_row].end))
            self.trips[0] = cursor.fetchall()
            cursor.execute('''
                SELECT DISTINCT name FROM timeSlot where name = '{}';
            '''.format(name))
            self.trips[1] = cursor.fetchall()
            cursor.execute('''
                SELECT DISTINCT startDateTime FROM timeSlot where startDateTime = '{}' and endDateTime = '{}';
            '''.format(self.timeslots[current_row].start,self.timeslots[current_row].end))
            self.trips[2] = cursor.fetchall()
            cursor.execute('''
                SELECT DISTINCT endDateTime FROM timeSlot where startDateTime = '{}' and endDateTime = '{}';
            '''.format(self.timeslots[current_row].start,self.timeslots[current_row].end))
            self.trips[3] = cursor.fetchall()
            if len(self.trips) >= 1:
                self.tripTable.setRowCount(len(self.trips))
                self.tripTable.setItem(0,0,QTableWidgetItem(str(list(self.trips[0][0].values())[0])))
                self.tripTable.setItem(0,1,QTableWidgetItem(list(self.trips[1][0].values())[0]))
                self.tripTable.setItem(0,2,QTableWidgetItem(str(list(self.trips[2][0].values())[0])))
                self.tripTable.setItem(0,3,QTableWidgetItem(str(list(self.trips[3][0].values())[0])))
                self.tripTable.resizeColumnsToContents()
            else:
                pass

        view_info_button.clicked.connect(find_time_slots)
        add_to_trip_button.clicked.connect(find_trip)


        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel('City:'), self.city)
        layout.addRow(QLabel('Date:'), self.month)
        layout.addRow(QLabel(" "), self.day)
        layout.addRow(QLabel(" "), self.year)
        layout.addRow(QLabel('Attractions:'), self.attractionComboBox)
        layout.addRow(view_info_button)
        layout.addRow(QLabel("Time Slots"), self.timeslotsTable)
        layout.addRow(add_to_trip_button)
        layout.addRow(QLabel("Trip"), self.tripTable)


        form_group_box.setLayout(layout)

        cancel_button = QPushButton('Cancel')  # This button will send you back to the admin dash
        def close():
            self.close()
        ok_button = QPushButton('OK')

        def add_trip():
            city = self.city.currentText()
            dt = date(int(self.year.currentText()),
                int(self.month.currentIndex()),
                int(self.day.currentIndex()))
            sql = "INSERT INTO trip (city,startDate,booked,email) values ('{}','{}',{},'{}');".format(city,dt,1,'notachicken123@gmail.com')
            print(sql)
            cursor.execute(sql)
            self.close()


        ok_button.clicked.connect(add_trip)
        cancel_button.clicked.connect(close)

        vbox_layout = QVBoxLayout()

        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(ok_button)
        vbox_layout.addWidget(cancel_button)
        self.setLayout(vbox_layout)
        self.trip.setFocus()




def userlogin(username,password):
    try:
        sql = "SELECT email from user where email = '{}' and password ='{}'".format(username,password)
        cursor.execute(sql)
        result1 = cursor.fetchall()
        result1 = result1[0].values()
        sql2 = "SELECT isAdmin from user where email= '{}'".format(username)
        cursor.execute(sql2)
        result = cursor.fetchall()
        result = result[0].values()

        sqlsus = "SELECT suspended from user where email = '{}' and password ='{}'".format(username,password)
        cursor.execute(sqlsus)
        resultsus = cursor.fetchall()
        resultsus = resultsus[0].values()

        if list(result)[0] == b'\x01':
            admindash.exec()
        elif list(result)[0] == b'\x00':
            custdash.exec()

        if list(resultsus)[0] == b'\x01':
            error_window.exec()

    except:
        error_window.exec()


class DbError(QDialog):
    def __init__(self):
        super(DbError, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Try Again")


        self.errorMessage = QLabel('Command Unsuccessful. Try Again')
        reg_button = QPushButton('Register')

        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("Error:"), self.errorMessage)
        form_group_box.setLayout(layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)

        vbox_layout.addWidget(buttons)

        self.setLayout(vbox_layout)


class DbLoginDialog(QDialog):
    def __init__(self):
        super(DbLoginDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Login")


        self.user = QLineEdit()
        self.password = QLineEdit()


        form_group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("User:"), self.user)
        layout.addRow(QLabel("Password:"), self.password)

        form_group_box.setLayout(layout)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog
        login_customer_button = QPushButton('Login')
        reg_button = QPushButton("Register")
        login_customer_button.clicked.connect(lambda: userlogin(self.user.text(),self.password.text()))
        reg_button.clicked.connect(lambda: register.exec())


        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(login_customer_button)
        vbox_layout.addWidget(reg_button)

        self.setLayout(vbox_layout)
        self.password.setFocus()






if __name__=='__main__':
    app = QApplication(sys.argv)
    error_window = DbError()
    edit_attraction = DbEditAttraction()
    custdash = DbCustomerDash()
    admindash = DbAdminDash()
    login = DbLoginDialog()
    register = DbRegistration()
    reports = DbReportsDialog()
    new_attraction = DbNewAttraction()
    reviews = DbEditTrip()
    edit_user = DbEditUser()
    # This is how you check which button the user used to dismiss the dialog.
    if login.exec() == QDialog.Accepted:
        # connection is global so we can use it in any class, function, or method
        # defined in this module

      main = MainWindow(login.db.text())
      main.show()
      sys.exit(app.exec_())

