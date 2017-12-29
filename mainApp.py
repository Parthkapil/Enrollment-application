import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import sqlite3
from io import BytesIO
from PIL import Image

import pyqrcode
import png

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def popup_msg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    popup.geometry("250x100+700+300")
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup,text="okay", command= popup.destroy)
    B1.pack()
    popup.mainloop()

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------EMPLOYEE DATA BASE FUNCTIONS----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def set_up_employee_table():
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    try:
        c.execute("CREATE TABLE  IF NOT EXISTS employees(fname TEXT NOT NULL,"
                  " lname TEXT NOT NULL, email TEXT PRIMARY KEY,"
                  " mnum TEXT NOT NULL, altnum TEXT NOT NULL,"
                  " address TEXT NOT NULL, altaddress TEXT NOT NULL,"
                  " photo BLOB NOT NULL, adhar BLOB NOT NULL )")
        conn.commit()
        print("EMPLOYEE TABLE CREATED")
        conn.close()
    except Exception as e:
        print("ERROR IN set_up_employee_table:->>",e)


def submit_to_the_employee_table(fname, lname, email, mnum, altnum, addr, altaddr, pname, aname):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    pimg = open(pname, "rb")
    pimg_data = pimg.read()
    pimg.close()

    aimg = open(aname, "rb")
    aimg_data = aimg.read()
    aimg.close()
    try:
        c.execute("INSERT INTO employees (fname, lname, email, mnum, altnum, address, altaddress, photo, adhar) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (fname, lname, email, mnum, altnum, addr, altaddr,
                                                         sqlite3.Binary(pimg_data), sqlite3.Binary(aimg_data)))
        conn.commit()
        conn.close()
        popup_msg("VALUES INSERTED TO \nTHE DATA BASE ")

    except Exception as e:
        print("ERROR IN submit_to_the_employee_table->>",e)


