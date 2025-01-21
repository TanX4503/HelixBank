# Importing Required Modules
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

# Payment Gateway for performing transactions by the bank client.
def transaction():
    f=open('assets\\temp.dat','rb')
    clientid=pickle.load(f)
    f.close()

    # Starting Payment Registrations
    def pay():
        # Transaction Registration to the MySQL Database (Step-3)
        def register_transaction(data):
            # Getting Ready to Register Transaction
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

                # Final Transaction Registration
                mycursor.execute("insert into TransactionHistory values('"+transid+"','"+data[0]+"','"+data[1]+"',"+str(data[2])+",'"+data[3]+"');")
                mydb.commit()
                CTkMessagebox(message="Transaction Successful. TransactionID="+transid,icon="check", option_1="Thanks",title="Payment Successful")
            except:
                mydb.rollback()
                CTkMessagebox(message="An unexpected error was encountered. Transaction Failed!",icon="cancel",title="Transaction Failed")
            finally:
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                mydb.commit()
        
        # Verifying the Entered Data (Step-2)
        debitto=DebitTo.get()
        ammount=Ammount.get()
        notes=Notes.get()
        password=Password.get()
        towhere=radio_var.get()
        if debitto!="" and ammount!="" and password!="":
            try:
                ammount=float(ammount)
            except ValueError:
                CTkMessagebox(message="Amount must be a number!",icon="warning",title="Error")
            mycursor.execute("select * from Login where userid='"+clientid+"';")
            logininfo=mycursor.fetchall()
            if logininfo[0][2]==password:
                mycursor.execute("select accountid from AccountData;")
                acclist=mycursor.fetchall()
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
                CTkMessagebox(message="Kindly enter valid password!",icon="cancel",title="Error")
        else:
            CTkMessagebox(message="No fields except Notes can be blank.",icon="info",title="Info")

    # Displaying the Transaction Window for the user to enter the details in (Step-1)
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
    mycursor.execute("select * from AccountData where clientid = '"+clientid+"';")
    mydata=mycursor.fetchall()
    debitfrom=mydata[0][0]
    label2=ctk.CTkLabel(app,text=debitfrom)
    label2.grid(row=2,column=1)

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

    label6=ctk.CTkLabel(app,text="Password:",pady=2)
    label6.grid(row=6,column=0)
    Password=ctk.StringVar()
    entry4=ctk.CTkEntry(app,textvariable=Password,show="*")
    entry4.grid(row=6,column=1,pady=2)

    # Radiobuttons for Paying to Current or Savings A/C
    radio_var = tkinter.IntVar(value=0)
    radiobutton_1 = ctk.CTkRadioButton(master=app, text="Pay to Current A/C",variable=radio_var, value=0)
    radiobutton_2 = ctk.CTkRadioButton(master=app, text="Pay to Savings A/C",variable=radio_var, value=1)
    radiobutton_1.grid(row=7,columnspan=2,pady=5)
    radiobutton_2.grid(row=8,columnspan=2,pady=5)

    # Confirm Transaction Button
    button=ctk.CTkButton(app,text="Confirm Transaction",command=pay)
    button.grid(row=9,columnspan=2,padx=20,pady=20)

    app.mainloop()

