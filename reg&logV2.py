import io
from tkinter import *
import tkinter as tk
import re
from tkinter.ttk import Combobox
from tkinter import ttk
from functools import partial

import Pmw

import db
import bcrypt
import CSV
from PIL import Image, ImageTk
import Imagini


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.screenError = None
        self.dbObject = db.DB()
        self.switch_frame(MainScreen)


    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self.screenError is not None:
            self.screenError.destroy()
        if self._frame is not None:
            self._frame.destroy()
        if frame_class is MainScreen:
            self.geometry("400x350")
        elif frame_class is Register:
            self.geometry("500x450")
        elif frame_class is Login:
            self.geometry("400x300")
        elif frame_class is Shop:
            self.geometry("600x550")
        self._frame = new_frame
        self._frame.pack()

    def generateScreenError(self, text, color):
        if self.screenError is not None:
            self.screenError.destroy()
        self.screenError = Label(self, text=text, fg=color)
        self.screenError.pack()

    def addUserToDB(self, first_name, last_name, email, username, password):

        if not (re.match("([A-Za-z]+)", first_name.get())):
            self.generateScreenError( "Invalid first name", "red")
        elif not (re.match("([A-Za-z]+)", last_name.get())):
            self.generateScreenError( "Invalid last name ", "red")
        elif not (re.match("^[A-Za-z_\-\.]+@([A-Za-z_\-]+\.)+[A-Za-z_\-]{2,4}$", email.get())):
            self.generateScreenError( "Invalid email adress", "red")
        elif not (re.match("[A-Za-z0-9_\-\.]{3,16}", username.get())):
            self.generateScreenError( "Invalid username", "red")
        elif not (re.match("[A-Za-z0-9@#$%^&*]{8,30}", password.get())):
            self.generateScreenError( "Invalid password", "red")
        else:
            try:
                self.dbObject.addAccount(username.get(), self.encrypt(password.get()), first_name.get(),
                                         last_name.get(), email.get())
                self.generateScreenError( "Registration Success", "green")
                first_name.delete(0, END)
                last_name.delete(0, END)
                email.delete(0, END)
                username.delete(0, END)
                password.delete(0, END)

            except:
                self.generateScreenError( "Registration Failed", "red")

    def encrypt(self, password):
        hashed = bcrypt.hashpw(password.encode(encoding="ascii", errors="replace"), bcrypt.gensalt())
        return hashed

    def loginVerify(self, username, password, username_login_entry, password_login_entry):
        username1 = username.get()
        password1 = password.get()

        username_login_entry.delete(0,END)
        password_login_entry.delete(0,END)

        cursor = self.dbObject.getCursorAndCon()[0]
        cursor.execute('select Password from usersInfo where Username=?', (username1,))
        returnedValue = cursor.fetchone()
        if returnedValue is not None and bcrypt.checkpw(password1.encode(encoding="ascii", errors="replace"), returnedValue[0]):
            #self.shop()
            self.switch_frame(Shop)
        else:
            self.generateScreenError( "Login fail", "red")



class MainScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)


        Label(self, text="Welcome to The Drinks Store", bg="grey", width="50", height="3", font=("Calibri", 20)).pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Button(self, text="Register", width="30", height="3", bg="light grey", relief = FLAT, command=lambda: master.switch_frame(Register)).pack()
        Label(self, text="").pack()
        Button(self, text="Login", width="30", height="3", bg="light grey", relief = FLAT, command=lambda: master.switch_frame(Login)).pack()
        Label(self, text="").pack()


