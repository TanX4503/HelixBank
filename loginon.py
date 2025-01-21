import mysql.connector
import os
import pickle

# Connecting to AIVEN Console
f=open('C:\\HelixTempFiles\\HelixTemp.dat','rb')
mybase=pickle.load(f)
mydb = mysql.connector.connect(host=mybase['host'],port=mybase['port'],user=mybase['user'], password=mybase['password'],database=mybase['database'])
mycursor=mydb.cursor()
os.chdir(mybase['cwd'])
f.close()

# Checks if entered password is correct
def Login(id,passwd):
    mycursor.execute("select * from Login")
    details=mycursor.fetchall()
    level=False
    for i in details:
        if i[0]==id and i[2]==passwd:
            level=i[1]
    return level

# Gets the name of the user using the id of the user
def getName(id,level):
    try:
        if level=="client":
            mycursor.execute("select clientid,first_name,last_name from ClientData where clientid='"+id+"';")
            details=mycursor.fetchall()
            value=details[0][1]+" "+details[0][2]
            return value
        else:
            mycursor.execute("select empid,first_name,last_name from EmployeeData where empid='"+id+"';")
            details=mycursor.fetchall()
            value=details[0][1]+" "+details[0][2]
            return value
    except:
        return "Unnamed User"