def load_emp_data(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    try:
        print(email)
        result = c.execute("SELECT * FROM employees WHERE email=?", (email,))
        return result
    except Exception as e:
        print("ERROR IN load_emp_data:->> ", e)


def update_employee_table(fname, lname, email, mnum, altnum, addr, altaddr, pname, aname):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    pimg = open(pname, "rb")
    pimg_data = pimg.read()
    pimg.close()

    aimg = open(aname, "rb")
    aimg_data = aimg.read()
    aimg.close()

    try:
        c.execute("UPDATE employees SET fname = ?, lname = ?, mnum = ?, altnum = ?,"
                  " address = ?, altaddress = ?, photo = ?, adhar = ? WHERE email = ? ",
                  (fname, lname, mnum, altnum, addr, altaddr,
                sqlite3.Binary(pimg_data), sqlite3.Binary(aimg_data),
                email))
        conn.commit()
        conn.close()
        popup_msg("VALUES UPDATED TO \nTHE DATA BASE ")

    except Exception as e:
        print("ERROR IN update_employee_table->>",e)


def delete_from_emp_db(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    try:
        c.execute("DELETE FROM employees WHERE email = ?", (email,))
        conn.commit()
        popup_msg("EMPLOYEE DELETED FROM \n THE DATA BASE")
        conn.close()
    except Exception as e:
        print("error in delete_from_emp_db:->>", e)


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------STUDENT DATA BASE FUNCTIONS----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def return_fname(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()
    name = ""

    try:
        result = c.execute("SELECT fname FROM employees where email = ?", (email,))
        for row in  result.fetchall():
            name = row[0]
        conn.close()
        return name
    except Exception as e:
        print("error in setup_admin_connection :->>", e)


def set_up_student_table():
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    try:
        c.execute("CREATE TABLE  IF NOT EXISTS students(fname TEXT NOT NULL,"
                  " lname TEXT NOT NULL, email TEXT PRIMARY KEY,"
                  " mnum TEXT NOT NULL, altnum TEXT NOT NULL,"
                  " address TEXT NOT NULL, altaddress TEXT NOT NULL,"
                  " photo BLOB NOT NULL, tenth BLOB NOT NULL, twelth BLOB NOT NULL )")
        conn.commit()
        print("Student TABLE CREATED....")
        conn.close()
    except Exception as e:
        print("ERROR IN set_up_student_table:->>", e)


def insert_into_student_table(fname, lname, email, mnum, altnum, addr, altaddr, pname, tenname, twelname):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    pimg = open(pname, "rb")
    pimg_data = pimg.read()
    pimg.close()

    tenimg = open(tenname, "rb")
    tenimg_data = tenimg.read()
    tenimg.close()

    twelimg = open(twelname, "rb")
    twelimg_data = twelimg.read()
    twelimg.close()

    try:
        c.execute("INSERT INTO students (fname, lname, email, mnum, altnum, address, altaddress, photo, tenth, twelth) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (fname, lname, email, mnum, altnum, addr, altaddr,
                                                         sqlite3.Binary(pimg_data), sqlite3.Binary(tenimg_data),
                                                         sqlite3.Binary(twelimg_data)))
        conn.commit()
        conn.close()
        popup_msg("VALUES INSERTED TO \nTHE DATA BASE ")
        print("values inserted")
    except Exception as e:
        print("ERROR IN insert_into_student_table->>", e)


def load_student_data(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()
    try:
        print(email)
        result = c.execute("SELECT * FROM students WHERE email=?", (email,))
        return result
    except Exception as e:
        print("ERROR IN load_student_data:->> ", e)


def update_student_table(fname, lname, email, mnum, altnum, addr, altaddr, pname, tenname, twelname):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    pimg = open(pname, "rb")
    pimg_data = pimg.read()
    pimg.close()

    tenimg = open(tenname, "rb")
    tenimg_data = tenimg.read()
    tenimg.close()

    twelimg = open(twelname, "rb")
    twelimg_data = twelimg.read()
    twelimg.close()

    try:
        c.execute("UPDATE students SET fname = ?, lname = ?, mnum = ?, altnum = ?,"
                  " address = ?, altaddress = ?, photo = ?, tenth = ?, twelth = ? WHERE email = ? ",
                  (fname, lname, mnum, altnum, addr, altaddr,
                   sqlite3.Binary(pimg_data), sqlite3.Binary(tenimg_data), sqlite3.Binary(twelimg_data),
                   email))
        conn.commit()
        conn.close()
        popup_msg("VALUES UPDATED TO \nTHE DATA BASE ")

    except Exception as e:
        print("ERROR IN update_student_table->>", e)


def delete_from_student_db(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()

    try:
        c.execute("DELETE FROM students WHERE email = ?", (email,))
        conn.commit()
        popup_msg("STUDENT DELETED FROM \n THE DATA BASE")
        conn.close()
    except Exception as e:
        print("error in delete_from_student_db:->>", e)


def generate_qr(email):
    q = pyqrcode.create(email)
    q.png("QrCode.png", scale=6)
    print("QR code generated.......")


def send_mail(rec_email):
    email_user = 'test199914@gmail.com'
    send_user = rec_email
    subject = "YOUR QR CODE!!!"

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = send_user
    msg["Subject"] = subject

    body = "YOU ARE ENROLLED IN BPIT COLLEGE. YOUR QR CODE IS ATTACHED. PLEASE KEEP IT SAFE FOR FUTURE USE."

    msg.attach(MIMEText(body, "plain"))

    filename = 'QrCode.png'
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=" + filename)
    msg.attach(part)

    text = msg.as_string()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, "sparshkapil14")

    server.sendmail(email_user, send_user, text)

    server.quit()

    print("EMAIL SENT........")


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------ADMIN DATA BASE FUNCTIONS----------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

def setup_admin_connection(email):
    conn = sqlite3.connect('myApp.db')
    c = conn.cursor()
    name = ""

    try:
        result = c.execute("SELECT fname FROM admin where email = ?", (email,))
        for row in  result.fetchall():
            name = row[0]
        conn.close()
        return name
    except Exception as e:
        print("error in setup_admin_connection :->>", e)


# ------------------------------------------------------------------------------------------------------------
# --------------------------------------MAIN CLASSES----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="appicon.ico")
        tk.Tk.wm_title(self, "STUDENT ADMISSION APPLICATION")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AdminLogin, EmployeeLogin, AdminPage, EmployeeInfo, StudentInfo, AdminInfo, EmployeePage, EmployeeForm, EmployeeUpdate,
                  StudentForm, StudentUpdate, AdminForm, AdminUpdate):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Start Page", font=10)
        label.pack()
        button1 = tk.Button(self, text="LOGIN AS ADMIN", height=10, width=20,
                            command= lambda: controller.show_frame(AdminLogin))
        button1.place(relx=0.2, rely=0.4, anchor="nw")
        button2 = tk.Button(self, text="LOGIN AS EMPLOYEE", height=10, width=20,
                            command=lambda: controller.show_frame(EmployeeLogin))
        button2.place(relx=0.6, rely=0.4, anchor="nw")


class AdminLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="\t\tADMIN LOGIN", font=10)
        label.grid(row=0, column=0)

        # --------------1st row-------------------

        email_label = tk.Label(self, text=" REGISTERED \nEMAIL", font="6")
        email_label.place(x=20, y=100, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=190, y=100, width=200, height=30, anchor="w")

        # --------------2nd row-------------------

        password_label = tk.Label(self, text="PASSWORD", font="6")
        password_label.place(x=20, y=200, anchor="w")

        self.password_entry = tk.StringVar(self, value="")
        self.password_entry_box = tk.Entry(self, textvariable=self.password_entry)
        self.password_entry_box.place(x=190, y=180, width=200, height=30, anchor="w")

        # --------------3rd row-------------------
        def check_admin():
            if not self.email_entry.get() or not self.password_entry.get():
                popup_msg("PLEASE FILL THE ENTRIES")
            else:
                if setup_admin_connection(self.email_entry.get()) == self.password_entry.get():
                    self.email_entry_box.delete(0, "end")
                    self.password_entry_box.delete(0, "end")
                    controller.show_frame(AdminPage)
                else:
                    popup_msg('WRONG USERNAME \nOR PASSWORD')

        button1 = tk.Button(self, text="LOGIN", height=5, width=20,
                            command=lambda: check_admin())
        button1.place(x=190, y=250)

        # --------------4th row-------------------

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=220, y=450)


class EmployeeLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="EMPLOYEE LOGIN", font=10)
        label.pack()

        # --------------1st row-------------------

        email_label = tk.Label(self, text=" REGISTERED \nEMAIL", font="6")
        email_label.place(x=20, y=100, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=190, y=100, width=200, height=30, anchor="w")

        # --------------2nd row-------------------

        password_label = tk.Label(self, text="PASSWORD", font="6")
        password_label.place(x=20, y=200, anchor="w")

        self.password_entry = tk.StringVar(self, value="")
        self.password_entry_box = tk.Entry(self, textvariable=self.password_entry)
        self.password_entry_box.place(x=190, y=180, width=200, height=30, anchor="w")

        # --------------3rd row-------------------

        def check_employee():
            if not self.email_entry.get() or not self.password_entry.get():
                popup_msg("PLEASE FILL THE ENTRIES")
            else:
                if return_fname(self.email_entry.get()) == self.password_entry.get():
                    self.email_entry_box.delete(0, "end")
                    self.password_entry_box.delete(0, "end")
                    controller.show_frame(EmployeePage)
                else:
                    popup_msg('WRONG USERNAME \nOR PASSWORD')

        button1 = tk.Button(self, text="LOGIN", height=5, width=20,
                            command=lambda: check_employee())
        button1.place(x=190, y=250)

        # --------------4th row-------------------

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=220, y=450)