class Register(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        first_name = StringVar()
        last_name = StringVar()
        email = StringVar()
        username = StringVar()
        password = StringVar()

        Label(self, text="Enter your details to register", font=("Calibri", 15)).pack()
        Label(self, text="").pack()
        Label(self, text="First name *").pack()
        first_name_entry = Entry(self, textvariable=first_name, relief = FLAT)
        first_name_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Last name *").pack()
        last_name_entry = Entry(self, textvariable=last_name, relief = FLAT)
        last_name_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Email *").pack()
        email_entry = Entry(self, textvariable=email, relief = FLAT)
        email_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Username *").pack()
        username_entry = Entry(self, textvariable=username, relief = FLAT)
        username_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Password *").pack()
        password_entry = Entry(self, textvariable=password, show="*", relief = FLAT)
        password_entry.pack()
        Label(self, text="").pack()
        Label(self, text="").pack()

        buttonFrame = Frame(self)
        buttonFrame.pack()
        Button(buttonFrame, text="Register", width="10", height="2", bg="light grey", relief = FLAT,
               command=lambda: master.addUserToDB(first_name_entry, last_name_entry, email_entry, username_entry,
                                                password_entry)).grid(row = 0, column = 0, padx = 10)
        Button(buttonFrame, text="Back", width="10", height="2", bg="light grey", relief = FLAT,
                                 command=lambda: master.switch_frame(MainScreen)).grid(row = 0, column = 1)


class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        username = StringVar()
        password = StringVar()

        Label(self, text="Enter your details below to login", font=("Calibri", 15)).pack()
        Label(self, text="").pack()
        Label(self, text="Username *").pack()
        username_login_entry = Entry(self, textvariable=username, relief = FLAT)
        username_login_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Password *").pack()
        password_login_entry = Entry(self, textvariable=password, show="*", relief = FLAT)
        password_login_entry.pack()
        Label(self, text="").pack()
        Label(self, text="").pack()

        buttonFrame = Frame(self)
        buttonFrame.pack()
        Button(buttonFrame, text="Login", width="10", height="2", bg="light grey", relief = FLAT,
               command=lambda: master.loginVerify(username, password, username_login_entry,
                                               password_login_entry)).grid(row = 0, column = 0, padx = 10)

        Button(buttonFrame, text="Back", width="10", height="2", bg="light grey", relief = FLAT,
                        command=lambda: master.switch_frame(MainScreen)).grid(row = 0, column = 1)



class Shop(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.bigFrame = None
        self.dbObj = CSV.Produse()
        self.checkoutList = []
        self.total = 0
        self.loadComp()

    def loadComp(self):
        topFrame = Frame(self, background="light grey")
        topFrame.pack()
        Button(topFrame, text="Browse", width="10", height="2", relief=FLAT, bg="light grey",
               command=lambda: self.createBigFrame(0)).pack(side=LEFT, padx=110)
        Button(topFrame, text='Checkout', width="10", height="2", relief=FLAT, bg="light grey",
               command=lambda: self.createBigFrame(1)).pack(side=RIGHT, padx=110)
        self.createBigFrame(0)

    def createBigFrame(self, windowType):
        if self.bigFrame is not None:
            self.bigFrame.destroy()
        self.bigFrame = Frame(self, width = 1000)
        self.bigFrame.pack()

        if windowType == 0:
            self.windowType0()
            #Label(self, text="").pack()
        else:
            #load checkout
            self.windowType1()
            #Label(self.bigFrame, text=" haga").pack()

#window type 0 and left Frame

    def windowType0(self):
        # leftFrame

        self.leftFrame = Frame(self.bigFrame,  width=150, height=600)
        self.leftFrame.grid(row=0, column=0)

        Label(self.leftFrame, text="").pack()
        Label(self.leftFrame, text="Bottle size").pack()
        var1 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="100", variable=var1).pack()
        var2 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="200", variable=var2).pack()
        var3 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="375", variable=var3).pack()
        var4 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="500", variable=var4).pack()
        var5 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="750", variable=var5).pack()
        var6 = IntVar()
        ttk.Checkbutton(self.leftFrame, text="1000", variable=var6).pack()

        cursor = self.dbObj.getCursorAndCon()[0]
        cursor.execute('select DISTINCT category_name from Produse')
        returnedValue = cursor.fetchall()
        Label(self.leftFrame, text="").pack()
        Label(self.leftFrame, text="Category").pack()
        n = tk.StringVar()
        category = Combobox(self.leftFrame, width=20, textvariable=n)
        category['values'] = returnedValue
        category.pack()

        Label(self.leftFrame, text="").pack()
        Button(self.leftFrame, text = "Apply", width="10", height="2", relief=FLAT, bg="light grey", command = lambda: self.prepareStatement()).pack()

        self.createRightFrame((), '')

    def prepareStatement(self):
        checkboxValues = []
        checkboxes = self.leftFrame.winfo_children()[2:8]
        for checkbox in checkboxes:
            if checkbox.instate(['selected']):
                checkboxValues.append(checkbox.cget("text"))
        category = self.leftFrame.winfo_children()[-3].get()

        self.createRightFrame(tuple(checkboxValues), category)

