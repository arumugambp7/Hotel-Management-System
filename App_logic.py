import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog
from PyQt5.QtCore import QDate,Qt
from login import Ui_Dialog
import main
from reportlab.pdfgen  import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.platypus import TableStyle


ono = 0
class MainClass(QDialog):

    def __init__(self):
        super(MainClass,self).__init__()
        self.uilog = Ui_Dialog()
        self.uilog.setupUi(self)
        self.uilog.pb_login.clicked.connect(self.loginCheck)

    def loginCheck(self):
        if self.uilog.le_username.text() == "ad" and self.uilog.le_password.text() == "q":
            self.openMain()
            self.close()
        else:
            self.showMessageBox("Warning","Incorrect Password",QtWidgets.QMessageBox.Warning)

    def openMain(self):
        self.obj = QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.obj)
        self.obj.show()
        self.ui.t3_pb_add.clicked.connect(self.addDetails)
        self.ui.t3_pb_mod.clicked.connect(self.modDetails)
        self.ui.t3_pb_del.clicked.connect(self.delDetails)
        self.ui.t3_pb_reset.clicked.connect(self.t3reset)
        self.ui.t2_pb_VD.clicked.connect(self.viewDetails)
        self.ui.t2_pb_search.clicked.connect(self.searchDetails)
        self.ui.t2_pb_reset.clicked.connect(self.t2reset)
        self.ui.t1_pb_GD.clicked.connect(self.getDetails)
        self.ui.t1_pb_ATC.clicked.connect(self.addToCart)
        self.row = 0
        self.total = 0
        self.ui.t1_pb_del_itm.clicked.connect(self.deleteItem)
        self.ui.t1_pb_receipt.clicked.connect(self.receipt)
        self.ui.t1_pb_new_order.clicked.connect(self.newOrder)
        self.ui.t4_pb_GR.clicked.connect(self.getReport)
        self.ui.t4_pb_download.clicked.connect(self.download)
    def download(self):
        self.getReport()

        data = [["YEAR","MONTH","TOTAL ORDERS","TOTAL AMOUNT"]]
        for row in range(self.ui.t4_tw.rowCount()):
            data.append([self.ui.t4_tw.item(row, 0).text(),self.ui.t4_tw.item(row, 1).text(),self.ui.t4_tw.item(row, 2).text(),self.ui.t4_tw.item(row, 3).text()])


        print(data)
        c = canvas.Canvas("report.pdf",pagesize=letter)
        c.setFillColor(colors.red)
        c.setFont("Helvetica-Bold",48)
        c.drawCentredString(300,700,"XYZ RESTAURENT")
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(200, 600, "Monthly Sales Report")
        t = Table(data)
        style = TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.green),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, -1), "Courier-Bold"),
                            ("FONTSIZE", (0, 0), (-1,-1), 12),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BOX", (0, 0), (-1, -1), 2, colors.black),
                            ("GRID", (0, 0), (-1, -1), 2, colors.black)
                            ])
        t.setStyle(style)

        # Adding Alternate background color for rows
        total_rows = len(data)
        for i in range(1, total_rows):
            if i % 2 == 0:
                bc = colors.lightpink
            else:
                bc = colors.lightcyan
            ts = TableStyle([("BACKGROUND", (0, i), (-1, i), bc)])
            t.setStyle(ts)

        t.wrapOn(c, 100, 450)
        t.drawOn(c, 100, 450)
        c.showPage()
        c.save()


    def getReport(self):
        start_month = self.ui.t4_from.text()
        sm = start_month[:4] + '-' + start_month[5:] + '-' + '01'
        end_month = self.ui.t4_to.text()
        em = end_month[:4] + '-' + end_month[5:] + '-' + '31'
        print(start_month)
        print(end_month)
        print(int(start_month[5:]))
        print(int(end_month[5:]))
        if int(start_month[5:]) <= int(end_month[5:]):
            self.ui.t4_tw.setRowCount(0)
            con = sqlite3.connect("XYZ.db")
            result = con.execute('''SELECT strftime('%Y',odate),strftime('%m',odate) as "m",count(ono),sum(oamount) FROM ORDERS GROUP BY "m" HAVING odate BETWEEN ? AND ?''',(sm,em))
            to = 0
            total = 0
            for row,form in enumerate(result.fetchall()):
                self.ui.t4_tw.insertRow(row)
                for col,item in enumerate(form):
                    if col == 2:
                        to = to + item
                    elif col == 3:
                        total = total + item
                    self.ui.t4_tw.setItem(row,col,QtWidgets.QTableWidgetItem(str(item)))
            con.close()
            self.ui.t4_tot_orders.setText(str(to))
            self.ui.t4_total.setText(str(round(total,2)))
        else:
            self.showMessageBox("Warning", "start month should be less than the ending month", QtWidgets.QMessageBox.Warning)

    def newOrder(self):
        self.ui.t1_le_ono.setText("")
        self.ui.t1_le_fid.setText("")
        self.ui.t1_le_fname.setText("")
        self.ui.t1_le_qty.setText("")
        self.ui.t1_le_price.setText("")
        self.ui.t1_tw.setRowCount(0)
        self.ui.t1_displaytotal.setText("")
        self.ui.t1_displaytax.setText("")
        self.ui.t1_grandtotal.setText("")
        self.row = 0
        self.total = 0



    def receipt(self):
        con = sqlite3.connect("XYZ.db")
        con.execute("CREATE TABLE IF NOT EXISTS ORDERS(ono TEXT PRIMARY KEY,odate DATE,oamount NUMERIC)")
        on = self.onoGenerator()
        try:
            while (True):
                result = con.execute("Select ono from ORDERS")
                for count, row in enumerate(result.fetchall()):
                    for i, col in enumerate(row):
                        if col == on:
                            on = self.onoGenerator()
                        else:
                            orderno = on
                            con.close()
                            break
        except:
            self.ui.t1_le_ono.setText(orderno)
            now = QDate.currentDate()
            now = now.toString(Qt.ISODate)
            amt = self.ui.t1_grandtotal.text()
            o = self.ui.t1_le_ono.text()
            con = sqlite3.connect("XYZ.db")
            con.execute("INSERT INTO ORDERS(ono,odate,oamount)VALUES(?,?,?)",(o,now,amt))
            con.commit()
            con.close()
            data = []
            for row in range(self.ui.t1_tw.rowCount()):
                data.append([self.ui.t1_tw.item(row, 0).text(), self.ui.t1_tw.item(row, 1).text(),self.ui.t1_tw.item(row, 2).text(), self.ui.t1_tw.item(row, 3).text()])
            myformat = "{:<20}{:<10}{:<5}{}"
            with open("bill.txt","w") as target:
                target.write("\t\t\t\tXYZ RESTAURENT\n")
                target.write("\t\t\tTel : 0452 - 4321098\n")
                target.write("\n----------------------------------------------")
                target.write(f"\nOrder No : {self.ui.t1_le_ono.text()}\t\t\t\tDate : {now}")
                target.write("\n----------------------------------------------\n")
                target.write(myformat.format('Items','Price','QTY','Amount'))
                target.write("\n----------------------------------------------\n")
                for row in data:
                    target.write(myformat.format(row[0],row[1],row[2],row[3]))
                    target.write("\n")
                target.write("----------------------------------------------\n")
                target.write(f"\t\t\t\t\t\tTotal    : {self.ui.t1_displaytotal.text()}\n")
                target.write(f"\t\t\t\t\t\tTax(10%) : {self.ui.t1_displaytax.text()}\n")
                target.write(f"\t\t\t\t\t\tNetTotal : {self.ui.t1_grandtotal.text()}\n")
                target.write("----------------------------------------------\n")
                target.write("\t\t\t\tThanks! Visit Again")






    def deleteItem(self):
        rows = self.ui.t1_tw.selectionModel().selectedRows()
        for r in rows:
            deductamount = int(self.ui.t1_tw.item(self.ui.t1_tw.currentRow(), 3).text())
            self.total = self.total - deductamount
            tax = self.total * 0.1
            tax = round(tax,2)
            gtotal = self.total + tax
            self.row = self.row - 1
            self.ui.t1_tw.removeRow(r.row())
            self.ui.t1_displaytotal.setText(str(self.total))
            self.ui.t1_displaytax.setText(str(tax))
            self.ui.t1_grandtotal.setText(str(gtotal))
    def onoGenerator(self):
        global ono
        pstart = 1
        pinterval = 1
        if ono == 0:
            ono = pstart
        else:
            ono = ono + pinterval
        orderno = str(ono).zfill(3)
        return orderno
    def addToCart(self):
        name = self.ui.t1_le_fname.text()
        price = self.ui.t1_le_price.text()
        qty = self.ui.t1_le_qty.text()
        status = 0
        if name != "" and price != "" and qty != "":
            try:
                temp = int(price) * int(qty)
            except:
                self.showMessageBox("Warning", "price and quantity should be a number", QtWidgets.QMessageBox.Warning)
                status = 1
            if status == 0:

                self.ui.t1_tw.insertRow(self.row)
                self.ui.t1_tw.setItem(self.row,0,QtWidgets.QTableWidgetItem(name))
                self.ui.t1_tw.setItem(self.row,1,QtWidgets.QTableWidgetItem(price))
                self.ui.t1_tw.setItem(self.row,2, QtWidgets.QTableWidgetItem(qty))
                self.ui.t1_tw.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(temp)))

                self.total = self.total + temp

                self.ui.t1_displaytotal.setText(str(self.total))
                tax = self.total * 0.1
                tax = (round(tax,2))
                self.ui.t1_displaytax.setText(str(tax))
                gt = self.total + tax

                self.ui.t1_grandtotal.setText(str(gt))
                self.row += 1

        else:
            self.showMessageBox("Warning", "Please fill all the fields", QtWidgets.QMessageBox.Warning)






    def getDetails(self):
        a = self.ui.t1_le_fid.text()
        if a != "":
            con = sqlite3.connect("XYZ.db")
            result = con.execute("SELECT * FROM FOOD WHERE fid = ?",(a,))
            data = result.fetchone()

            if data != None:
                self.ui.t1_le_fname.setText(str(data[1]))
                self.ui.t1_le_price.setText(str(data[2]))
                self.ui.t1_le_qty.setText("1")
            else:
                self.showMessageBox("Warning", "Incorrect Food ID", QtWidgets.QMessageBox.Warning)

        else:
            self.showMessageBox("Warning","Please type the Food ID",QtWidgets.QMessageBox.Warning)

    def searchDetails(self):
        self.ui.t2_tw.setRowCount(0)
        a = self.ui.t2_le_fid.text()
        b = self.ui.t2_le_fname.text()
        con = sqlite3.connect("XYZ.db")
        print("connection established")
        print((a,b))
        c= (a,b)
        result = con.execute("SELECT * from FOOD WHERE fid LIKE ? OR fname LIKE ?",c)
        print("selction query executed")
        for count,row in enumerate(result.fetchall()):
            self.ui.t2_tw.insertRow(count)
            print(count)
            for i,item in enumerate(row):
                print(i)
                self.ui.t2_tw.setItem(count,i,QtWidgets.QTableWidgetItem(str(item)))
        con.close()


    def viewDetails(self):
        self.ui.t2_tw.setRowCount(0)
        con = sqlite3.connect("XYZ.db")
        result = con.execute("SELECT * FROM FOOD")
        for count,row in enumerate(result.fetchall()):
            self.ui.t2_tw.insertRow(count)
            for i,item in enumerate(row):
                self.ui.t2_tw.setItem(count,i,QtWidgets.QTableWidgetItem(str(item)))
        con.close()

    def t3reset(self):
        self.ui.t3_le_fid.setText("")
        self.ui.t3_le_fname.setText("")
        self.ui.t3_le_price.setText("")
    def t2reset(self):
        self.ui.t2_le_fid.setText("")
        self.ui.t2_le_fname.setText("")
        self.ui.t2_tw.setRowCount(0)


    def addDetails(self):
        fid = self.ui.t3_le_fid.text()
        fname = self.ui.t3_le_fname.text()
        fcost = self.ui.t3_le_price.text()
        status = 0
        if fid != "" and fname != "" and fcost != "":
            try:
                fcost = int(fcost)
            except:
                self.showMessageBox("Warning", "Cost can't be string", QtWidgets.QMessageBox.Warning)
                status = 1
            if status == 0:

                con = sqlite3.connect("XYZ.db")
                con.execute("CREATE TABLE IF NOT EXISTS FOOD(fid TEXT PRIMARY KEY NOT NULL,fname TEXT,fcost INT)")

                result = con.execute("Select fid from FOOD")
                check = 0
                for count,row in enumerate(result.fetchall()):
                    for i,col in enumerate(row):
                        if col == fid:
                            check = 1
                if check > 0:
                    self.showMessageBox("Warning", "Food ID already exists",QtWidgets.QMessageBox.Warning)
                    con.close()
                else:
                    con.execute("INSERT INTO FOOD VALUES(?,?,?)",(fid,fname,fcost))
                    self.showMessageBox("Status", "Record added successfully",QtWidgets.QMessageBox.Information)
                    con.commit()
                    con.close()
        else:
            self.showMessageBox("Warning", "Please fill all the fields", QtWidgets.QMessageBox.Warning)

    def modDetails(self):

        f1 = self.ui.t3_le_fid.text()
        f2 = self.ui.t3_le_fname.text()
        f3 = self.ui.t3_le_price.text()
        status = 0
        if f1 != "" and f2 != "" and f3!= "":
            try:
                f3 = int(f3)
            except:
                self.showMessageBox("Warning", "Cost can't be string", QtWidgets.QMessageBox.Warning)
                status = 1
            if status == 0:
                con = sqlite3.connect("XYZ.db")
                result = con.execute("Select fid from FOOD")
                check = 0

                for count, row in enumerate(result.fetchall()):
                    for i, col in enumerate(row):
                        if col == f1:
                            check = 1

                if check == 1:
                    con.execute("""Update FOOD SET fname = ?,fcost = ? WHERE fid = ?""",(f2,f3,f1))
                    self.showMessageBox("Status", "Record updated successfully",QtWidgets.QMessageBox.Information)
                    con.commit()
                    con.close()
                else:
                    self.showMessageBox("Warning", "Mentioned FID not exists",QtWidgets.QMessageBox.Warning)
                    con.commit()
                    con.close()
        else:
            self.showMessageBox("Warning", "Please fill all the fields", QtWidgets.QMessageBox.Warning)



    def delDetails(self):

        con = sqlite3.connect("XYZ.db")
        f = self.ui.t3_le_fid.text()
        result = con.execute("Select fid from FOOD")
        check = 0
        for count, row in enumerate(result.fetchall()):
            for i, col in enumerate(row):
                if col == f:
                    check = 1

        if check == 1:
            con.execute("DELETE FROM FOOD WHERE fid = ?",(f,))
            self.showMessageBox("Status", "Record deleted successfully", QtWidgets.QMessageBox.Information)
            con.commit()
            con.close()
        else:
            self.showMessageBox("Warning", "Mentioned FID not exists",QtWidgets.QMessageBox.Warning)
            con.commit()
            con.close()


    def showMessageBox(self,title,message,icon):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(icon)
        msgbox.setWindowTitle(title)
        msgbox.setText(message)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.exec_()

if __name__ == "__main__":
    app = QApplication([])
    window = MainClass()
    window.show()
    app.exec_()