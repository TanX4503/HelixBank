import socket
import time
import pickle
import mysql.connector
import os
import datetime
import maskpass

# Connecting to AIVEN DigitalOcean MySQL Server
f=open('C:\\HelixTempFiles\\HelixTemp.dat','rb')
mybase=pickle.load(f)
mydb = mysql.connector.connect(host=mybase['host'],port=mybase['port'],user=mybase['user'], password=mybase['password'],database=mybase['database'])
mycursor=mydb.cursor()
os.chdir(mybase['cwd'])
f.close()

# IP Verification Process
def Admin(id,name):
    time.sleep(0.5)
    f=open("assets\\temp.dat",'wb')
    pickle.dump([name,id],f)
    f.close()
    print("Authorizing your IP Address")
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    print(".....",flush=True)
    time.sleep(2)
    if ip.startswith(mybase['adminip']):
        Bonjour(hostname)
    else:
        print("Access Denied.")

# Starting the Console if the IP Address is authenticated
def Bonjour(hostname):
    f=open("assets\\temp.dat",'rb')
    who=pickle.load(f)
    f.close()
    print('''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
                                                              
 █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗                      
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║                      
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║                      
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║                      
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║                      
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝                      
                                                              
          ''',flush=True)
    time.sleep(0.5)
    print("You have been authorized as:")
    print("Name:\t\t"+who[0])
    print("LoginID:\t"+who[1])
    print("Hostname:\t"+hostname,flush=True)
    time.sleep(0.5)
    startconsole()