# --------------------------------------------------------------------------------------------------------------
# -------------------------------------------AFTER ADMIN LOGIN---------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Admin Page", font =10)
        label.pack()
        button1 = tk.Button(self, text="Employee Information", height=5, width=20,
                            command=lambda: controller.show_frame(EmployeeInfo))
        button1.place(x=170, y=100)
        button2 = tk.Button(self, text="Student Information", height=5, width=20,
                            command=lambda: controller.show_frame(StudentInfo))
        button2.place(x=170, y=200)
        button3 = tk.Button(self, text="Aadmin Information", height=5, width=20,
                            command=lambda: controller.show_frame(AdminInfo))
        button3.place(x=170, y=300)
        backButton = tk.Button(self, text="back", command=lambda: controller.show_frame(StartPage))
        backButton.place(x=220, y=450)


class EmployeeInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="EMPLOYEE INFORMATION", font=10)
        label.pack()
        button1 = tk.Button(self, text="ADD NEW EMPLOYEE", height=5, width=20,
                            command=lambda: controller.show_frame(EmployeeForm))
        button1.place(x=170, y=100)
        button2 = tk.Button(self, text="EDIT AN EMPLOYEE", height=5, width=20,
                            command=lambda: controller.show_frame(EmployeeUpdate))
        button2.place(x=170, y=200)
        backButton = tk.Button(self, text="back", command=lambda: controller.show_frame(AdminPage))
        backButton.place(x=220, y=450)


class StudentInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="STUDENT INFORMATION", font=10)
        label.pack()

        button1 = tk.Button(self, text="ADD NEW STUDENT", height=5, width=20,
                            command=lambda: controller.show_frame(StudentForm))
        button1.place(x=170, y=100)
        button2 = tk.Button(self, text="EDIT AN STUDENT", height=5, width=20,
                            command=lambda: controller.show_frame(StudentUpdate))
        button2.place(x=170, y=200)
        backButton = tk.Button(self, text="back", command=lambda: controller.show_frame(AdminPage))
        backButton.place(x=220, y=450)


class AdminInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ADMIN INFORMATION", font=10)
        label.pack()

        button1 = tk.Button(self, text="ADD NEW ADMIN", height=5, width=20,
                            command=lambda: controller.show_frame(AdminForm))
        button1.place(x=170, y=100)
        button2 = tk.Button(self, text="EDIT AN ADMIN", height=5, width=20,
                            command=lambda: controller.show_frame(AdminUpdate))
        button2.place(x=170, y=200)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(AdminPage))
        back_button.place(x=220, y=450)


