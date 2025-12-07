import sys
import sqlite3
import re
import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.setObjectName('main')

    # setting UI Fuction
    def set_ui(self):
        self.setWindowTitle("Register")
        self.setGeometry(200, 200, 500, 520)

        # For form Layout
        f = QFormLayout()
        self.lbl = QLabel("Register Account")
        self.lbl.setObjectName("head")

        self.lbl1 = QLabel("First Name:")
        self.txt1 = QLineEdit(self)
        self.txt1.setPlaceholderText("Enter First Name")

        self.lbl2 = QLabel("Last Name:")
        self.txt2 = QLineEdit(self)
        self.txt2.setPlaceholderText("Enter Last Name")

        self.lbl3 = QLabel("User Name:")
        self.txt3 = QLineEdit(self)
        self.txt3.setPlaceholderText("Enter User Name")

        self.lbl4 = QLabel("Address:")
        self.txt4 = QLineEdit(self)
        self.txt4.setPlaceholderText("Enter Address")

        self.lbl5 = QLabel("Phone Number:")
        self.txt5 = QLineEdit(self)
        self.txt5.setPlaceholderText("Enter Phone Number")

        self.lbl6 = QLabel("Email:")
        self.txt6 = QLineEdit(self)
        self.txt6.setPlaceholderText("Enter Email")

        self.lbl7 = QLabel("New Password:")
        self.txt7 = QLineEdit(self)
        self.txt7.setPlaceholderText("Enter New Password")
        self.txt7.setEchoMode(QLineEdit.Password)

        self.lbl8 = QLabel("Confirm Password:")
        self.txt8 = QLineEdit(self)
        self.txt8.setPlaceholderText("Enter Confirm Password")
        self.txt8.setEchoMode(QLineEdit.Password)

        self.lbl9 = QLabel("Gender")
        h = QHBoxLayout()
        self.rb1 = QRadioButton("Male")
        self.rb1.setChecked(False)
        self.rb2 = QRadioButton("Female")
        self.rb2.setChecked(False)
        self.btn_grp = QButtonGroup()
        self.btn_grp.addButton(self.rb1)
        self.btn_grp.addButton(self.rb2)

        h.addWidget(self.rb1)
        h.addWidget(self.rb2)

        self.btn = QPushButton("Submit")
        self.btn.clicked.connect(self.validation)

        self.lblacc = QLabel("If you have account already.")
        self.lblacc.setObjectName("linklbl")
        self.loglbl = QLabel("<a href='login.py' style='text-decoration:none;'>Login</a>")
        self.loglbl.setOpenExternalLinks(False)
        self.loglbl.linkActivated.connect(self.open_login)
        self.loglbl.setObjectName("mylink")

        self.lbl.setAlignment(Qt.AlignHCenter)

        # Adding element in form
        f.addRow(self.lbl)
        f.addRow(self.lbl1, self.txt1)
        f.addRow(self.lbl2, self.txt2)
        f.addRow(self.lbl3, self.txt3)
        f.addRow(self.lbl4, self.txt4)
        f.addRow(self.lbl5, self.txt5)
        f.addRow(self.lbl6, self.txt6)
        f.addRow(self.lbl7, self.txt7)
        f.addRow(self.lbl8, self.txt8)
        f.addRow(self.lbl9, h)
        f.addRow(self.btn)
        f.addRow(self.lblacc, self.loglbl)

        # for stylesheet
        self.setStyleSheet('''
        QWidget#main{
        background-color:#cddddd;
        }

        QLabel#head{
        margin-top:10px;
        margin-bottom:10px;
        font-family:Times new roman;
        font-size:22px;
       }

        QLabel{
        margin-bottom:10px;
        font-size:14px;
        font-family:Times new roman;
        font-weight:bold;
        }

        QLineEdit{
        margin-bottom:10px;
        font-size:14px;
        font-family:Times new roman;
        }

        QRadioButton{
        margin-bottom:10px;
        font-size:14px;
        font-family:Times new roman;
        }

        QPushButton{
        margin-bottom:10px;
        font-size:14px;
        font-family:Times new roman;
        padding:7px;
        background-color:#29a2a6;
        border-radius:5px;
        }

        QPushButton:hover{
        background-color:#65d2d6;
        color:white;
        font-weight:bold;
        }

        QLabel#mylink{
        text-decoration:none;
        margin-top:10px;
        }

        QLabel#linklbl{
        margin-top:10px;
        }
        ''')

        # setting layout
        self.setLayout(f)
    #function for form validation
    def validation(self):
        fname = self.txt1.text().strip()
        lname = self.txt2.text().strip()
        uname = self.txt3.text().strip()
        add = self.txt4.text().strip()
        phone = self.txt5.text().strip()
        e = self.txt6.text().strip()
        np = self.txt7.text().strip()
        cp = self.txt8.text().strip()
        select_btn = self.btn_grp.checkedButton()

        # for hashing password
        hashed_np = hashlib.sha256(np.encode()).hexdigest()
        hashed_cp = hashlib.sha256(cp.encode()).hexdigest()

        if not fname:
            self.display_error("First name is empty.")
            return

        if not lname:
            self.display_error("Last name is empty.")
            return

        if not uname:
            self.display_error("User name is empty.")
            return

        if not add:
            self.display_error("Address is empty.")
            return

        if not phone:
            self.display_error("Phone is empty.")
            return

        if len(phone) != 10 or not phone.isdigit():
            self.display_error("Invalid number")
            return

        if not e:
            self.display_error("Email is empty.")
            return

        if not re.match(r'[^@]+@[^@]+\.[^@]+', e):
            self.display_error("Invalid email format.")
            return

        if np != cp:
            self.pwd_msg("Password didn't matched.")
            return

        if select_btn is None:
            self.display_error("Please select a gender.")
            return

        gen = select_btn.text()

        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()

        # For preventing from username and email which is already used
        cur.execute("SELECT * FROM user WHERE username=? and email=?", (uname, e))

        # For inserting data
        cur.execute('''INSERT INTO user(firstname,lastname,username,address,phone_no,email,new_password,confirm_password,gender)
                    VALUES (?,?,?,?,?,?,?,?,?)''', (fname, lname, uname, add, phone, e, hashed_np, hashed_cp, gen))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Account Created", "Your account has been created successfully.")
        self.clear_box()
    #Displaying error message
    def display_error(self, m):
        QMessageBox.critical(self, 'Empty', m)
    #Displaying this message when both new and confirm password is unmatched
    def pwd_msg(self, n):
        QMessageBox.critical(self, "Unmatched", n)
    #For clearing form after certain process is done
    def clear_box(self):
        self.txt1.clear()
        self.txt2.clear()
        self.txt3.clear()
        self.txt4.clear()
        self.txt5.clear()
        self.txt6.clear()
        self.txt7.clear()
        self.txt8.clear()

        for radio in [self.rb1, self.rb2]:
            radio.setAutoExclusive(False)
            radio.setChecked(False)
            radio.setAutoExclusive(True)
    #Open a login
    def open_login(self):
        from login import Login
        self.login = Login()
        self.login.show()
        self.close()


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = RegisterPage()
    w.show()
    sys.exit(a.exec_())