# Opening new account for a new bank client
def openaccount():
    print("--------------------------------------------ADD NEW USER--------------------------------------------")
    print("Account Opening Charges: Rs. 1200")
    input("Kindly press enter to continue after recieving payment from Client.")
    mycursor.execute("select count(*) from AccountData")
    temp=mycursor.fetchall()
    now=datetime.datetime.now()
    daystamp=now.strftime("%d%m%y")
    clientid=daystamp+"AA"+str(temp[0][0]+1)
    accid=daystamp+"CC"+str(temp[0][0]+1)
    try:
        fname=input("Enter First Name of Client:  ")
        lname=input("Enter Last Name of Client:  ")
        empl=input("Enter Employer of Client:  ")
        desig=input("Enter Designation of Client:  ")

        # Entering the phone number and checking if it is a valid number
        phonetrue=False
        while phonetrue==False:
            phone=int(input("Enter Phone Number of Client:  "))
            phone2=int(input("Enter Alternate Number of Client:  "))
            if 1000000000<=phone<=9999999999 and 1000000000<=phone2<=9999999999:
                phonetrue=True
            else:
                print("Invalid Phone Number(s)!")

        citytown=input("Enter City/Town of Client:  ")
        sex=input("Enter Gender of Client (M/F): ")
        birthdate=int(input("Enter birthdate of client as YYYYMMDD: "))
        income=float(input("Enter Annual Income of Client:  "))
        savings=input("Would the client like to open a savings account? (y/n):  ")
        if savings in 'yY':
            print("Administrator to kindly collect minimum deposit of Rs.5000 from the client.")
            input("Hit enter upon recieving payment.")
            savingsbal=5000
            savings="Yes"
        else:
            savings="No"
        current=input("Would the client like to open a current account? (y/n):  ")
        if current in 'yY':
            print("Administrator to kindly collect minimum deposit amount of Rs.5000 from the client.")
            input("Hit enter upon recieving payment.")
            currentbal=5000
            current="Yes"
        else:
            current="No"

        # Setting up user password
        strong=False
        while strong==False:
            passwd=maskpass.askpass(prompt="Set Login Password:  ",mask="*")
            passwdc=maskpass.askpass(prompt="Confirm Password:  ",mask="*")
            if len(passwd)>=8:
                anydig=False
                anysym=False
                for i in passwd:
                    if i.isdigit()==True:
                        anydig=True
                    if i.isalnum()==False:
                        anysym=True
                if anydig==True and anysym==True:
                    if passwd==passwdc:
                        strong=True
                    else:
                        print("Passwords don't match!")
                else:
                    print("Password must contain at least one digit and one symbol")
            else:
                print("Password must be at least 8 characters long")
        print()

        # Details confirmation
        print("Kindly Confirm your Details:")
        print()
        print("First Name:\t\t",fname)
        print("Last Name:\t\t",lname)
        print("Employer:\t\t",empl)
        print("Designation\t\t",desig)
        print("Phone No.:\t\t",phone," ",phone2)
        print("City/Town:\t\t",citytown)
        print("Sex/Gender:\t\t",sex)
        print("Birthdate:\t\t",str(birthdate)[6:8]+"-"+str(birthdate)[4:6]+"-"+str(birthdate)[0:4])
        print("AnnIncome:\t\t",income)
        print("Savings Account:\t",savings)
        print("Current Account:\t",current)
        print()
        correct=input("All details are correct? (y/n) ")

        # Writing all details to MYSQL Database
        if correct in 'yY':
            if sex in "mMfF":
                if sex in "mM":
                    sex="Male"
                elif sex in "fF":
                    sex="Female"
                mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                mycursor.execute("INSERT INTO ClientData(clientid,first_name,last_name,employer,designation,phone,alt_phone,citytown,sex,birthdate,income) VALUES('"+clientid+"','"+fname+"','"+lname+"','"+empl+"','"+desig+"',"+str(phone)+","+str(phone2)+",'"+citytown+"','"+sex+"',"+str(birthdate)+","+str(income)+");")
                mycursor.execute("INSERT INTO Login(userid,authlevel,passwd) VALUES('"+clientid+"','client','"+passwd+"');")
                mydb.commit()
                if savings=="Yes" and current=="Yes":
                    savings,current=1,1
                    mycursor.execute("INSERT INTO AccountData(accountid,clientid,savings,savingsbal,current,currentbal) VALUES('"+accid+"','"+clientid+"',"+str(savings)+",5000,"+str(current)+",5000);")
                    mydb.commit()
                elif savings=="No" and current=="Yes":
                    savings,current=0,1
                    mycursor.execute("INSERT INTO AccountData(accountid,clientid,savings,current,currentbal) VALUES('"+accid+"','"+clientid+"',"+str(savings)+","+str(current)+",5000);")
                    mydb.commit()
                elif savings=="Yes" and current=="No":
                    savings,current=1,0
                    mycursor.execute("INSERT INTO AccountData(accountid,clientid,savings,savingsbal,current) VALUES('"+accid+"','"+clientid+"',"+str(savings)+",5000,"+str(current)+");")
                    mydb.commit()
                elif savings=="No" and current=="No":
                    savings,current=0,0
                    mycursor.execute("INSERT INTO AccountData(accountid,clientid,savings,current) VALUES('"+accid+"','"+clientid+"',"+str(savings)+","+str(current)+");")
                    mydb.commit()

                print()
                print("Registering User...",flush=True)
                time.sleep(2)
                print("User Registered.",flush=True)
                time.sleep(0.5)
                print()

                # Confirmation Message and Welcome Message
                print("****************************** Client Login Credentials ******************************")
                print("****************************DO NOT SHARE THESE WITH ANYONE****************************")
                input("PRESS ENTER TO VIEW CREDENTIALS")
                print("AccountID:\t",accid)
                print("LoginID:\t",clientid)
                print("You may access your account using this software by using your personal credentials.")
                print("Thank You for Choosing to work with us.")
                input("Press Enter to continue...")
                print(
                    '''
    ██╗  ██╗███████╗██╗     ██╗██╗  ██╗    ██████╗  █████╗ ███╗   ██╗██╗  ██╗                            
    ██║  ██║██╔════╝██║     ██║╚██╗██╔╝    ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝                            
    ███████║█████╗  ██║     ██║ ╚███╔╝     ██████╔╝███████║██╔██╗ ██║█████╔╝                             
    ██╔══██║██╔══╝  ██║     ██║ ██╔██╗     ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗                             
    ██║  ██║███████╗███████╗██║██╔╝ ██╗    ██████╔╝██║  ██║██║ ╚████║██║  ██╗                            
    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                            
                                                                                                        
    ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗███████╗    ██╗   ██╗ ██████╗ ██╗   ██╗
    ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝██╔════╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║
    ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  ███████╗     ╚████╔╝ ██║   ██║██║   ██║
    ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ╚════██║      ╚██╔╝  ██║   ██║██║   ██║
    ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗███████║       ██║   ╚██████╔╝╚██████╔╝
    ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ 
                    '''
                )
                print()
                print("*")
                print("*")
                input("Press Enter to Continue...")

    # Error and Exception Handling, Invalid Value checking
            else:
                print("Invalid Values Entered!")
                print("Cancelling Transaction...",flush=True)
                time.sleep(1)
                print("*",flush=True)
                time.sleep(0.5)
                print("*",flush=True)
                time.sleep(0.5)
                print()
        else:
            print("Cancelling Transaction...",flush=True)
            time.sleep(1)
            print("*",flush=True)
            time.sleep(0.5)
            print("*",flush=True)
            time.sleep(0.5)
    except ValueError:
        print("Kinly Enter valid values!")
    except:
        print("An unexpected error was encountered. Transaction Failed.")
    finally:
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        mydb.commit()

