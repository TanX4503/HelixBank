# Importing required Modules
import customtkinter as ctk # Importing the Custom Tkinter Module
import tkinter
from CTkMessagebox import CTkMessagebox # Importing the Custom Tkinter Message Box Module
from PIL import Image # Pillow Module used for images in tkinter
import os
import mysql.connector
import pickle
import datetime

# Connecting to AIVEN DigitalOcean MySQL Server
f=open('C:\\HelixTempFiles\\HelixTemp.dat','rb')
mybase=pickle.load(f)
mydb = mysql.connector.connect(host=mybase['host'],port=mybase['port'],user=mybase['user'], password=mybase['password'],database=mybase['database'])
mycursor=mydb.cursor(buffered=True) # Without buffered=True, there is an error occuring on opening different apps at one login instance.
os.chdir(mybase['cwd'])
f.close()

# Bank Deposit Function
def deposit():
    f=open('assets\\temp.dat','rb')
    empdata=pickle.load(f)
    f.close()

    # Confirming and Registering Transaction
    def confirmation():
        # Getting Ready for Transaction Confirmation
        accid=ClientVar1.get()
        accname=ClientVar0.get()
        ammount=float(Ammount.get())
        mycursor.execute("select accountid from AccountData;")
        acclist=mycursor.fetchall()
        exists0=False
        for i in acclist:
            if i[0]==accid:
                exists0=True
                break
        
        # Transaction Registration (Step-3)
        def register_transaction():
            try:
                now=datetime.datetime.now()
                daystamp=now.strftime("%y%m%d.%H:%M:%S")
                transid=daystamp+"CASH"+accid[6:]+"X"
                departure=mydata[0][5]+ammount
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;") # Needed as otherwise we wouldnt be able to change the balance values since their tables have foreign key constraints
                mycursor.execute("update AccountData set currentbal="+str(departure)+" where accountid='"+accid+"';")
                mycursor.execute("insert into TransactionHistory values('"+transid+"','"+accid+"','"+accid+"',"+str(ammount)+",'"+"Cash Deposit by "+empdata[0][0][6:]+"');")
                mydb.commit()
                CTkMessagebox(message="The Cash Deposit request for "+accname+" ("+accid+") of Rs."+str(ammount)+"/- raised by agent, "+empdata[0][1]+" "+empdata[0][2]+" ("+empdata[0][0]+") "+"has been recieved by our servers, kindly press the button below to finish the transaction.\nThank you for working with Helix Banks.",icon="check",title="Transaction Recieved",option_1='Thanks')
            except:
                mydb.rollback()
                CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")
            finally:
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                mydb.commit()
        
        # Transaction Confirmation (Step-2)
        try:
            if exists0==True:
                mycursor.execute("select * from AccountData natural join ClientData where accountid = '"+accid+"';")
                mydata=mycursor.fetchall()
                mycursor.execute("select clientid,accountid from AccountData where accountid='"+accid+"';")
                details=mycursor.fetchall()
                if accname!="" and ammount!="":
                    try:
                        ammount=float(ammount)
                    except ValueError:
                        CTkMessagebox(message="Amount must be a number!",icon="warning",title="Error")
                    clientid=details[0][0]
                    mycursor.execute("select * from Login where userid='"+clientid+"';")
                    logininfo=mycursor.fetchall()
                    if accname==mydata[0][6]+" "+mydata[0][7]:
                        currentammount=mydata[0][5]
                        register_transaction()
                    else:
                        CTkMessagebox(message="Kindly enter valid credentials!",icon="cancel",title="Error")

                else:
                    CTkMessagebox(message="No fields except Notes can be blank.",icon="info",title="Info")
            else:
                CTkMessagebox(message="Account does not Exist!",icon="cancel",title="Error")
        except:
            CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")

    # Bank Deposit Console to enter information (Step-1)
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")
    app=ctk.CTkToplevel()
    app.geometry("375x630")
    app.resizable(False,False)
    app.title("Cash Transaction Management")
    app.grid_columnconfigure(0,weight=1)
    app.grid_columnconfigure(1,weight=1)

    myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
    imglabel=ctk.CTkLabel(app,text="",image=myimg)
    imglabel.grid(row=0,columnspan=2)
    title=ctk.CTkLabel(app,text="CASH DEPOSIT",font=('Courier',30))
    title.grid(row=1,columnspan=2,pady=20)

    label1=ctk.CTkLabel(app,text="AccountID of Client:")
    label1.grid(row=2,column=0)
    ClientVar1=ctk.StringVar()
    entry0=ctk.CTkEntry(app,textvariable=ClientVar1)
    entry0.grid(row=2,column=1,pady=2)

    label3=ctk.CTkLabel(app,text="Name of Client:")
    label3.grid(row=3,column=0,pady=2)
    ClientVar0=ctk.StringVar()
    entry1=ctk.CTkEntry(app,textvariable=ClientVar0)
    entry1.grid(row=3,column=1,pady=2)

    label4=ctk.CTkLabel(app,text="AccountID of Agent:",pady=2)
    label4.grid(row=4,column=0)
    data1=ctk.CTkLabel(app,text=empdata[0][0])
    data1.grid(row=4,column=1,pady=2)

    label5=ctk.CTkLabel(app,text="Name of Agent:",pady=2)
    label5.grid(row=5,column=0)
    data2=ctk.CTkLabel(app,text=empdata[0][1]+" "+empdata[0][2])
    data2.grid(row=5,column=1,pady=2)

    label6=ctk.CTkLabel(app,text="Amount to be Deposited:",pady=2)
    label6.grid(row=6,column=0)
    Ammount=ctk.StringVar()
    entry2=ctk.CTkEntry(app,textvariable=Ammount)
    entry2.grid(row=6,column=1,pady=2)

    button=ctk.CTkButton(app,text="Confirm Transaction",command=confirmation)
    button.grid(row=7,columnspan=2,padx=20,pady=20)

    app.mainloop()

