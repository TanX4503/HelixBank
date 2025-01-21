# Setup file containing setup functions for the Helix Banking Console
def setup(dir):
    # Creating Temp Files Folder in C Drive
    import os
    os.chdir(dir)
    import pickle
    folder="C:\\HelixTempFiles"
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Storing Connectivity Details in the temp files folder along with the cwd in order to know the path to the scripts folder whenever main.py is run from anywhere on the device
    f=open('C:\\HelixTempFiles\\HelixTemp.dat','wb')
    internalinfo=dict(host='',port='',user='', password='',database='',adminip='',cwd=dir)
    pickle.dump(internalinfo,f)
    f.close()