# Starting the Admin console after the initial welcome
def startconsole():
    while True:
        print()
        print("---------------------------------------Welcome to HELIX BANK!----------------------------------------")
        print("----------------------------Computer Science Project by Tanish Jain XII-B----------------------------")
        print("ADMIN FUNCTIONS")
        print("1. Open account of new user")
        print("2. Check client data")
        print("3. Check employee data")
        print("4. Check transaction log")
        print("5. Quit")
        try:
            ch=int(input("Enter your choice:  "))
            if ch==1:
                openaccount()
            elif ch==2:
                # Check Client Data
                id=input("Enter ClientID of the Client whose details you wish to view:  ")
                print()
                mycursor.execute("select * from ClientData natural join AccountData where clientid='"+id+"';")
                data=mycursor.fetchall()
                print("ClientID: \t\t",data[0][0])
                print("FirstName: \t\t",data[0][1])
                print("LastName: \t\t",data[0][2])
                print("Employer: \t\t",data[0][3])
                print("Designation: \t\t",data[0][4])
                print("Phone: \t\t\t",data[0][5])
                print("AltPhone: \t\t",data[0][6])
                print("City/Town: \t\t",data[0][7])
                print("Sex/Gender: \t\t",data[0][8])
                print("Birthdate: \t\t",data[0][9])
                print("Income: \t\t",data[0][10])
                print("AccountID: \t\t",data[0][11])
                print("Savings Exists: \t",data[0][12])
                print("Savings Balance: \t",data[0][13])
                print("Curremt Exists: \t",data[0][14])
                print("Current Balance: \t",data[0][15])
            elif ch==3:
                # Check Employee Data
                id=input("Enter EmployeeID of the Employee whose details you wish to view:  ")
                print()
                mycursor.execute("select * from EmployeeData where empid='"+id+"';")
                data=mycursor.fetchall()
                print("EmployeeID:\t",data[0][0])
                print("FirstName:\t",data[0][1])
                print("LastName:\t",data[0][2])
                print("Department:\t",data[0][3])
                print("Designation:\t",data[0][4])
                print("Phone:\t\t",data[0][5])
                print("AltPhone:\t",data[0][6])
                print("EduLevel:\t",data[0][7])
                print("Sex/Gender:\t",data[0][8])
                print("Birthdate:\t",data[0][9])
                print("Salary:\t\t",data[0][10])
                print("Notes:\t\t",data[0][11])
            elif ch==4:
                mycursor.execute("select * from TransactionHistory;")
                data=mycursor.fetchall()
                print("TransactionID\t\t\tDebitedFrom\tDebitedTo\tAmount\tNotes")
                for i in data:
                    for j in i:
                        print(j,end="\t")
                    print()
            elif ch==5:
                break

        # Exception Handing
        except ValueError:
            print("\nKindly enter a valid value!",flush=True)
            time.sleep(0.5)
        except TypeError:
            print("\nKindly enter a valid value!",flush=True)
            time.sleep(0.5)
        except IndexError:
            print("\nKindly enter a valid value!",flush=True)
            time.sleep(0.5)
        except KeyError:
            print("\nKindly enter a valid value!",flush=True)
            time.sleep(0.5)
        except:
            print("\nAn unexpected error was enountered.",flush=True)
            time.sleep(0.5)