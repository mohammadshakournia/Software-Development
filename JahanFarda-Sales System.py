from tkinter import *
import pyodbc
import tkinter.messagebox
from tkinter import ttk
import time


############################################## Align registration_frame Frame to Center ################################################
def center_window(frame, w=500, h=200):
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    frame.geometry('%dx%d+%d+%d' % (w, h, x, y))


############################################## DataBase to Treeview ################################################
def CheckDB_Exist(dbname):
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Trusted_Connection=yes;')
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    cursor.execute("SELECT name FROM master.dbo.sysdatabases where name = '"+str(dbname)+"'")
    rows = cursor.fetchall()
    for row in rows:
        if not row == []:
            break
        else:
            create_DB(dbname)
    cnxn.close()


def create_DB(name):
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    cursor.execute("create database " + str(name))
    cnxn.close()

CheckDB_Exist('Sales_System')

def create_Table_1(tname):
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cnxn.autocommit = True
    cursor.execute(
        "Create table " + str(
            tname) + "(pname nvarchar(50),pprice nvarchar(50),pcode nvarchar(50),pcost nvarchar(50),pcount nvarchar(50))")

    cnxn.close()

def create_Table_Sale():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cnxn.autocommit = True
    cursor.execute(
        "Create table Sale(cname nvarchar(50),pname nvarchar(50),pcost nvarchar(50),pcount nvarchar(50),discount nvarchar(50),totalprice nvarchar(50),Date navrchar(50))")

    cnxn.close()

    


cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Trusted_Connection=yes;')
cnxn.autocommit = True
cursor = cnxn.cursor()
cursor.execute("select * from Sales_System.sys.tables where name = 'Tabel_1'")
rows = cursor.fetchall()
for row in rows:
    if not row == []:
        break
    else:
        create_Table_1(Tabel_1)
cnxn.close()

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Trusted_Connection=yes;')
cnxn.autocommit = True
cursor = cnxn.cursor()
cursor.execute("select * from Sales_System.sys.tables where name = 'sale'")
rows = cursor.fetchall()
for row in rows:
    if not row == []:
        break
    else:
        create_Table_Sale()
cnxn.close()


def Read_btnFunction(query):
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        part1, part2, part3, part4, part5 = row
        # print('{} - {}'.format(part1, part2))

        tree.insert("", END, values=(part1, part2, part3, part4, part5))

    cnxn.close()


def Search_btnFunction():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    s = si.get()
    if s == "":
        delete()
        Read_btnFunction("select * from Sales_System.dbo.Tabel_1")
    else:
        cursor.execute("SELECT * FROM Sales_System.dbo.Tabel_1 WHERE pname like N'%" + str(s) + "%'")
        rows = cursor.fetchall()
        if rows == []:
            tkinter.messagebox.showerror(title='جستجو', message='کالایی با این مشخصات پیدا نشد')
        else:
            delete()

            for row in rows:
                part1, part2, part3, part4, part5 = row
                # print('{} - {}'.format(part1, part2))
                tree.insert("", END, values=(part1, part2, part3, part4, part5))

    cnxn.close()
    search_input.delete(0, END)
    delete_input.delete(0, END)


def Insert_btnFunction():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    name = n.get()
    price = p.get()
    code = c.get()
    cost = co.get()
    count = cu.get()
    if name == "" or price == "" or code == "" or cost == "" or count == "":
        tkinter.messagebox.showwarning('خطا', 'لطفا فیلدهای مربوطه را پر کنید')
    else:
        cursor.execute('INSERT INTO Tabel_1(pname,pprice,pcode,pcost,pcount) VALUES (?,?,?,?,?)',
                       (str(name), str(price), str(code), str(cost), str(count)))
        cnxn.commit()
        tkinter.messagebox.showinfo('ثبت کالا', 'ثبت کالا با موفقیت انجام شد')
    delete()
    Read_btnFunction("SELECT * FROM Sales_System.dbo.Tabel_1")


def Delete_Function():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    d = de.get()
    cursor.execute("delete FROM Sales_System.dbo.Tabel_1 WHERE pname = N'" + str(d) + "'")
    result = tkinter.messagebox.askquestion("حذف کالا", "آیا برای حذف کالا < " + str(d) + " > مطمئن هستید؟",
                                            icon='warning')
    if result == 'yes':
        cnxn.commit()
        tkinter.messagebox.showinfo('حذف کالا', 'حذف کالا با موفقیت انجام شد')
        delete_input.delete(0, END)

    delete()
    Read_btnFunction("SELECT * FROM Sales_System.dbo.Tabel_1")