class EmployeeForm(tk.Frame):
    photoname = ""
    adharname = ""

    def clear_all(self):
        self.fname_entry_box.delete(0, "end")
        self.lname_entry_box.delete(0, "end")
        self.email_entry_box.delete(0, "end")
        self.mnumber_entry_box.delete(0, "end")
        self.altnumber_entry_box.delete(0, 'end')
        self.address_entry_box.delete(0, "end")
        self.altaddress_entry_box.delete(0, "end")
        self.photo_entry_box.delete(0, "end")
        self.adhar_entry_box.delete(0, "end")

    def photo_file_dialogue(self):
        self.photoname = askopenfilename()
        print(self.photoname)
        self.photo_entry.set(self.photoname)

    def adhar_file_dialogue(self):
        self.adharname = askopenfilename()
        print(self.adharname)
        self.adhar_entry.set(self.adharname)

    def check_all_fill(self):
        if not self.fname_entry.get() or not self.lname_entry.get() or not self.email_entry.get() or not self.mnumber_entry.get() or not self.altnumber_entry.get() or not self.address_entry.get() or not self.altaddress_entry.get() or not self.photo_entry.get() or not self.adhar_entry.get():
            popup_msg('FILL ALL ENTRIES')
        else:
            submit_to_the_employee_table(self.fname_entry.get(), self.lname_entry.get(),
                                         self.email_entry.get(), self.mnumber_entry.get(),
                                         self.altnumber_entry.get(), self.address_entry.get(),
                                         self.altaddress_entry.get(), self.photoname, self.adharname)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        set_up_employee_table()
        label = tk.Label(self, text="NEW EMPLOYEE FORM", font=10)
        label.pack()

        # --------------First name -------------------

        fname_label = tk.Label(self, text="FIRST NAME", font=("Verdana", 10))
        fname_label.place(x=50, y=50, anchor="w")

        self.fname_entry = tk.StringVar(self, value="")
        self.fname_entry_box = tk.Entry(self, textvariable=self.fname_entry)
        self.fname_entry_box.place(x=170, y=50, width=200, anchor="w")

        # --------------Last name -------------------

        lname_label = tk.Label(self, text="LAST NAME", font=("Verdana", 10))
        lname_label.place(x=50, y=80, anchor="w")

        self.lname_entry = tk.StringVar(self, value="")
        self.lname_entry_box = tk.Entry(self, textvariable=self.lname_entry)
        self.lname_entry_box.place(x=170, y=80, width=200, anchor="w")

        # --------------EMAIL-------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=50, y=110, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=170, y=110, width=200, anchor="w")

        # --------------MOBILE NUMBER-------------------

        mnumber_label = tk.Label(self, text="MOBILE NUMBER", font=("Verdana", 10))
        mnumber_label.place(x=50, y=140, anchor="w")

        self.mnumber_entry = tk.StringVar(self, value="")
        self.mnumber_entry_box = tk.Entry(self, textvariable=self.mnumber_entry)
        self.mnumber_entry_box.place(x=170, y=140, width=200, anchor="w")

        # --------------ALTERNATE NUMBER-------------------

        altnumber_label = tk.Label(self, text="ALT. NUMBER", font=("Verdana", 10))
        altnumber_label.place(x=50, y=170, anchor="w")

        self.altnumber_entry = tk.StringVar(self, value="")
        self.altnumber_entry_box = tk.Entry(self, textvariable=self.altnumber_entry)
        self.altnumber_entry_box.place(x=170, y=170, width=200, anchor="w")

        # --------------ADDRESS-------------------

        address_label = tk.Label(self, text="ADDRESS", font=("Verdana", 10))
        address_label.place(x=50, y=200, anchor="w")

        self.address_entry = tk.StringVar(self, value="")
        self.address_entry_box = tk.Entry(self, textvariable=self.address_entry)
        self.address_entry_box.place(x=170, y=200, width=200, anchor="w")

        # --------------ALTERNATE ADDRESS-------------------

        altaddress_label = tk.Label(self, text="ALT. ADDRESS", font=("Verdana", 10))
        altaddress_label.place(x=50, y=230, anchor="w")

        self.altaddress_entry = tk.StringVar(self, value="")
        self.altaddress_entry_box = tk.Entry(self, textvariable=self.altaddress_entry)
        self.altaddress_entry_box.place(x=170, y=230, width=200, anchor="w")

        # --------------PHOTO -------------------

        photo_label = tk.Label(self, text="PHOTOGRAPH", font=("Verdana", 10))
        photo_label.place(x=50, y=260, anchor="w")

        self.photo_entry = tk.StringVar(self, value="")
        self.photo_entry_box = tk.Entry(self, textvariable=self.photo_entry)
        self.photo_entry_box.place(x=170, y=260, width=200, anchor="w")

        pchoose_button = ttk.Button(self, text="CHOOSE FILE", command= lambda: self.photo_file_dialogue())
        pchoose_button.place(x=170, y=290)

        self.photo_entry.set(self.photoname)

        # --------------ADHAR CARD-------------------

        adhar_label = tk.Label(self, text="ADHAR CARD", font=("Verdana", 10))
        adhar_label.place(x=50, y=330, anchor="w")

        self.adhar_entry = tk.StringVar(self, value="")
        self.adhar_entry_box = tk.Entry(self, textvariable=self.adhar_entry)
        self.adhar_entry_box.place(x=170, y=330, width=200, anchor="w")

        achoose_button = ttk.Button(self, text="CHOOSE FILE", command= lambda:self.adhar_file_dialogue())
        achoose_button.place(x=170, y=360)

        # --------------SUBMIT BUTTON------------------------

        submit_button = tk.Button(self, text="SUBMIT", width=20, fg="red", command= lambda: self.check_all_fill())
        submit_button.place(x=180, y=400)

        # --------------CLEAR BUTTON------------------------

        clear_button = tk.Button(self, text="CLEAR ALL", width=10, fg="red", command=lambda: self.clear_all())
        clear_button.place(x=350, y=400)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(EmployeeInfo))
        back_button.place(x=220, y=450)