#right Frame

    def createRightFrame(self, checkboxValues, category):

        self.rightFrame = Frame(self.bigFrame, width = 450, height = 600)
        self.rightFrame.grid(row=0, column=1)


        self.sframe = Pmw.ScrolledFrame(self.rightFrame, usehullsize=1, hull_width=450, hull_height=400,
                                   horizflex="elastic", borderframe=0)
        self.sframe.grid(row=0, column=0)

        cursor = self.dbObj.getCursorAndCon()[0]

        if len(checkboxValues) == 0 and len(category) == 0:
            query = 'select * from Produs P inner join Imagini I on P.image_id = I.id order by random() limit 20'
            cursor.execute(query)
        elif len(checkboxValues) == 0:
            query = 'select * from Produs P inner join Imagini I on P.image_id = I.id where category_name = ? order by random() limit 20'
            cursor.execute(query, (category,))
        elif len(category) == 0:
            conditions = list()
            for val in checkboxValues:
                conditions.append('bottle_size = ' + val)
            finalCondition = ' or '.join(conditions)

            query = 'select * from Produs P inner join Imagini I on P.image_id = I.id where '+finalCondition + ' order by random() limit 20'
            cursor.execute(query)
        else:
            conditions = list()
            for val in checkboxValues:
                conditions.append('bottle_size = ' + val)
            finalCondition = ' or '.join(conditions)
            query = 'select * from Produs P inner join Imagini I on P.image_id = I.id where category_name = ? and '+finalCondition + ' order by random() limit 20'
            cursor.execute(query, (category,))

        for produs in cursor:
            self.creareFrame()
            self.imageFrame = Frame(self.productFrame, width=100, height=100)
            self.imageFrame.grid(row=0, column=0)
            self.textFrame = Frame(self.productFrame, width=300, height=100)
            self.textFrame.grid(row=0, column=1)
            self.addProduse(produs)


    def addProduse(self, produs):
        Label(self.textFrame, text="Category: ").grid(row=0, column=0)
        clabel = Label(self.textFrame, text = produs[2])
        clabel.grid(row=0, column=1)
        Label(self.textFrame, text="Name: ").grid(row=1, column=0)
        nlabel = Label(self.textFrame, text=produs[3])
        nlabel.grid(row=1, column=1)
        Label(self.textFrame, text="Bottle size: ").grid(row=2, column=0)
        blabel = Label(self.textFrame, text=produs[5])
        blabel.grid(row=2,column=1)
        Label(self.textFrame, text="Price: ").grid(row=3, column=0)
        plabel = Label(self.textFrame, text=str(int(produs[6])))
        plabel.grid(row=3, column=1)
        idlabel = Label(self.textFrame, text=produs[0], fg="white")
        idlabel.grid(row=0, column=2)
        Button(self.textFrame, text="Add", width="5", height="1", relief=FLAT, bg="light grey",
               command = lambda: [self.checkoutList.append(idlabel.cget("text")), self.totalPrice(plabel)]).grid(row=4, column=0, sticky = E)
        Label(self.textFrame, text="-------------------------------------------", fg = "white").grid(row=2, column=4)


        image = Image.open(io.BytesIO(produs[8]))
        image = image.resize((100, 100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)

        img = Label(self.imageFrame, image=render)
        img.image = render
        img.place(x=0, y=0)


    def creareFrame(self):
        self.productFrame = Frame(self.sframe.interior(), width = 450, height = 100)
        self.productFrame.pack()

#window type 1

    def windowType1(self):
        cursor = self.dbObj.getCursorAndCon()[0]
        list = []
        dict = {}
        for elem in self.checkoutList:
            cursor.execute('select category_name, item_description, bottle_size, bottle_price from Produs P where P.id = ?', (elem,))
            list.append(cursor.fetchone())

        self.checkoutFrame = Pmw.ScrolledFrame(self.bigFrame, usehullsize=1, hull_width=600, hull_height=400,
                                        horizflex="elastic", borderframe=0)
        self.checkoutFrame.grid(row=0, column=0)

        for elem in list:
            if elem in dict:
                dict[elem] += 1
            else:
                dict[elem] = 1

        totalLabel = Label(self.bigFrame, text="Total: $" + str(self.total))

        for elem in dict:
            elemFrame = Frame(self.checkoutFrame.interior(), width=600, height=150)
            elemFrame.pack(pady = 10)
            Label(elemFrame, text="Category: ").grid(row = 0, column = 0)
            Label(elemFrame, text= elem[0]).grid(row=0, column=1)
            Label(elemFrame, text="Name: ").grid(row=1, column=0)
            Label(elemFrame, text=elem[1]).grid(row=1, column=1)
            Label(elemFrame, text="Bottle size: ").grid(row=2, column=0)
            Label(elemFrame, text=elem[2]).grid(row=2, column=1)
            Label(elemFrame, text="Bottle price: ").grid(row=3, column=0)
            plabel = Label(elemFrame, text=str(int(elem[3])))
            plabel.grid(row=3, column=1)
            Label(elemFrame, text="Amount: ").grid(row=4, column=0)
            alabel = Label(elemFrame, text=dict[elem])
            alabel.grid(row=4, column = 1)
            Button(elemFrame, text="Delete", width="5", height="1", relief=FLAT, bg="light grey",
                   command = partial(self.deleteProdus, alabel, elemFrame, plabel, totalLabel)).grid(row=5, column = 0)


        totalLabel.grid(row=1, column=0)
        self.cbutton =Button(self.bigFrame, text="Checkout", width="10", height="1", relief=FLAT, bg="light grey",
               command = self.checkout)
        self.cbutton.grid(row=2, column=0)

    def deleteProdus(self, param, frame, label, label2):
        self.total -= int(label.cget("text"))
        label2.config(text="Total: $"+ str(self.total))
        if param.cget("text") > 1:
            param.config(text= int(param.cget("text") - 1))
        elif param.cget("text") == 1:
            frame.destroy()


    def totalPrice(self, p):
        self.total += int(p.cget("text"))

    def checkout(self):
        self.checkoutFrame.destroy()
        self.cbutton.destroy()
        Label(self.bigFrame, text = "Thank you for shopping with us", width="50", height="3", font=("Calibri", 20)).grid(row=0, column=0)
        self.total = 0
        self.checkoutList = []



if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.mainloop()