def Edit_btnFunction():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost;'
                          'Database=Sales_System;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    s = si.get()
    e = ed.get()
    price = ep.get()
    code = ec.get()
    cost = eco.get()
    count = ecu.get()

    cursor.execute("update Sales_System.dbo.Tabel_1 set pname = N'" + str(e) + "' , pprice='" + str(
        price) + "' ,pcode='" + str(code) + "' , pcost='" + str(cost) + "' , pcount='" + str(
        count) + "' where pname=N'" + str(s) + "'")

    cnxn.commit()
    tkinter.messagebox.showinfo('ویرایش کالا', 'ویرایش کالا با موفقیت انجام شد')
    delete()
    Read_btnFunction("SELECT * FROM Sales_System.dbo.Tabel_1")
    search_input.delete(0, END)
    delete_input.delete(0, END)
    edit_input.delete(0, END)
    eprice_input.delete(0, END)
    ecode_input.delete(0, END)
    ecost_input.delete(0, END)
    ecount_input.delete(0, END)


def txtMoney_Format(entry, text):
    digits = str(text)
    length = len(digits)
    if length <= 6:
        entry.set('{},{}'.format(digits[0:length - 3], digits[length - 3:length]))
    elif length <= 9:
        entry.set('{},{},{}'.format(digits[0:length - 6], digits[length - 6:length - 3], digits[length - 3:length]))
    elif length <= 12:
        entry.set(
            '{},{},{},{}'.format(digits[0:length - 9], digits[length - 9:length - 6], digits[length - 6:length - 3],
                                 digits[length - 3:length]))


############################################## Delete Treeview List ################################################

def delete():
    for i in tree.get_children():
        tree.delete(i)


############################################## Select and get a cell from Treeview List ################################################

def selectItem(event):
    curItem = tree.item(tree.focus())
    col = tree.identify_column(event.x)

    if col == '#0':
        cell_value = curItem['values']
    elif col == '#1':
        cell_value1 = curItem['values'][0]
        cell_value2 = curItem['values'][1]
        cell_value3 = curItem['values'][2]
        cell_value4 = curItem['values'][3]
        cell_value5 = curItem['values'][4]
    elif col == '#2':
        cell_value1 = curItem['values'][0]
        cell_value2 = curItem['values'][1]
        cell_value3 = curItem['values'][2]
        cell_value4 = curItem['values'][3]
        cell_value5 = curItem['values'][4]
    elif col == '#3':
        cell_value1 = curItem['values'][0]
        cell_value2 = curItem['values'][1]
        cell_value3 = curItem['values'][2]
        cell_value4 = curItem['values'][3]
        cell_value5 = curItem['values'][4]
    elif col == '#4':
        cell_value1 = curItem['values'][0]
        cell_value2 = curItem['values'][1]
        cell_value3 = curItem['values'][2]
        cell_value4 = curItem['values'][3]
        cell_value5 = curItem['values'][4]
    elif col == '#5':
        cell_value1 = curItem['values'][0]
        cell_value2 = curItem['values'][1]
        cell_value3 = curItem['values'][2]
        cell_value4 = curItem['values'][3]
        cell_value5 = curItem['values'][4]
    search_input.delete(0, END)
    delete_input.delete(0, END)
    edit_input.delete(0, END)
    eprice_input.delete(0, END)
    ecode_input.delete(0, END)
    ecost_input.delete(0, END)
    ecount_input.delete(0, END)
    delete_input.insert(END, cell_value1)
    search_input.insert(END, cell_value1)
    edit_input.insert(END, cell_value1)
    eprice_input.insert(END, cell_value2)
    ecode_input.insert(END, cell_value3)
    ecost_input.insert(END, cell_value4)
    ecount_input.insert(END, cell_value5)


############################################## Create Registration Frame ################################################


registration_frame = Tk()
center_window(registration_frame, 1000, 700)
registration_frame.title("ثبت کالا")
registration_frame.wm_maxsize(width=1000, height=600)

n = StringVar()
pname_input = Entry(registration_frame, width=30, textvariable=n)

p = StringVar()
pprice_input = Entry(registration_frame, width=30, textvariable=p)

c = StringVar()
pcode_input = Entry(registration_frame, width=30, textvariable=c)

co = StringVar()
pcost_input = Entry(registration_frame, width=30, textvariable=co)