# Bank Withdrawl
def withdraw():
    f=open('assets\\temp.dat','rb')
    empdata=pickle.load(f)
    f.close()

    # Confirming and Registering Transaction
    def confirmation():
        # Getting ready to register transaction
        accid=ClientVar1.get()
        accname=ClientVar0.get()
        ammount=float(Ammount.get())
        mycursor.execute("select accountid from AccountData;")
        acclist=mycursor.fetchall()
        exists0=False
        for i in acclist:
            if i[0]==accid:
                exists0=True
                break
        
        # Registering Transaction (Step-3)
        def registertransaction():
            try:
                now=datetime.datetime.now()
                daystamp=now.strftime("%y%m%d.%H:%M:%S")
                transid=daystamp+accid[6:]+"CASHX"
                departure=mydata[0][5]-ammount
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;") # Needed as otherwise we wouldnt be able to change the balance values since their tables have foreign key constraints
                mycursor.execute("update AccountData set currentbal="+str(departure)+" where accountid='"+accid+"';")
                mycursor.execute("insert into TransactionHistory values('"+transid+"','"+accid+"','"+accid+"',"+str(ammount)+",'"+"Cash Withdrawl by "+empdata[0][0][6:]+"');")
                mydb.commit()
                CTkMessagebox(message="The Cash Withdrawl request for "+accname+" ("+accid+") of Rs."+str(ammount)+"/- raised by our agent, "+empdata[0][1]+" "+empdata[0][2]+" ("+empdata[0][0]+") "+"has been recieved by our servers, kindly press the button upon recieving your cash.\nThank you for working with Helix Banks.",icon="check",title="Transaction Recieved",option_1='Thanks')
            except:
                mydb.rollback()
                CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")
            finally:
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                mydb.commit()

        # Confirming Transaction (Step-2)
        try:
            if exists0==True:
                mycursor.execute("select * from AccountData natural join ClientData where accountid = '"+accid+"';")
                mydata=mycursor.fetchall()
                mycursor.execute("select clientid,accountid from AccountData where accountid='"+accid+"';")
                details=mycursor.fetchall()
                if accname!="" and ammount!="":
                    try:
                        ammount=float(ammount)
                    except ValueError:
                        CTkMessagebox(message="Amount must be a number!",icon="warning",title="Error")
                    clientid=details[0][0]
                    mycursor.execute("select * from Login where userid='"+clientid+"';")
                    logininfo=mycursor.fetchall()
                    if accname==mydata[0][6]+" "+mydata[0][7]:
                        currentammount=mydata[0][5]
                        if currentammount-ammount>5000:
                            registertransaction()
                        else:
                            CTkMessagebox(message="Insufficient Funds!",icon="warning",title="Insufficient Funds")
                    else:
                        CTkMessagebox(message="Kindly enter valid credentials!",icon="cancel",title="Error")

                else:
                    CTkMessagebox(message="No fields except Notes can be blank.",icon="info",title="Info")
            else:
                CTkMessagebox(message="Account does not Exist!",icon="cancel",title="Error")
        except:
            CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")

    # Bank Withdrawl Console to enter information (Step-1)
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")
    app=ctk.CTkToplevel()
    app.geometry("375x630")
    app.resizable(False,False)
    app.title("Cash Transaction Management")
    app.grid_columnconfigure(0,weight=1)
    app.grid_columnconfigure(1,weight=1)

    myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
    imglabel=ctk.CTkLabel(app,text="",image=myimg)
    imglabel.grid(row=0,columnspan=2)
    title=ctk.CTkLabel(app,text="CASH WITHDRAWL",font=('Courier',30))
    title.grid(row=1,columnspan=2,pady=20)

    label1=ctk.CTkLabel(app,text="AccountID of Client:")
    label1.grid(row=2,column=0)
    ClientVar1=ctk.StringVar()
    entry0=ctk.CTkEntry(app,textvariable=ClientVar1)
    entry0.grid(row=2,column=1,pady=2)

    label3=ctk.CTkLabel(app,text="Name of Client:")
    label3.grid(row=3,column=0,pady=2)
    ClientVar0=ctk.StringVar()
    entry1=ctk.CTkEntry(app,textvariable=ClientVar0)
    entry1.grid(row=3,column=1,pady=2)

    label4=ctk.CTkLabel(app,text="AccountID of Agent:",pady=2)
    label4.grid(row=4,column=0)
    data1=ctk.CTkLabel(app,text=empdata[0][0])
    data1.grid(row=4,column=1,pady=2)

    label5=ctk.CTkLabel(app,text="Name of Agent:",pady=2)
    label5.grid(row=5,column=0)
    data2=ctk.CTkLabel(app,text=empdata[0][1]+" "+empdata[0][2])
    data2.grid(row=5,column=1,pady=2)

    label6=ctk.CTkLabel(app,text="Amount to be Withdrawn:",pady=2)
    label6.grid(row=6,column=0)
    Ammount=ctk.StringVar()
    entry2=ctk.CTkEntry(app,textvariable=Ammount)
    entry2.grid(row=6,column=1,pady=2)

    button=ctk.CTkButton(app,text="Confirm Transaction",command=confirmation)
    button.grid(row=7,columnspan=2,padx=20,pady=20)

    app.mainloop()

