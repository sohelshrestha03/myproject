import hashlib
import sys
import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 350, 370)
        self.setObjectName('main')

        l = QFormLayout()
        self.lbl = QLabel("User Login")
        self.lbl.setObjectName('user_login')
        self.lbl1 = QLabel("Username:")
        self.txt1 = QLineEdit(self)
        self.txt1.setPlaceholderText("Enter Username")
        self.lbl2 = QLabel("Password:")
        self.txt2 = QLineEdit(self)
        self.txt2.setPlaceholderText("Enter Password")
        self.txt2.setEchoMode(QLineEdit.Password)
        self.btn = QPushButton("Login")
        self.btn.clicked.connect(self.login_account)
        self.forgot_lbl = QLabel('<a href="forgotpwd.py" style="text-decoration:none;">Forget Password...</a>')
        self.forgot_lbl.setOpenExternalLinks(False)
        self.forgot_lbl.linkActivated.connect(self.open_forget)
        self.forgot_lbl.setObjectName('myforget')
        self.acclbl = QLabel("Don't have account.")
        self.acclbl.setObjectName('golbl')
        self.lblreg = QLabel("<a href='register.py' style='text-decoration:none;'>Register</a>")
        self.lblreg.setOpenExternalLinks(False)
        self.lblreg.linkActivated.connect(self.open_register)
        self.lblreg.setObjectName('golink')

        self.lbl.setAlignment(Qt.AlignHCenter)
        self.lbl1.setAlignment(Qt.AlignHCenter)
        self.lbl2.setAlignment(Qt.AlignHCenter)
        self.txt1.setAlignment(Qt.AlignHCenter)
        self.txt2.setAlignment(Qt.AlignHCenter)
        self.forgot_lbl.setAlignment(Qt.AlignHCenter)

        l.addRow(self.lbl)
        l.addRow(self.lbl1)
        l.addRow(self.txt1)
        l.addRow(self.lbl2)
        l.addRow(self.txt2)
        l.addRow(self.btn)
        l.addRow(self.forgot_lbl)
        l.addRow(self.acclbl, self.lblreg)

        self.setStyleSheet('''
        QWidget#main{
        background-color:#bbc1cd;
        }

        QLabel#user_login{
        font-size:22px;
        font-weight:bold;
        font-family:Times new roman;
        margin-top:10px;
        margin-bottom:10px;
        }

        QLabel{
        font-size:14px;
        font-family:Times new roman;
        margin-top:7px;
        margin-bottom:10px;
        font-weight:bold;
        }

        QLineEdit{
        font-size:14px;
        font-family:Times new roman;
        }

        QPushButton{
        font-size:14px;
        font-family:Times new roman;
        background-color:#261e95;
        border-radius:3px;
        padding:7px;
        }

        QPushButton:hover{
        background-color:#3529d7;
        color:white;
        font-weight:bold;
        }


        ''')

        self.setLayout(l)

    def login_account(self):
        uname = self.txt1.text().strip()
        pwd = self.txt2.text().strip()

        if not uname or not pwd:
            QMessageBox.warning(self, "Empty", "Please enter both username and password.")
            return

        hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()

        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('SELECT id FROM user WHERE username=? and confirm_password=?', (uname, hash_pwd))
        own = cur.fetchone()
        conn.close()
        if own:
            u_id=own[0]
            from app import Inventory
            self.my_app = Inventory(uname,u_id)
            self.my_app.show()
            self.close()

        else:
            QMessageBox.critical(self, "Invalid", "Invalid username and password.")

    def open_register(self):
        from register import RegisterPage
        self.reg = RegisterPage()
        self.reg.show()
        self.close()

    def open_forget(self):
        from forgotpwd import ForgotPassword
        self.fp = ForgotPassword()
        self.fp.show()
        self.close()


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = Login()
    w.show()
    sys.exit(a.exec_())