cu = StringVar()
pcount_input = Entry(registration_frame, width=30, textvariable=cu)

pname_input.place(x=600, y=40)
pname_lbl = Label(registration_frame, text="نام کالا")
pname_lbl.place(x=800, y=40)

pprice_input.place(x=600, y=70)
pprice_lbl = Label(registration_frame, text="قیمت فروش کالا")
pprice_lbl.place(x=800, y=70)

pcode_input.place(x=600, y=100)
pcode_lbl = Label(registration_frame, text="کد کالا")
pcode_lbl.place(x=800, y=100)

pcost_input.place(x=600, y=130)
pcost_lbl = Label(registration_frame, text="قیمت خرید کالا")
pcost_lbl.place(x=800, y=130)

pcount_input.place(x=600, y=160)
pcount_lbl = Label(registration_frame, text="تعداد موجودی انبار")
pcount_lbl.place(x=800, y=160)

insert_btn = Button(registration_frame, height=6, width=15, text="افزودن کالا", command=Insert_btnFunction)
insert_btn.place(x=470, y=45)

quit_btn = Button(registration_frame, text='خروج', command=registration_frame.destroy)
quit_btn.place(x=30, y=550)

###############################################  Treeview Table  ##############################################

cols = ('نام کالا', 'قیمت فروش', 'کد کالا', 'قیمت خرید', 'تعداد موجودی انبار')
tree = ttk.Treeview(registration_frame, column=cols, show='headings')

for col in cols:
    tree.heading(col, text=col)

tree.grid(row=1, column=0, columnspan=2)
tree.place(x=0, y=300)
Read_btnFunction("SELECT * FROM Sales_System.dbo.Tabel_1")

############################################### Search & Delete ##############################################

si = StringVar()
search_input = Entry(registration_frame, width=30, textvariable=si)
search_input.place(x=120, y=20)

search_btn = Button(registration_frame, text='جستجو', command=Search_btnFunction)
search_btn.place(x=320, y=15)

de = StringVar()
delete_input = Entry(registration_frame, width=30, textvariable=de)
delete_input.place(x=120, y=50)

delete_btn = Button(registration_frame, text='حذف کالا', command=Delete_Function)
delete_btn.place(x=320, y=50)
############################################### Edit ##############################################

ed = StringVar()
edit_input = Entry(registration_frame, width=30, textvariable=ed)
edit_input.place(x=120, y=80)

edit_input_lbl = Label(registration_frame, text='نام کالا')
edit_input_lbl.place(x=32, y=80)

ep = StringVar()
eprice_input = Entry(registration_frame, width=30, textvariable=ep)

ec = StringVar()
ecode_input = Entry(registration_frame, width=30, textvariable=ec)

eco = StringVar()
ecost_input = Entry(registration_frame, width=30, textvariable=eco)

ecu = StringVar()
ecount_input = Entry(registration_frame, width=30, textvariable=ecu)

eprice_input.place(x=120, y=110)
eprice_lbl = Label(registration_frame, text="قیمت فروش کالا")
eprice_lbl.place(x=30, y=110)

ecode_input.place(x=120, y=140)
ecode_lbl = Label(registration_frame, text="کد کالا")
ecode_lbl.place(x=30, y=140)

ecost_input.place(x=120, y=170)
ecost_lbl = Label(registration_frame, text="قیمت خرید کالا")
ecost_lbl.place(x=30, y=170)

ecount_input.place(x=120, y=200)
ecount_lbl = Label(registration_frame, text="تعداد موجودی انبار")
ecount_lbl.place(x=20, y=200)

edit_btn = Button(registration_frame, height=8, text='ویرایش کالا', command=Edit_btnFunction)
edit_btn.place(x=320, y=85)

tree.bind('<ButtonRelease-1>', selectItem)


###############################################  Sale Frame  ##############################################