# Transaction Gateway same as the client.py version with slight modifications
def transaction():
    def pay():
        debitfrom=DebitFrom.get()
        mycursor.execute("select accountid from AccountData;")
        acclist=mycursor.fetchall()
        exists0=False
        for i in acclist:
            if i[0]==debitfrom:
                exists0=True
                break

        def register_transaction(data):
            try:
                # Transaction ID Creation
                now=datetime.datetime.now()
                daystamp=now.strftime("%y%m%d.%H:%M:%S")
                transid=daystamp+data[0][6:]+data[1][6:]
                if data[4]==0:
                    transid+="C"
                elif data[4]==1:
                    transid+="S"

                # Changing Current Account Balance
                departure=mydata[0][5]-data[2]
                mycursor.execute("select * from AccountData where accountid='"+data[1]+"';")
                yourdata=mycursor.fetchall()
                if towhere==0:
                    arrival=yourdata[0][5]+data[2]
                elif towhere==1:
                    arrival=yourdata[0][3]+data[2]
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;") # Needed as otherwise we wouldnt be able to change the balance values since their tables have foreign key constraints
                mycursor.execute("update AccountData set currentbal="+str(departure)+" where accountid='"+data[0]+"';")
                if towhere==0:
                    mycursor.execute("update AccountData set currentbal="+str(arrival)+" where accountid='"+data[1]+"';")
                elif towhere==1:
                    mycursor.execute("update AccountData set savingsbal="+str(arrival)+" where accountid='"+data[1]+"';")

                # Transaction Registration
                mycursor.execute("insert into TransactionHistory values('"+transid+"','"+data[0]+"','"+data[1]+"',"+str(data[2])+",'"+data[3]+"');")
                mydb.commit()
                CTkMessagebox(message="Transaction Successful. TransactionID="+transid,icon="check", option_1="Thanks",title="Payment Successful")

            except:
                mydb.rollback()
                CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")
            
            finally:
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                mydb.commit()
        try:
            if exists0==True:
                mycursor.execute("select * from AccountData where accountid = '"+debitfrom+"';")
                mydata=mycursor.fetchall()
                mycursor.execute("select clientid,accountid from ClientData natural join AccountData where accountid='"+debitfrom+"';")
                details=mycursor.fetchall()
                clientid=details[0][0]
                debitto=DebitTo.get()
                ammount=Ammount.get()
                notes=Notes.get()
                towhere=radio_var.get()
                if debitto!="" and ammount!="":
                    try:
                        ammount=float(ammount)
                    except ValueError:
                        CTkMessagebox(message="Amount must be a number!",icon="warning",title="Error")
                    mycursor.execute("select * from Login where userid='"+clientid+"';")
                    logininfo=mycursor.fetchall()
                    if True:
                        exists=False
                        for i in acclist:
                            if i[0]==debitto:
                                exists=True
                                break
                        if exists==True:
                            currentammount=mydata[0][5]
                            if currentammount-ammount>5000:
                                transactiondata=[debitfrom,debitto,ammount,notes,towhere]
                                if towhere==0 and debitfrom==debitto:
                                    CTkMessagebox(message="You cannot send yourself money!",icon="cancel",title="Not Allowed")
                                else:
                                    register_transaction(transactiondata)
                            else:
                                CTkMessagebox(message="Insufficient Funds!",icon="warning",title="Insufficient Funds")
                        else:
                            CTkMessagebox(message="Account does not exist!",icon="warning",title="Error")
                else:
                    CTkMessagebox(message="No fields except Notes can be blank.",icon="info",title="Info")
            else:
                CTkMessagebox(message="Account does not exist!",icon="warning",title="Error")
        except:
            CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")

    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")
    app=ctk.CTkToplevel()
    app.geometry("375x630")
    app.resizable(False,False)
    app.title("Helix Payment Gateway")
    app.grid_columnconfigure(0,weight=1)
    app.grid_columnconfigure(1,weight=1)

    myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
    imglabel=ctk.CTkLabel(app,text="",image=myimg)
    imglabel.grid(row=0,columnspan=2)
    title=ctk.CTkLabel(app,text="PAYMENT GATEWAY",font=('Courier',30))
    title.grid(row=1,columnspan=2,pady=20)

    label1=ctk.CTkLabel(app,text="Transactioning Account:")
    label1.grid(row=2,column=0)
    DebitFrom=ctk.StringVar()
    entry0=ctk.CTkEntry(app,textvariable=DebitFrom)
    entry0.grid(row=2,column=1,pady=2)

    label3=ctk.CTkLabel(app,text="Beneficiary Account:")
    label3.grid(row=3,column=0,pady=2)
    DebitTo=ctk.StringVar()
    entry1=ctk.CTkEntry(app,textvariable=DebitTo)
    entry1.grid(row=3,column=1,pady=2)

    label4=ctk.CTkLabel(app,text="Amount:",pady=2)
    label4.grid(row=4,column=0)
    Ammount=ctk.StringVar()
    entry2=ctk.CTkEntry(app,textvariable=Ammount)
    entry2.grid(row=4,column=1,pady=2)

    label5=ctk.CTkLabel(app,text="Notes:",pady=2)
    label5.grid(row=5,column=0)
    Notes=ctk.StringVar()
    entry3=ctk.CTkEntry(app,textvariable=Notes)
    entry3.grid(row=5,column=1,pady=2)

    radio_var = tkinter.IntVar(value=0)
    radiobutton_1 = ctk.CTkRadioButton(master=app, text="Pay to Current A/C",variable=radio_var, value=0)
    radiobutton_2 = ctk.CTkRadioButton(master=app, text="Pay to Savings A/C",variable=radio_var, value=1)
    radiobutton_1.grid(row=6,columnspan=2,pady=5)
    radiobutton_2.grid(row=7,columnspan=2,pady=5)

    button=ctk.CTkButton(app,text="Confirm Transaction",command=pay)
    button.grid(row=8,columnspan=2,padx=20,pady=20)

    app.mainloop()

