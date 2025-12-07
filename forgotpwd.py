import sys
import sqlite3
import hashlib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class ForgotPassword(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle("Forgot Password")
        self.setGeometry(200, 200, 350, 350)

        form_layout = QFormLayout()
        self.head = QLabel("Change Your Password")
        self.head.setObjectName('heading')
        self.username_lbl = QLabel("Username:")
        self.a = QLineEdit(self)
        self.a.setPlaceholderText("Enter Username")

        self.new = QLabel("New Password:")
        self.b = QLineEdit(self)
        self.b.setPlaceholderText("Enter New Password")
        self.b.setEchoMode(QLineEdit.Password)

        self.confirm = QLabel("Confirm Password:")
        self.c = QLineEdit(self)
        self.c.setPlaceholderText("Enter Confirm Password")
        self.c.setEchoMode(QLineEdit.Password)

        self.reset_btn = QPushButton("Reset Button")
        self.reset_btn.clicked.connect(self.reset_pwd)

        self.back_lbl = QLabel("<a href='app.py' style='text-decoration:none;'>Back</a>")
        self.back_lbl.setOpenExternalLinks(False)
        self.back_lbl.linkActivated.connect(self.open_log)
        self.back_lbl.setObjectName('back')

        form_layout.addRow(self.head)
        form_layout.addRow(self.username_lbl)
        form_layout.addRow(self.a)
        form_layout.addRow(self.new)
        form_layout.addRow(self.b)
        form_layout.addRow(self.confirm)
        form_layout.addRow(self.c)
        form_layout.addRow(self.reset_btn)
        form_layout.addRow(self.back_lbl)

        self.head.setAlignment(Qt.AlignHCenter)
        self.username_lbl.setAlignment(Qt.AlignHCenter)
        self.a.setAlignment(Qt.AlignHCenter)
        self.new.setAlignment(Qt.AlignHCenter)
        self.b.setAlignment(Qt.AlignHCenter)
        self.confirm.setAlignment(Qt.AlignHCenter)
        self.c.setAlignment(Qt.AlignHCenter)
        self.back_lbl.setAlignment(Qt.AlignHCenter)

        self.setStyleSheet('''
        QLabel#heading{
        font-family:Times New Roman;
        font-size:22px;
        font-weight:bold;
        margin-top:8px;
        margin-bottom:10px;
        }

        QLabel{
        font-family:Times New Roman;
        font-size:14px;
        font-weight:bold;
        margin-bottom:10px;
        }

        QLineEdit{
        font-family:Times New Roman;
        font-size:14px;
        margin-bottom:10px;
        }

        QPushButton{
        font-family:Times New Roman;
        font-size:14px;
        background-color:#068993;
        border-radius:5px;
        padding:5px;
        }

        QPushButton:hover{
        background-color:#2cc2cd;
        color:white;
        font-weight:bold;
        }

        QLabel#back{
        font-family:Times New Roman;
        font-size:14px;
        margin-top:10px;
        }
        ''')

        self.setLayout(form_layout)

    def reset_pwd(self):
        u = self.a.text().strip()
        n = self.b.text()
        p = self.c.text()

        if not u or not n or not p:
            QMessageBox.warning(self, "Empty", "Required field is empty.")
            return

        if n != p:
            QMessageBox.warning(self, "Unmatched", "Password didn't match.")
            return

        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM user WHERE username=?', (u,))
        user = cur.fetchone()

        if user:
            hash_np = hashlib.sha256(n.encode()).hexdigest()
            hash_cp = hashlib.sha256(p.encode()).hexdigest()

            cur.execute("UPDATE user SET new_password=?,confirm_password=? WHERE username=?", (hash_np, hash_cp, u))
            conn.commit()
            QMessageBox.information(self, "Success", "Password changed successfully.")
        else:
            QMessageBox.critical(self, "Not Found", "Username not found.")

        conn.close()

    def open_log(self):
        from login import Login
        self.login = Login()
        self.login.show()
        self.close()


if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = ForgotPassword()
    w.show()
    sys.exit(a.exec_())