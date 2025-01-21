'''
All database functions are performed via other python files that are part of this project
main.py deals only with what has to be displayed on screen
Logic behind commands are present in the other files of this distribution:
 - setupscript.py
 - loginon.py
 - emp.py
 - admin.py
 - client.py
'''

# Loading Message
print("Loading Helix Banking...",flush=True)

# Importing Required Modules
import time
import os
import mysql.connector
import pickle
import maskpass
from sys import platform

# Some Required Functions
genauth=False
def end():
    print()
    if genauth==True:
        print("Pleasure to work with you!",flush=True)
        time.sleep(1)
    print("-----------------------------------------------------------------------------------------------------")
    print()
    print("© 2024 Helix Banking Inc. Programmed by Tanish Jain XII-B")
    print("The terminal window will auto-terminate in 5 seconds...",flush=True) #Output flushing is necessary before using time.sleep as output buffering can cause the command to not work as intended.
    time.sleep(5)
    print()
    exit()

# This try except block is created to ensure that python doesn't run into an error and crashes if the connection is unsuccessful
try:
    # Connecting to AIVEN DigitalOcean MySQL Server
    f=open('C:\\HelixTempFiles\\HelixTemp.dat','rb')
    mybase=pickle.load(f)
    mydb = mysql.connector.connect(host=mybase['host'],port=mybase['port'],user=mybase['user'], password=mybase['password'],database=mybase['database'])
    mycursor=mydb.cursor()
    os.chdir(mybase['cwd'])
    f.close()
except:
    print("You are offline. Kindly reconnect to the internet and reopen the console. If that doesn't work, try running the setup.py file present in the Helix Bank Installation Folder.",flush=True)
    end()

# Importing Required Files
import scripts.loginon as loginon
import scripts.emp as emp
import scripts.admin as admin
import scripts.client as client
if platform == "win32":
    print()
    # CUI Interface
    print("---------------------------------------Welcome to HELIX BANK!----------------------------------------")
    print("----------------------------Computer Science Project by Tanish Jain XII-B----------------------------")
    print()
    ch=input("Do you wish to proceed?(y/n) ")

    # Login to Bank Console
    if ch=="y":
        print()
        print("--------------------------------------Login to Bank Server-------------------------------------------")
        n=0
        while n<3:
            id=input("UserID:  ")
            passwd=maskpass.askpass(prompt="Password:  ",mask="*")
            level=loginon.Login(id,passwd)
            if level!=False:
                genauth=True
                name=loginon.getName(id,level)
                if level=="admin":
                    print("Administrator Login Request Recieved.")
                else:
                    print("\nWelcome to Console,",name)
                print("-----------------------------------------------------------------------------------------------------")
                break
            else:
                print("Authorization Failed.")
                n+=1
                print("You have",3-n,"attempts remaining...\n")
        if genauth==False:
            end() # Not to be confused with exit() which is used to kill the program
    else:
        end()

    # Now accessing the required applications as per the authentication level of the user.
    if level=="client":
        print("Launching Helix Client Interface...")
        client.client(id,name)
        end()
    elif level=="teller":
        print("Launching Helix Bank Management...")
        emp.Emp(id,name)
        end()
    elif level=="admin":
        print("Launching Admin Verification Protocol...",flush=True)
        admin.Admin(id,name)
        end()
    else:
        print("User Verification is incomplete. Kindly contact admin for more information.")
        end()

# Incase the OS is not windows
else:
    print("Operating System not supported. Kindly use a Windows Machine to use the HELIX Banking Application.")
    end()