# Main Employee Console
def Emp(empid,name):
    # Starting the CTk Application
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")
    capp=ctk.CTk()
    capp.geometry("800x500")
    capp.resizable(False,False)
    capp.title("Helix Bank Management")
    capp.wm_iconbitmap("assets\\favicon.ico")

    mycursor.execute("select * from EmployeeData where empid='"+empid+"';")
    empdata=mycursor.fetchall()
    f=open('assets\\temp.dat','wb')
    pickle.dump(empdata,f)
    f.close()

    capp.grid_columnconfigure(0,weight=1)
    capp.grid_columnconfigure(1,weight=1)
    capp.grid_columnconfigure(2,weight=1)
    capp.grid_columnconfigure(3,weight=1)
    capp.grid_columnconfigure(4,weight=1)
    capp.grid_columnconfigure(5,weight=1)

    myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
    imglabel=ctk.CTkLabel(capp,text="",image=myimg)
    imglabel.grid(row=0,columnspan=3)
    money=ctk.CTkLabel(capp,text="Employee ID: "+empdata[0][0]+"\nDepartment: "+empdata[0][3]+"\nDesignation: "+empdata[0][4]+"\nPhone: "+str(empdata[0][5])+"   "+str(empdata[0][6]),font=('Arial',14))
    money.grid(row=0,column=3,columnspan=3)

    title=ctk.CTkLabel(capp,text="Welcome to Helix Bank,",font=('Courier',30))
    nametitle=ctk.CTkLabel(capp,text=name,font=('Cascadia Code',30))
    title.grid(row=1,columnspan=6,pady=0)
    nametitle.grid(row=2,columnspan=6,pady=0)
    button1=ctk.CTkButton(capp,text="Payment Gateway",command=transaction)
    button1.grid(row=3,column=0,columnspan=2,padx=20,pady=40)
    button2=ctk.CTkButton(capp,text="Deposit Money",command=deposit)
    button2.grid(row=3,column=2,columnspan=2,padx=20,pady=20)
    button3=ctk.CTkButton(capp,text="Withdraw Cash",command=withdraw)
    button3.grid(row=3,column=4,columnspan=2,padx=20,pady=20)

    footer=ctk.CTkLabel(capp,text="© 2024 Helix Banking Inc. Programmed by Tanish Jain XII-B",pady=40)
    footer.grid(row=4,columnspan=6)

    capp.mainloop()