class EmployeeUpdate(tk.Frame):
    photoname = ""
    adharname = ""
    photoname_changed = False
    adharname_changed = False

    def clear_all(self):
        self.fname_entry_box.delete(0, "end")
        self.lname_entry_box.delete(0, "end")
        self.email_entry_box.delete(0, "end")
        self.mnumber_entry_box.delete(0, "end")
        self.altnumber_entry_box.delete(0, 'end')
        self.address_entry_box.delete(0, "end")
        self.altaddress_entry_box.delete(0, "end")
        self.email1_entry_box.delete(0, "end")
        self.pImage = 0
        self.aImage = 0

    def photo_file_dialogue(self):
        self.photoname_changed = True
        self.photoname = askopenfilename()
        print(self.photoname)

    def adhar_file_dialogue(self):
        self.adharname_changed = True
        self.adharname = askopenfilename()
        print(self.adharname)

    def check_all_fill(self):
        if not self.fname_entry.get() or not self.lname_entry.get() or not self.email_entry.get() or not self.mnumber_entry.get() or not self.altnumber_entry.get() or not self.address_entry.get() or not self.altaddress_entry.get() and self.photoname == ""  and self.adharname == "" :
            popup_msg('FILL ALL ENTRIES')
        else:
            update_employee_table(self.fname_entry.get(), self.lname_entry.get(),
                                  self.email_entry.get(), self.mnumber_entry.get(),
                                  self.altnumber_entry.get(), self.address_entry.get(),
                                  self.altaddress_entry.get(), self.photoname, self.adharname)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pImage = 0
        self.aImage = 0

        label = tk.Label(self, text="EMPLOYEES INFORMATION FROM DATABASE", font=5)
        label.pack()

        # -------------Email------------------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=20, y=40)

        self.email1_entry = tk.StringVar(self, value="")
        self.email1_entry_box = tk.Entry(self, textvariable=self.email1_entry)
        self.email1_entry_box.place(x=70, y=40, width=150)

        def load_emp_to_entries():
            for row in load_emp_data(self.email1_entry.get()).fetchall():
                self.fname_entry.set(row[0])
                self.lname_entry.set(row[1])
                self.email_entry.set(row[2])
                self.mnumber_entry.set(row[3])
                self.altnumber_entry.set(row[4])
                self.address_entry.set(row[5])
                self.altaddress_entry.set(row[6])
                pfetch_img = row[7]
                afetch_img = row[8]

                pfile = BytesIO(pfetch_img)
                afile = BytesIO(afetch_img)

                self.pImage = Image.open(pfile)
                print(pfile)
                self.aImage = Image.open(afile)

        b1 = tk.Button(self, text="SEARCH", command=lambda: load_emp_to_entries())
        b1.place(x=230, y=35)

        # ------------------OR-----------------------------

        or_label = tk.Label(self, text="OR", font=("verdana", 15))
        or_label.place(x=300, y=30)

        # --------------------Scan Qr---------------------------

        qr_button = tk.Button(self, text="SCAN QR", command=lambda: popup_msg("NOT SUPPORTED YET"), width=15)
        qr_button.place(x=350, y=35)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(EmployeeInfo))
        back_button.place(x=220, y=450)

        # ----------------SEPERATOR-------------------------------

        seperator = tk.Label(self, text="----------------------------------------------------------------------"
                                        "-----------------------------------------------------------",fg="black")
        seperator.place(x=0, y=60)

        # --------------First name -------------------

        fname_label = tk.Label(self, text="FIRST NAME", font=("Verdana", 10))
        fname_label.place(x=20, y=100, anchor="w")

        self.fname_entry = tk.StringVar(self, value="")
        self.fname_entry_box = tk.Entry(self, textvariable=self.fname_entry)
        self.fname_entry_box.place(x=150, y=100, width=200, anchor="w")

        # --------------Last name -------------------

        lname_label = tk.Label(self, text="LAST NAME", font=("Verdana", 10))
        lname_label.place(x=20, y=130, anchor="w")

        self.lname_entry = tk.StringVar(self, value="")
        self.lname_entry_box = tk.Entry(self, textvariable=self.lname_entry)
        self.lname_entry_box.place(x=150, y=130, width=200, anchor="w")

        # --------------EMAIL-------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=10, y=160, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=150, y=160, width=200, anchor="w")

        # --------------MOBILE NUMBER-------------------

        mnumber_label = tk.Label(self, text="MOBILE NUMBER", font=("Verdana", 10))
        mnumber_label.place(x=20, y=190, anchor="w")

        self.mnumber_entry = tk.StringVar(self, value="")
        self.mnumber_entry_box = tk.Entry(self, textvariable=self.mnumber_entry)
        self.mnumber_entry_box.place(x=150, y=190, width=200, anchor="w")

        # --------------ALTERNATE NUMBER-------------------

        altnumber_label = tk.Label(self, text="ALT. NUMBER", font=("Verdana", 10))
        altnumber_label.place(x=20, y=220, anchor="w")

        self.altnumber_entry = tk.StringVar(self, value="")
        self.altnumber_entry_box = tk.Entry(self, textvariable=self.altnumber_entry)
        self.altnumber_entry_box.place(x=150, y=220, width=200, anchor="w")

        # --------------ADDRESS-------------------

        address_label = tk.Label(self, text="ADDRESS", font=("Verdana", 10))
        address_label.place(x=20, y=250, anchor="w")

        self.address_entry = tk.StringVar(self, value="")
        self.address_entry_box = tk.Entry(self, textvariable=self.address_entry)
        self.address_entry_box.place(x=150, y=250, width=200, anchor="w")

        # --------------ALTERNATE ADDRESS-------------------

        altaddress_label = tk.Label(self, text="ALT. ADDRESS", font=("Verdana", 10))
        altaddress_label.place(x=20, y=280, anchor="w")

        self.altaddress_entry = tk.StringVar(self, value="")
        self.altaddress_entry_box = tk.Entry(self, textvariable=self.altaddress_entry)
        self.altaddress_entry_box.place(x=150, y=280, width=200, anchor="w")

        # --------------PHOTO -------------------

        photo_label = tk.Label(self, text="PHOTOGRAPH", font=("Verdana", 10))
        photo_label.place(x=20, y=320, anchor="w")

        popen_button = ttk.Button(self, text="OPEN FILE", command=lambda: self.pImage.show())
        popen_button.place(x=170, y=310)

        pchoose_button = ttk.Button(self, text="CHOOSE NEW FILE", command=lambda: self.photo_file_dialogue())
        pchoose_button.place(x=340, y=310)

        # --------------ADHAR CARD-------------------

        adhar_label = tk.Label(self, text="ADHAR CARD", font=("Verdana", 10))
        adhar_label.place(x=20, y=370, anchor="w")

        aopen_button = ttk.Button(self, text="OPEN FILE", command=lambda: self.aImage.show())
        aopen_button.place(x=170, y=360)

        achoose_button = ttk.Button(self, text="CHOOSE NEW FILE", command=lambda: self.adhar_file_dialogue())
        achoose_button.place(x=340, y=360)

        # --------------UPDATE BUTTON------------------------

        update_button = tk.Button(self, text="UPDATE", width=20, fg="red", command=lambda: self.check_all_fill())
        update_button.place(x=20, y=420)

        # --------------DELETE-------------------------------------

        def delete():
            email = self.email1_entry.get()
            self.clear_all()
            delete_from_emp_db(email)


        delete_button = tk.Button(self, text="DELETE", width=20, fg="red", command=lambda: delete())
        delete_button.place(x=200, y=420)

        # -------------CLEAR ALL---------------------------------

        clear_button = tk.Button(self, text="CLEAR ALL", width=10, fg="red", command=lambda: self.clear_all())
        clear_button.place(x=400, y=420)


