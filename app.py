import  sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from  PyQt5.QtGui import *

class Inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.load_item()
        self.setObjectName("myWindow")

    def set_ui(self):
        #For main window
        self.setWindowTitle("Inventory Management System")
        self.setWindowIcon(QIcon("images/in.jpg"))
        self.setGeometry(200,200,550,550)

        #for Layout
        v=QVBoxLayout()

        #for form layout
        form=QFormLayout()
        self.lbl1=QLabel("Enter item name: ")
        self.txt1=QLineEdit()
        self.txt1.setPlaceholderText("Item name")
        self.lbl2=QLabel("Enter quantity of an item: ")
        self.txt2=QSpinBox()
        self.txt2.setMaximum(999)
        self.lbl3=QLabel("Enter price of an item: ")
        self.txt3=QDoubleSpinBox()
        self.txt3.setMaximum(999999)
        self.txt3.setDecimals(2)

        form.addRow(self.lbl1,self.txt1)
        form.addRow(self.lbl2,self.txt2)
        form.addRow(self.lbl3,self.txt3)
        v.addLayout(form)

        #for button
        h=QHBoxLayout()
        self.btn1=QPushButton("Add Item")
        self.btn1.setObjectName("addbtn")
        self.btn1.clicked.connect(self.add_item)
        self.btn2=QPushButton("Remove Item")
        self.btn2.setObjectName("delbtn")
        self.btn2.clicked.connect(self.delete_item)
        self.btn3=QPushButton("Edit Item")
        self.btn3.setObjectName("updatebtn")
        self.btn3.clicked.connect(self.update_item)
        h.addWidget(self.btn1)
        h.addWidget(self.btn2)
        h.addWidget(self.btn3)
        v.addLayout(h)

        #For table
        self.table=QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["SN","Name","Quantity","Price","Total"])
        self.table.horizontalHeader().setStyleSheet('''
            QHeaderView::section{
            background-color:#46464b;
            font-weight:bold;
            font-family:Times New Roman;
            color:#e2e2f1;
            padding:5px;
            }
        ''')
        self.table.horizontalHeader().setStretchLastSection(True)
        v.addWidget(self.table)

        self.setStyleSheet('''
        #myWindow{
        background-color:#c1c1e1;
        }
        
        QLabel{
        font-family:Times New Roman;
        font-weight:bold;
        font-size:14px;
        margin-bottom:3px;
        }
        
        QLineedit,QSpinBox,QDoubleSpinBox{
        margin-bottom:3px;
        }
        
        QPushButton{
        font-family:Times New Roman;
        font-weight:bold;
        border-radius:3px;
        margin:3px;
        padding:7px;
        }
        QPushButton#addbtn{
        background-color:#e80425;
        }
        
        QPushButton#addbtn:hover{
        background-color:#c42e43;
        color:white;
        font-weight:bold;
        }
        
        QPushButton#delbtn{
        background-color:#1342d9;
        }
        
        QPushButton#delbtn:hover{
        background-color:#4a6fe2;
        color:white;
        font-weight:bold;
        }
        
        QPushButton#updatebtn{
        background-color:#00af36;
        }
        
        QPushButton#updatebtn:hover{
        background-color:#3cf775;
        color:white;
        font-weight:bold;
        }
        
        QTableWidget{
        border:1px solid #8c948f;
        }
        ''')


        self.setLayout(v)

    def load_item(self):
        conn=sqlite3.connect('inventory.db')
        cur=conn.cursor()
        cur.execute("SELECT * FROM items")
        r=cur.fetchall()
        conn.close()

        self.table.setRowCount(0)

        for num,data in enumerate(r):
            self.table.insertRow(num)
            for col,c_data in enumerate(data):
                self.table.setItem(num,col,QTableWidgetItem(str(c_data)))

    def add_item(self):
        n=self.txt1.text().strip()
        q=self.txt2.value()
        p=self.txt3.value()
        t=q*p

        if n=="":
            QMessageBox.warning(self,"Invalid","Please enter item name.")

        conn=sqlite3.connect('inventory.db')
        cur=conn.cursor()
        cur.execute("INSERT INTO items (name,quantity,price,total) VALUES (?,?,?,?)",(n,q,p,t))
        conn.commit()
        conn.close()

        self.load_item()
        self.txt1.clear()
        self.txt2.setValue(0)
        self.txt3.setValue(0)

    def delete_item(self):
        s=self.table.currentRow()

        if s<0:
            QMessageBox.warning(self,"Invalid","Please select and item")

        item_id=self.table.item(s,0).text()

        conn=sqlite3.connect('inventory.db')
        cur=conn.cursor()
        cur.execute('DELETE FROM items WHERE sn=?',(item_id,))
        conn.commit()
        conn.close()
        self.load_item()

    def update_item(self):
        i=self.table.currentRow()
        n=self.txt1.text().strip()
        q=self.txt2.value()
        p=self.txt3.value()
        t=q*p

        if n=="":
            QMessageBox.warning(self,"Invalid","Please fill the item name for edit.")

        if i<0:
            QMessageBox.warning(self,"Invalid","Please select a data for editing.")

        item_id=self.table.item(i,0).text()

        conn=sqlite3.connect('inventory.db')
        cur=conn.cursor()
        cur.execute("UPDATE items SET name=?,quantity=?,price=?,total=? WHERE sn=?",(n,q,p,t,item_id))
        conn.commit()
        conn.close()
        self.load_item()

if __name__=="__main__":
    a=QApplication(sys.argv)
    w=Inventory()
    w.show()
    sys.exit(a.exec_())