def sale():
    def Read_tree2():
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                              'Database=Sales_System;'
                              'Trusted_Connection=yes;')
        cursor10 = cnxn.cursor()
        cursor10.execute("SELECT * FROM Sales_System.dbo.Tabel_1")
        rows = cursor10.fetchall()
        for row in rows:
            part1, part2, part3, part4, part5 = row
            # print('{} - {}'.format(part1, part2))
            tree2.insert("", END, values=(part1, part2, part3, part4, part5))

        cnxn.close()

    def selectItem(event):
        curItem = tree2.item(tree2.focus())
        col = tree2.identify_column(event.x)

        if col == '#0':
            cell_value = curItem['values']
        elif col == '#1':
            cell_value2 = curItem['values'][0]
            cell_value3 = curItem['values'][1]
            cell_value = curItem['values'][4]
        elif col == '#2':
            cell_value2 = curItem['values'][0]
            cell_value3 = curItem['values'][1]
            cell_value = curItem['values'][4]
        elif col == '#3':
            cell_value2 = curItem['values'][0]
            cell_value3 = curItem['values'][1]
            cell_value = curItem['values'][4]
        elif col == '#4':
            cell_value2 = curItem['values'][0]
            cell_value3 = curItem['values'][1]
            cell_value = curItem['values'][4]
        elif col == '#5':
            cell_value2 = curItem['values'][0]
            cell_value3 = curItem['values'][1]
            cell_value = curItem['values'][4]
        produce_count.delete(0, END)
        produce_name.delete(0, END)
        produce_cost.delete(0, END)
        total_cost.delete(0, END)
        produce_count.insert(END, cell_value)
        produce_name.insert(END, cell_value2)
        produce_cost.insert(END, cell_value3)
        txtMoney_Format(tc, cell_value3)

    # total_cost.insert(END, cell_value3)
    def delete_tree2():
        for i in tree2.get_children():
            tree2.delete(i)

    def Saling():
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                              'Database=Sales_System;'
                              'Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        cursor2 = cnxn.cursor()

        name = cn.get()
        pname = pn.get()
        cost = pc.get()
        count = cc.get()
        count2 = cc2.get()
        now = time.strftime('%Y/%m/%d %H:%M:%S')

        dis = dc.get()
        total = tc.get()
        Sale_frame.attributes("-topmost", True)

        if name == "" or pname == "" or cost == "" or count == "" or dis == "" or total == "":
            tkinter.messagebox.showwarning('خطا', 'لطفا فیلدهای مربوطه را پر کنید', parent=Sale_frame)
        else:
            if int(count2) < int(count):
                tkinter.messagebox.showwarning('خطا', 'مقدار درخواستی کالا بیشتر از موجودی می باشد.',
                                               parent=Sale_frame)
            else:
                cursor.execute(
                    'INSERT INTO Sale(cname,pname,pcost,pcount,discount,totalprice,Date) VALUES (?,?,?,?,?,?,?)',
                    (str(name), str(pname), str(cost), str(count), str(dis), str(total), str(now)))
                cursor2.execute(
                    "Update Sales_System.dbo.Tabel_1 set pcount=pcount-" + str(count) + " where pname=N'" + str(
                        pname) + "'")
                cnxn.commit()
                tkinter.messagebox.showinfo('فروش کالا', 'فروش کالا با موفقیت انجام شد', parent=Sale_frame)
                delete_tree2()
                Read_tree2()
                delete()
                Read_btnFunction('select * from Sales_System.dbo.Tabel_1  ')

    def OnKeyRelease_Discount(event):
        value = pc.get()
        value2 = discount.get()
        res = int(value) - int(value2)
        total_cost.delete(0, END)
        total_cost.insert(END, res)
        txtMoney_Format(tc, res)

    def OnKeyRelease_Search(event):
        value = search_input.get()
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                              'Database=Sales_System;'
                              'Trusted_Connection=yes;')
        cursor = cnxn.cursor()

        s = si.get()
        if s == "":
            delete_tree2()
            Read_tree2()
        else:
            cursor.execute("SELECT * FROM Sales_System.dbo.Tabel_1 WHERE pname like N'%" + str(value) + "%'")
            rows = cursor.fetchall()
            if rows == []:
                tkinter.messagebox.showerror(title='جستجو', message='کالایی با این مشخصات پیدا نشد')

            else:
                delete_tree2()
                for row in rows:
                    part1, part2, part3, part4, part5 = row
                    # print('{} - {}'.format(part1, part2))
                    tree2.insert("", END, values=(part1, part2, part3, part4, part5))

    ######################################################## Create Sale Frame ##################################
    Sale_frame = Toplevel(registration_frame)
    center_window(Sale_frame, 1000, 700)
    Sale_frame.title("صدور فاکتور فروش")
    Sale_frame.wm_maxsize(width=1000, height=600)

    si = StringVar()
    search_input = Entry(Sale_frame, width=30, textvariable=si)
    search_input.place(x=100, y=50)
    search_input.bind('<KeyRelease>', OnKeyRelease_Search)
    search_lbl = Label(Sale_frame, text="جستجوی کالا")
    search_lbl.place(x=280, y=50)

    cn = StringVar()
    costumer_name = Entry(Sale_frame, width=30, textvariable=cn)
    costumer_name.place(x=600, y=50)

    costumer_name_lbl = Label(Sale_frame, text="نام مشتری")
    costumer_name_lbl.place(x=800, y=50)

    pn = StringVar()
    produce_name = Entry(Sale_frame, width=30, textvariable=pn)
    produce_name.place(x=600, y=80)

    produce_name_lbl = Label(Sale_frame, text="نام کالا")
    produce_name_lbl.place(x=800, y=80)

    pc = StringVar()
    produce_cost = Entry(Sale_frame, width=30, textvariable=pc)
    produce_cost.place(x=600, y=110)

    produce_cost_lbl = Label(Sale_frame, text="فی قیمت کالا")
    produce_cost_lbl.place(x=800, y=110)

    cc = StringVar()
    produce_count2 = Entry(Sale_frame, width=30, textvariable=cc)
    produce_count2.place(x=600, y=140)

    cc2 = StringVar()
    produce_count = Entry(Sale_frame, width=30, textvariable=cc2)
    # produce_count.place(x=600, y=260)

    produce_count_lbl = Label(Sale_frame, text="تعداد")
    produce_count_lbl.place(x=800, y=140)

    dc = StringVar()
    discount = Entry(Sale_frame, width=30, textvariable=dc)
    discount.place(x=600, y=170)

    discount_lbl = Label(Sale_frame, text="تخفیف")
    discount_lbl.place(x=800, y=170)

    tc = StringVar()
    total_cost = Entry(Sale_frame, width=30, textvariable=tc)
    total_cost.place(x=600, y=200)

    total_cost_lbl = Label(Sale_frame, text="قیمت کل")
    total_cost_lbl.place(x=800, y=200)

    sale_btn = Button(Sale_frame, height=6, width=15, text='خرید', command=Saling)
    sale_btn.place(x=450, y=60)

    pcost_input.bind("<KeyRelease>", OnKeyRelease_Discount)
    discount.bind("<KeyRelease>", OnKeyRelease_Discount)
    ######################################################## Create Treeviw for Sale Frame ########################

    cols = ('نام کالا', 'قیمت فروش', 'کد کالا', 'قیمت خرید', 'تعداد موجودی انبار')
    tree2 = ttk.Treeview(Sale_frame, column=cols, show='headings')

    for col in cols:
        tree2.heading(col, text=col)

    tree2.grid(row=1, column=0, columnspan=2)
    tree2.place(x=0, y=300)

    tree2.bind('<ButtonRelease-1>', selectItem)
    Read_tree2()
    ########################################################  ############### ########################

    ###############################################  Sale Frame  ##############################################