class StudentForm(tk.Frame):
    photoname = ""
    adharname = ""

    def clear_all(self):
        self.fname_entry_box.delete(0, "end")
        self.lname_entry_box.delete(0, "end")
        self.email_entry_box.delete(0, "end")
        self.mnumber_entry_box.delete(0, "end")
        self.altnumber_entry_box.delete(0, 'end')
        self.address_entry_box.delete(0, "end")
        self.altaddress_entry_box.delete(0, "end")
        self.photo_entry_box.delete(0, "end")
        self.tenth_entry_box.delete(0, "end")
        self.twelth_entry_box.delete(0, "end")

    def photo_file_dialogue(self):
        self.photoname = askopenfilename()
        print(self.photoname)
        self.photo_entry.set(self.photoname)

    def tenth_file_dialogue(self):
        self.tenthname = askopenfilename()
        print(self.adharname)
        self.tenth_entry.set(self.tenthname)

    def twelth_file_dialogue(self):
        self.twelthname = askopenfilename()
        print(self.adharname)
        self.twelth_entry.set(self.twelthname)

    def qr_submit_mail(self):
        generate_qr(self.email_entry.get())
        send_mail(self.email_entry.get())
        insert_into_student_table(self.fname_entry.get(), self.lname_entry.get(),
                                  self.email_entry.get(), self.mnumber_entry.get(),
                                  self.altnumber_entry.get(), self.address_entry.get(),
                                  self.altaddress_entry.get(), self.photoname, self.tenthname,
                                  self.twelthname)

    def check_all_fill(self):
        if not self.fname_entry.get() or not self.lname_entry.get() or not self.email_entry.get() or not self.mnumber_entry.get() or not self.altnumber_entry.get() or not self.address_entry.get() or not self.altaddress_entry.get() or not self.photo_entry.get() or not self.tenth_entry.get() or not self.twelth_entry.get():
            popup_msg('FILL ALL ENTRIES')
        else:
            self.qr_submit_mail()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        set_up_student_table()
        label = tk.Label(self, text="NEW STUDENT FORM", font=10)
        label.pack()

        # --------------First name -------------------

        fname_label = tk.Label(self, text="FIRST NAME", font=("Verdana", 10))
        fname_label.place(x=50, y=50, anchor="w")

        self.fname_entry = tk.StringVar(self, value="")
        self.fname_entry_box = tk.Entry(self, textvariable=self.fname_entry)
        self.fname_entry_box.place(x=170, y=50, width=200, anchor="w")

        # --------------Last name -------------------

        lname_label = tk.Label(self, text="LAST NAME", font=("Verdana", 10))
        lname_label.place(x=50, y=80, anchor="w")

        self.lname_entry = tk.StringVar(self, value="")
        self.lname_entry_box = tk.Entry(self, textvariable=self.lname_entry)
        self.lname_entry_box.place(x=170, y=80, width=200, anchor="w")

        # --------------EMAIL-------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=50, y=110, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=170, y=110, width=200, anchor="w")

        # --------------MOBILE NUMBER-------------------

        mnumber_label = tk.Label(self, text="MOBILE NUMBER", font=("Verdana", 10))
        mnumber_label.place(x=50, y=140, anchor="w")

        self.mnumber_entry = tk.StringVar(self, value="")
        self.mnumber_entry_box = tk.Entry(self, textvariable=self.mnumber_entry)
        self.mnumber_entry_box.place(x=170, y=140, width=200, anchor="w")

        # --------------ALTERNATE NUMBER-------------------

        altnumber_label = tk.Label(self, text="ALT. NUMBER", font=("Verdana", 10))
        altnumber_label.place(x=50, y=170, anchor="w")

        self.altnumber_entry = tk.StringVar(self, value="")
        self.altnumber_entry_box = tk.Entry(self, textvariable=self.altnumber_entry)
        self.altnumber_entry_box.place(x=170, y=170, width=200, anchor="w")

        # --------------ADDRESS-------------------

        address_label = tk.Label(self, text="ADDRESS", font=("Verdana", 10))
        address_label.place(x=50, y=200, anchor="w")

        self.address_entry = tk.StringVar(self, value="")
        self.address_entry_box = tk.Entry(self, textvariable=self.address_entry)
        self.address_entry_box.place(x=170, y=200, width=200, anchor="w")

        # --------------ALTERNATE ADDRESS-------------------

        altaddress_label = tk.Label(self, text="ALT. ADDRESS", font=("Verdana", 10))
        altaddress_label.place(x=50, y=230, anchor="w")

        self.altaddress_entry = tk.StringVar(self, value="")
        self.altaddress_entry_box = tk.Entry(self, textvariable=self.altaddress_entry)
        self.altaddress_entry_box.place(x=170, y=230, width=200, anchor="w")

        # --------------PHOTO -------------------

        photo_label = tk.Label(self, text="PHOTOGRAPH", font=("Verdana", 10))
        photo_label.place(x=50, y=270, anchor="w")

        self.photo_entry = tk.StringVar(self, value="")
        self.photo_entry_box = tk.Entry(self, textvariable=self.photo_entry)
        self.photo_entry_box.place(x=170, y=270, width=200, anchor="w")

        pchoose_button = ttk.Button(self, text="CHOOSE FILE", command=lambda: self.photo_file_dialogue())
        pchoose_button.place(x=400, y=260)

        self.photo_entry.set(self.photoname)

        # --------------TENTH MARKSHET-------------------

        tenth_label = tk.Label(self, text="TENTH \nMARKSHEET", font=("Verdana", 10))
        tenth_label.place(x=50, y=310, anchor="w")

        self.tenth_entry = tk.StringVar(self, value="")
        self.tenth_entry_box = tk.Entry(self, textvariable=self.tenth_entry)
        self.tenth_entry_box.place(x=170, y=310, width=200, anchor="w")

        tenchoose_button = ttk.Button(self, text="CHOOSE FILE", command=lambda: self.tenth_file_dialogue())
        tenchoose_button.place(x=400, y=300)

        # --------------TENTH MARKSHET-------------------

        twelth_label = tk.Label(self, text="TWELTH \nMARKSHEET", font=("Verdana", 10))
        twelth_label.place(x=50, y=360, anchor="w")

        self.twelth_entry = tk.StringVar(self, value="")
        self.twelth_entry_box = tk.Entry(self, textvariable=self.twelth_entry)
        self.twelth_entry_box.place(x=170, y=360, width=200, anchor="w")

        tenchoose_button = ttk.Button(self, text="CHOOSE FILE", command=lambda: self.twelth_file_dialogue())
        tenchoose_button.place(x=400, y=350)

        # --------------SUBMIT BUTTON------------------------

        submit_button = tk.Button(self, text="SUBMIT", width=20, fg="red", command=lambda: self.check_all_fill())
        submit_button.place(x=180, y=400)

        # --------------CLEAR BUTTON------------------------

        clear_button = tk.Button(self, text="CLEAR ALL", width=10, fg="red", command=lambda: self.clear_all())
        clear_button.place(x=350, y=400)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(StudentInfo))
        back_button.place(x=220, y=450)