# Transaction History Console to view Transaction History of the user
def transhist():
    try:
        # Getting ClientID from temp file
        f=open('assets\\temp.dat','rb')
        clientid=pickle.load(f)
        f.close()

        # Starting the CTk Interface
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")
        tapp=ctk.CTkToplevel()
        tapp.geometry("1100x780")
        tapp.resizable(False,False)
        tapp.title("Helix Transaction Log")
        tapp.grid_columnconfigure(0,weight=1)
        tapp.grid_columnconfigure(1,weight=1)
        tapp.grid_columnconfigure(2,weight=1)
        tapp.grid_columnconfigure(3,weight=1)

        mycursor.execute("select * from AccountData natural join ClientData where clientid='"+clientid+"';")
        accinfo=mycursor.fetchall()
        accountid=accinfo[0][1]
        mycursor.execute("select * from TransactionHistory where debitfrom='"+accountid+"';")
        rawhistory=mycursor.fetchall()
        
        myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
        imglabel=ctk.CTkLabel(tapp,text="",image=myimg)
        imglabel.grid(row=0,column=0,rowspan=2)
        title=ctk.CTkLabel(tapp,text="Transaction\nHistory",font=('Cascadia Code',30))
        title.grid(row=0,column=1,columnspan=3,pady=0)
        titleinfo=ctk.CTkLabel(tapp,text="Account Number: \nFull Name: \nTotal Transactions: \nDate and Time: ",font=('Arial',15))
        titleinfo.grid(row=1,column=1,pady=0)
        information=ctk.CTkLabel(tapp,text=accinfo[0][1]+"\n"+accinfo[0][6]+" "+accinfo[0][7]+"\n"+str(len(rawhistory))+"\n"+str(datetime.datetime.now())[0:19],font=('Arial',15))
        information.grid(row=1,column=2,pady=0,columnspan=2)

        myframe=ctk.CTkScrollableFrame(tapp,orientation="vertical",width=950,height=500)
        myframe.grid(column=0,row=3,columnspan=4)
        myframe.grid_columnconfigure(0,weight=1)
        myframe.grid_columnconfigure(1,weight=1)
        myframe.grid_columnconfigure(2,weight=1)
        myframe.grid_columnconfigure(3,weight=1)
        myframe.grid_columnconfigure(4,weight=1)
        
        tablehead1=ctk.CTkLabel(myframe,text="TransactionID",font=('Arial',15))
        tablehead1.grid(row=0,column=0)
        tablehead2=ctk.CTkLabel(myframe,text="Transactioning\nAccount",font=('Arial',15))
        tablehead2.grid(row=0,column=1)
        tablehead3=ctk.CTkLabel(myframe,text="Beneficiary\nAccount",font=('Arial',15))
        tablehead3.grid(row=0,column=2)
        tablehead4=ctk.CTkLabel(myframe,text="Amount",font=('Arial',15))
        tablehead4.grid(row=0,column=3)
        tablehead5=ctk.CTkLabel(myframe,text="Date of Transaction",font=('Arial',15))
        tablehead5.grid(row=0,column=4)
        tablehead6=ctk.CTkLabel(myframe,text="Notes",font=('Arial',15))
        tablehead6.grid(row=0,column=5)

        for i in range(0,len(rawhistory)):
            label1=ctk.CTkLabel(myframe,text=rawhistory[i][0],font=('Arial',15))
            label2=ctk.CTkLabel(myframe,text=rawhistory[i][1],font=('Arial',15))
            label3=ctk.CTkLabel(myframe,text=rawhistory[i][2]+" "+rawhistory[i][0][23],font=('Arial',15))
            label4=ctk.CTkLabel(myframe,text=rawhistory[i][3],font=('Arial',15))
            label5=ctk.CTkLabel(myframe,text=rawhistory[i][0][4:6]+"-"+rawhistory[i][0][2:4]+"-"+rawhistory[i][0][0:2],font=('Arial',15))
            label6=ctk.CTkLabel(myframe,text=rawhistory[i][4],font=('Arial',15))

            label1.grid(row=i+1,column=0)
            label2.grid(row=i+1,column=1)
            label3.grid(row=i+1,column=2)
            label4.grid(row=i+1,column=3)
            label5.grid(row=i+1,column=4)
            label6.grid(row=i+1,column=5)

        tapp.mainloop()
    except:
        print("An internal error was encountered during the execution of the program. It is recommended to restart the application.")

# Main Window of the Client Application
def client(clientid,name):
    f=open('assets\\temp.dat','wb')
    pickle.dump(clientid,f)
    f.close()

    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")
    capp=ctk.CTk()
    capp.geometry("800x500")
    capp.resizable(False,False)
    capp.title("Helix Client Interface")
    capp.wm_iconbitmap("assets\\favicon.ico")

    mycursor.execute("select * from ClientData inner join AccountData on ClientData.clientid=AccountData.clientid where ClientData.clientid='"+clientid+"';")
    clientdata=mycursor.fetchall()

    capp.grid_columnconfigure(0,weight=1)
    capp.grid_columnconfigure(1,weight=1)
    capp.grid_columnconfigure(2,weight=1)
    capp.grid_columnconfigure(3,weight=1)
    capp.grid_columnconfigure(4,weight=1)
    capp.grid_columnconfigure(5,weight=1)

    # Logo Image Configuration and Bank Balance Display
    myimg = ctk.CTkImage(light_image=Image.open("assets\\logo.png"),dark_image=Image.open("assets\\logo.png"),size=(250,250))
    imglabel=ctk.CTkLabel(capp,text="",image=myimg)
    imglabel.grid(row=0,columnspan=3)
    money=ctk.CTkLabel(capp,text="Savings Account Balance: ₹"+str(clientdata[0][14])+"\nCurrent Account Balance: ₹"+str(clientdata[0][16]),font=('Arial',15))
    money.grid(row=0,column=3,columnspan=3)

    # Header
    title=ctk.CTkLabel(capp,text="Welcome to Helix Bank,",font=('Courier',30))
    nametitle=ctk.CTkLabel(capp,text=name,font=('Cascadia Code',30))
    title.grid(row=1,columnspan=6,pady=0)
    nametitle.grid(row=2,columnspan=6,pady=0)

    # Buttons and Defining the Information Function
    def info():
        clientinfostring="ClientID: "+clientdata[0][0]+"\nName: "+name+"\nEmployer:  "+clientdata[0][3]+"\nDesignation:  "+clientdata[0][4]+"\nPhone:  "+str(clientdata[0][5])+"  "+str(clientdata[0][6])+"\nCity/Town:  "+clientdata[0][7]+"\nSex:  "+clientdata[0][8]+"\nBirthdate:  "+str(clientdata[0][9])+"\nIncome:  "+str(clientdata[0][10])
        CTkMessagebox(message=clientinfostring,icon='info',title="My Information")
    button1=ctk.CTkButton(capp,text="My Information",command=info)
    button1.grid(row=3,column=0,columnspan=2,padx=20,pady=40)
    button2=ctk.CTkButton(capp,text="Send Money",command=transaction)
    button2.grid(row=3,column=2,columnspan=2,padx=20,pady=20)
    button3=ctk.CTkButton(capp,text="Transaction History",command=transhist)
    button3.grid(row=3,column=4,columnspan=2,padx=20,pady=20)

    # Footer
    footer=ctk.CTkLabel(capp,text="© 2024 Helix Banking Inc. Programmed by Tanish Jain XII-B",pady=40)
    footer.grid(row=4,columnspan=6)

    capp.mainloop()