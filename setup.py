# Used to setup the required temp files.

# Checking Platform of the user.
from sys import platform
if platform == "win32":
    # Using the setupscripts.py file to run setup procedures.
    dir=input("Enter the file path of the installation folder: (eg. C:\\Users\\.....\\BankManagementConsole)\n")
    import scripts.setupscript as setupfile
    setupfile.setup(dir)
    print()
    print("Checking for existence of required modules...")
    try:
        import mysql.connector
        import maskpass
        import PIL
        import customtkinter
        import CTkMessagebox
    except:
        print("Your device doesn't meet the software requirements. Kindly download the required modules as listed in help.readme")
    finally:
        print()
        print("Setup Procedures have been performed")
        input("Kindly press enter to exit...")

# In case operating system is not windows
else:
    print("Operating System not supported. Kindly use a Windows Machine to use the HELIX Banking Application.")
    print()
    input("Press enter to exit...")