def REPORT():
    def Read_REPtree():
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                              'Database=Sales_System;'
                              'Trusted_Connection=yes;')
        cursor10 = cnxn.cursor()
        cursor10.execute("SELECT * FROM Sales_System.dbo.Sale")
        rows = cursor10.fetchall()
        for row in rows:
            part1, part2, part3, part4, part5, part6, part7 = row
            rep_tree.insert("", END, values=(part1, part2, part3, part4, part5, part6, part7))

        cnxn.close()

    # total_cost.insert(END, cell_value3)

    ################################################## Create Sale Frame ##################################
    REPRT_Frame = Toplevel(registration_frame)
    center_window(REPRT_Frame, 1400, 700)
    REPRT_Frame.title("گزارش فروش")

    ######################################################## Create Treeviw for Sale Frame ########################

    cols = ('نام خریدار', 'نام کالا', 'فی قیمت', 'تعداد', 'تخفیف', 'قیمت کل', 'تاریخ')
    rep_tree = ttk.Treeview(REPRT_Frame, column=cols, show='headings', height=100)

    for col in cols:
        rep_tree.heading(col, text=col)

    rep_tree.grid(row=12, column=7, columnspan=7)
    rep_tree.place(x=0, y=50)
    Read_REPtree()
    ########################################################  ############### ########################


menubar = Menu(registration_frame)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="صدور فاکتور", command=sale)
filemenu.add_command(label="گزارش فروش", command=REPORT)

filemenu.add_separator()

filemenu.add_command(label="خروج", command=registration_frame.quit)
menubar.add_cascade(label="فروش", menu=filemenu)

registration_frame.config(menu=menubar)
registration_frame.grid()
registration_frame.mainloop()