class StudentUpdate(tk.Frame):
    photoname = ""
    tenthname = ""
    twelthname = ""
    photoname_changed = False
    tenthname_changed = False
    twelthname_changed = False

    def clear_all(self):
        self.fname_entry_box.delete(0, "end")
        self.lname_entry_box.delete(0, "end")
        self.email_entry_box.delete(0, "end")
        self.mnumber_entry_box.delete(0, "end")
        self.altnumber_entry_box.delete(0, 'end')
        self.address_entry_box.delete(0, "end")
        self.altaddress_entry_box.delete(0, "end")
        self.email1_entry_box.delete(0, "end")
        self.pImage = 0
        self.tenImage = 0
        self.twelImage = 0

    def photo_file_dialogue(self):
        self.photoname_changed = True
        self.photoname = askopenfilename()
        print(self.photoname)

    def tenth_file_dialogue(self):
        self.tenthname_changed = True
        self.tenthname = askopenfilename()
        print(self.tenthname)

    def twelth_file_dialogue(self):
        self.twelthname_changed = True
        self.twelthname = askopenfilename()
        print(self.twelthname)

    def check_all_fill(self):
        if not self.fname_entry.get() or not self.lname_entry.get() or not self.email_entry.get() or not self.mnumber_entry.get() or not self.altnumber_entry.get() or not self.address_entry.get() or not self.altaddress_entry.get() and self.photoname == "" and self.tenthname == "" or self.twelthname == "":
            popup_msg('FILL ALL ENTRIES')
        else:
            update_student_table(self.fname_entry.get(), self.lname_entry.get(),
                                  self.email_entry.get(), self.mnumber_entry.get(),
                                  self.altnumber_entry.get(), self.address_entry.get(),
                                  self.altaddress_entry.get(), self.photoname, self.tenthname, self.twelthname)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pImage = 0
        self.twelImage = 0
        self.tenImage = 0

        label = tk.Label(self, text="STUDENTS INFORMATION FROM DATABASE", font=5)
        label.pack()

        # -------------Email------------------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=20, y=40)

        self.email1_entry = tk.StringVar(self, value="")
        self.email1_entry_box = tk.Entry(self, textvariable=self.email1_entry)
        self.email1_entry_box.place(x=70, y=40, width=150)

        def load_student_to_entries():
            for row in load_student_data(self.email1_entry.get()).fetchall():
                self.fname_entry.set(row[0])
                self.lname_entry.set(row[1])
                self.email_entry.set(row[2])
                self.mnumber_entry.set(row[3])
                self.altnumber_entry.set(row[4])
                self.address_entry.set(row[5])
                self.altaddress_entry.set(row[6])
                pfetch_img = row[7]
                tenfetch_img = row[8]
                twelfetch_img = row[9]

                pfile = BytesIO(pfetch_img)
                tenfile = BytesIO(tenfetch_img)
                twelfile = BytesIO(twelfetch_img)

                self.pImage = Image.open(pfile)
                # print(pfile)
                self.tenImage = Image.open(tenfile)
                self.twelImage = Image.open(twelfile)

        b1 = tk.Button(self, text="SEARCH", command=lambda: load_student_to_entries())
        b1.place(x=230, y=35)

        # ------------------OR-----------------------------

        or_label = tk.Label(self, text="OR", font=("verdana", 15))
        or_label.place(x=300, y=30)

        # --------------------Scan Qr---------------------------

        qr_button = tk.Button(self, text="SCAN QR", command=lambda: popup_msg("NOT SUPPORTED YET"), width=15)
        qr_button.place(x=350, y=35)

        # ----------------SEPERATOR-------------------------------

        seperator = tk.Label(self, text="----------------------------------------------------------------------"
                                        "-----------------------------------------------------------", fg="black")
        seperator.place(x=0, y=60)

        # --------------First name -------------------

        fname_label = tk.Label(self, text="FIRST NAME", font=("Verdana", 10))
        fname_label.place(x=20, y=100, anchor="w")

        self.fname_entry = tk.StringVar(self, value="")
        self.fname_entry_box = tk.Entry(self, textvariable=self.fname_entry)
        self.fname_entry_box.place(x=150, y=100, width=200, anchor="w")

        # --------------Last name -------------------

        lname_label = tk.Label(self, text="LAST NAME", font=("Verdana", 10))
        lname_label.place(x=20, y=130, anchor="w")

        self.lname_entry = tk.StringVar(self, value="")
        self.lname_entry_box = tk.Entry(self, textvariable=self.lname_entry)
        self.lname_entry_box.place(x=150, y=130, width=200, anchor="w")

        # --------------EMAIL-------------------

        email_label = tk.Label(self, text="EMAIL", font=("Verdana", 10))
        email_label.place(x=10, y=160, anchor="w")

        self.email_entry = tk.StringVar(self, value="")
        self.email_entry_box = tk.Entry(self, textvariable=self.email_entry)
        self.email_entry_box.place(x=150, y=160, width=200, anchor="w")

        # --------------MOBILE NUMBER-------------------

        mnumber_label = tk.Label(self, text="MOBILE NUMBER", font=("Verdana", 10))
        mnumber_label.place(x=20, y=190, anchor="w")

        self.mnumber_entry = tk.StringVar(self, value="")
        self.mnumber_entry_box = tk.Entry(self, textvariable=self.mnumber_entry)
        self.mnumber_entry_box.place(x=150, y=190, width=200, anchor="w")

        # --------------ALTERNATE NUMBER-------------------

        altnumber_label = tk.Label(self, text="ALT. NUMBER", font=("Verdana", 10))
        altnumber_label.place(x=20, y=220, anchor="w")

        self.altnumber_entry = tk.StringVar(self, value="")
        self.altnumber_entry_box = tk.Entry(self, textvariable=self.altnumber_entry)
        self.altnumber_entry_box.place(x=150, y=220, width=200, anchor="w")

        # --------------ADDRESS-------------------

        address_label = tk.Label(self, text="ADDRESS", font=("Verdana", 10))
        address_label.place(x=20, y=250, anchor="w")

        self.address_entry = tk.StringVar(self, value="")
        self.address_entry_box = tk.Entry(self, textvariable=self.address_entry)
        self.address_entry_box.place(x=150, y=250, width=200, anchor="w")

        # --------------ALTERNATE ADDRESS-------------------

        altaddress_label = tk.Label(self, text="ALT. ADDRESS", font=("Verdana", 10))
        altaddress_label.place(x=20, y=280, anchor="w")

        self.altaddress_entry = tk.StringVar(self, value="")
        self.altaddress_entry_box = tk.Entry(self, textvariable=self.altaddress_entry)
        self.altaddress_entry_box.place(x=150, y=280, width=200, anchor="w")

        # --------------PHOTO -------------------

        photo_label = tk.Label(self, text="PHOTOGRAPH", font=("Verdana", 10))
        photo_label.place(x=20, y=320, anchor="w")

        popen_button = ttk.Button(self, text="OPEN FILE", command=lambda: self.pImage.show())
        popen_button.place(x=170, y=310)

        pchoose_button = ttk.Button(self, text="CHOOSE NEW FILE", command=lambda: self.photo_file_dialogue())
        pchoose_button.place(x=340, y=310)

        # --------------TENTH MARKSHEET-------------------

        tenth_label = tk.Label(self, text="TENTH MARKSHEET", font=("Verdana", 10))
        tenth_label.place(x=20, y=345, anchor="w")

        tenopen_button = ttk.Button(self, text="OPEN FILE", command=lambda: self.tenImage.show())
        tenopen_button.place(x=170, y=345)

        tenchoose_button = ttk.Button(self, text="CHOOSE NEW FILE", command=lambda: self.tenth_file_dialogue())
        tenchoose_button.place(x=340, y=345)

        # --------------TWELTH MARKSHEET-------------------

        twelth_label = tk.Label(self, text="TWELTH \nMARKSHEET", font=("Verdana", 10))
        twelth_label.place(x=20, y=380, anchor="w")

        twelopen_button = ttk.Button(self, text="OPEN FILE", command=lambda: self.twelImage.show())
        twelopen_button.place(x=170, y=380)

        twelchoose_button = ttk.Button(self, text="CHOOSE NEW FILE", command=lambda: self.twelth_file_dialogue())
        twelchoose_button.place(x=340, y=380)

        # --------------UPDATE BUTTON------------------------

        update_button = tk.Button(self, text="UPDATE", width=20, fg="red", command=lambda: self.check_all_fill())
        update_button.place(x=20, y=420)

        # --------------DELETE-------------------------------------

        def delete():
            email = self.email1_entry.get()
            self.clear_all()
            delete_from_student_db(email)

        delete_button = tk.Button(self, text="DELETE", width=20, fg="red", command=lambda: delete())
        delete_button.place(x=200, y=420)

        # -------------CLEAR ALL---------------------------------

        clear_button = tk.Button(self, text="CLEAR ALL", width=10, fg="red", command=lambda: self.clear_all())
        clear_button.place(x=400, y=420)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(StudentInfo))
        back_button.place(x=220, y=450)


class AdminForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="NOT SUPPORTED YET", font=10)
        label.pack()
        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(AdminInfo))
        back_button.place(x=220, y=450)


class AdminUpdate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="NOT SUPPORTED YET", font=10)
        label.pack()
        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(AdminInfo))
        back_button.place(x=220, y=450)


# --------------------------------------------------------------------------------------------------------------
# -------------------------------------------AFTER EMPLOYEE LOGIN---------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------


class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="EMPLOYEE PAGE AFTER LOGIN", font=10)
        label.pack()

        button1 = tk.Button(self, text="ADD NEW STUDENT", height=5, width=20,
                            command=lambda: controller.show_frame(StudentForm))
        button1.place(x=170, y=100)
        button2 = tk.Button(self, text="EDIT AN STUDENT", height=5, width=20,
                            command=lambda: controller.show_frame(StudentUpdate))
        button2.place(x=170, y=200)

        back_button = tk.Button(self, text="back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=220, y=450)

app = MyApp()
app.geometry("500x500+500+100")
app.mainloop()

