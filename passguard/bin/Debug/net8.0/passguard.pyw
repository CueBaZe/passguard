import random
import os
import string
import sys
import subprocess
import ctypes

def run_batch_script():
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        #Makes the path to the folder the script is in
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    #Makes the path to the batch file
    batch_file = os.path.join(script_dir, "passguard.bat")
    #Makes the path to hasrunned
    hasrunned_file = os.path.join(script_dir, "hasrunned.txt")
    
    #Checks if the hasrunned.txt exists
    if not os.path.exists(hasrunned_file):
        #Calls the batch file
        subprocess.call(batch_file, shell=True)
        #Makes the hasrunned.txt in the folder
        with open(hasrunned_file, "w") as file:
            ctypes.windll.kernel32.SetFileAttributesW(hasrunned_file, 0x02)
    else:
        print("Batch script has been runned once")

run_batch_script()

import tkinter as tk
from tkinter import ttk
import clipboard
import shutil

#########################(Folder path)#########################

folderpath = os.path.expanduser("~")
foldername = "vault"
folder = os.path.join(folderpath, foldername)

#########################(File paths)#########################

path = os.path.expanduser("~")
filen = "password.txt"
keyn = "key.txt"
loginn = "login.txt"
filename = os.path.join(path, foldername, filen)
keyname = os.path.join(path, foldername, keyn)
loginname = os.path.join(path, foldername, loginn)

#########################(Char List)#########################

char = string.punctuation + string.ascii_letters + string.digits
char = list(char)

#########################(Make and save functions)#########################

def make_folder():
    #Checks if the folder exists
    isExists = os.path.exists(folder)
    if not isExists:
        #Makes the folder
        os.chdir(folderpath)
        os.mkdir(folder)
        #Set the folder attribute to hidden
        ctypes.windll.kernel32.SetFileAttributesW(folder, 0x02)
    else:
        print("Folder all ready exists")

make_folder()

#This function makes the password
def makepassword(name, length):
    password_name = name
    password_length = length
    password = ""
    #Makes a random password
    for index in range(password_length):
        tempchar = random.choice(char)
        if tempchar != "\\":
            password += tempchar
        else:
            password_length += 1
    #Runs the function save_password. Checks if it returns true or false
    if save_Password(password_name, password, filename):
        #Returned true
        label_infotext_main.config(text="Password successfully saved. Use search to see password")
    else:
        #Returned false
        label_infotext_main.config(text="A password with that name already exists.")

#This function saves the password in password.txt
def save_Password(password_Name, password, filename):
    #It runs the function encrypt. So the password will get encrypted
    password = encrypt(password, get_key())
    #Checks if password.txt dosent exists
    isExists = os.path.exists(filename)
    if not isExists:
            #Makes the file password.txt
            with open(filename, "w") as file:
                print("File is created!")
    #Checks if the password name all ready exists
    with open(filename, "r") as f:
        existing_passwords = f.readlines()
    #Goes trough all lines in password.txt
    for line in existing_passwords:
        #Checks if the name on the line is the same as the new password
        if f"Name: {password_Name} " in line:
            return False  # Password name already exists
        
    #If the password name dosent exist. It saves the password in password.txt
    with open(filename, "a") as f:

        f.write(f"Name: {password_Name} Password: {password}\n")
    return True

#########################(Delete functions)#########################

#This function deletes passwords
def deletepassword(name):
    password_found = 0
    password_name = name

    with open(filename, "r+") as f:
        passwords = f.readlines()

    with open(filename, "w") as f:
        #Goes trough all lines in password.txt
        for line in passwords:
            #Checks if the line dosent match with the name we have typed in
            if f"Name: {password_name} " not in line:
                #if it dosent match it writes the line
                f.write(line)
            else:
                password_found = 1
    #Prints out the correct text
    if password_found == 1:
        label_infotext_main.config(text="Password deleted!")
    else:
        label_infotext_main.config(text="Password was not found!")

def deleteallpassword():

    #Checks if the password.txt exists
    isExists = os.path.exists(filename)
    if isExists:

        #Opens the password.txt and reads all the lines in it
        with open(filename, "r") as file:
            passwords = file.readlines()

        with open(filename, "w") as file:
            #Loops the passwords and dosent write them again so they been deleted
            for password in passwords:
                print("deleted")
            label_infotext_main.config(text="All passwords was deleted!")
    else:
        label_infotext_main.config(text="Password.txt dosent exist")

#########################(Search functions)#########################
    
#This function can search for passwords
def searchpassword(name):
    password_name = name
    name_found = 0

    with open(filename, "r") as f:
        passwords = f.readlines()
        #Goes trough all lines in password.txt
        for line in passwords:
            #Checks if it can find the name you typed in
            if f"Name: {password_name} " in line:
                #Removes all the text so you only have the password remaining
                password = line.replace(f"Name: {password_name} Password:", "").strip()
                decrypted_password = decrypt(password, get_key()) #Decrypts the password
                print(decrypted_password)
                clipboard.copy(decrypted_password) #Copys the password to the clipboard
                label_infotext_main.config(text="Password: " + decrypted_password +" Password saved on clipboard")
                name_found = 1

    if name_found == 0:
        label_infotext_main.config(text="Password was not found!")


    if name_found != 1:
        label_infotext_main.config(text="Password was not found!")

def search_all_text(textbox, frame):
        row = 0
        #Checks it the password.txt exists
        if os.path.exists(filename):
            #Opens the password.txt and reads all the lines
            with open(filename, 'r') as file:
                lines = file.readlines()
                #loops the lines
                for line in lines:
                    row += 1
                    #Removes the text we dont need
                    line = line.replace(f"Name:", "").strip()
                    line = line.replace(f"Password:", "").strip()
                    line = line.split(" ") #Splits the password at space
                    #Decrypts the password
                    password = decrypt(line[2], get_key())
                    #Makes the input line and puts it in the textbox
                    input = f"{row}. Name: {line[0]} Password: {password}\n"
                    textbox.insert(tk.END, input) #Insert the content into the textbox
                if row <= 0:
                    #If there is any password in the password.txt it closes the frame
                    label_infotext_main.config(text="No passwords found!")
                    frame.destroy() 
        else:
            #If the password.txt dosent exists the frame closes
            label_infotext_main.config(text="Password.txt dosent exist")
            frame.destroy()

#########################(Key functions)#########################

def make_key():
    key = ""
    #Checks if key.txt exists
    isExists = os.path.exists(keyname)
    if isExists:
        sureKeyWindow()
    else:
        #If it dosent exists is runs this
        with open(keyname, "w") as file:
            create_key = char.copy() #Makes a copy of the char list
            random.shuffle(create_key) #Shuffles the list
            #Takes the list and puts it in a string, so it can be saved in key.txt
            for x in create_key:
                key += "" + x
            file.write(key) 

def new_key():
    old_key = get_key() #Saves the old key in this var
    create_key = char.copy() #Makes a copy of the char list
    random.shuffle(create_key) #Shuffles the list
    key = ""

    with open(keyname, "w") as file: #Opens the key.txt as file
        #loops the create_key
        for x in create_key: 
            key += "" + x #Takes key + the char
        file.write(key) #Saves the new key in key.txt
        
    isExists = os.path.exists(filename)
    if isExists:
    
        with open(filename, "r") as file:
            passwords = file.readlines() #Reads all the lines in password.txt

        with open(filename, "w") as file:
            #loops the passwords
            for password in passwords:
                print(password)
                #Removes the text that we dont need
                password = password.replace(f"Name:", "").strip()
                password = password.replace(f"Password:", "").strip()
                password = password.split(" ") #Splits the password at space
                password_name = password[0] #Sets password_name to the index 0 of password (Name)
                password_pass = password[2] #Sets password_pass to the index 2 of password (Password)
                print(password_name)
                print(password_pass)
                password_pass = decrypt(password_pass, old_key) #Decrypts password with the old key
                password_pass = encrypt(password_pass, key) #Encrypts password with the new key
                line = f"Name: {password_name} Password: {password_pass} \n" #Set line var
                file.write(line) #Writes line into the file
    
    #Opens the loginname.txt and reads the line
    with open(loginname, "r") as file:
        line = file.readline()
        
    with open(loginname, "w") as file:
        line = line.split(":") #Splits the line at ":"
        username = line[0]
        password = line[1]

        #Decrypts with the old key and encrypts with the new key
        username = decrypt(username, old_key)
        username = encrypt(username, key)

        password = decrypt(password, old_key)
        password = encrypt(password, key)

        input = f"{username}:{password}" #Makes the input
        file.write(input) #Writes the input

    label_infotext_main.config(text="New key created")

def get_key():
    #Checks if key.txt exists
    isExists = os.path.exists(keyname)
    if isExists:
        #If key.txt exists it runs this
        with open(keyname, "r") as file:
            key = file.readline() #Reads the first line and puts it in the var "key"
            key = list(key) #Makes it into a list
            return key
    else:
        label_infotext_main.config(text="Please create a key")

#########################(Encrypt/Decrypt functions)#########################

#This function encrypts passwords
def encrypt(input, key):
    userInput = input
    encryptedText = ""
    #Loops the input for every char
    for letter in userInput:
        index = char.index(letter) #Finds the index of the char in the list "char"
        encryptedText += key[index] #Takes encryptedText and + key[index] to it
    return encryptedText #Returns the encrypted password


#This function decrypts passwords
def decrypt(input, key):
    userInput = input
    decryptedText = ""
    #Loops the input for every char
    for letter in userInput:
        index = key.index(letter) #Finds the index of the char in the list "key"
        decryptedText += char[index] #Takes decryptedText and + char[index] to it
    return decryptedText #Returns the decrypted password

#########################(Quit function)#########################

def quit_program(frame):
    frame.destroy()  # Close the menu window
    root.quit()  # Quit the entire application

#########################(Account making function)#########################

def make_account(username, password):
    shutil.rmtree(folder) #deletes the vault folder
    make_folder() #Runs the make folder function 

    make_key() #Makes a new key file

    password = encrypt(password, get_key()) #Encrypts the password
    username = encrypt(username, get_key()) #Encrypts the username

    #Opens a file named login.txt an put in the login infomation
    with open(loginname, "w") as file:
        file.write(f"{username}:{password}")

    root.deiconify() #Opens the login window/root window
#########################(Gui Tkinter)####################################################################################

#########################(Delete window)#########################

def deleteWindow():
    delete = tk.Toplevel(root)
    delete.title("Delete Window")
    delete.geometry("400x200")

    def make_ready_delete():
        name_delete = entry.get()
        name_delete = name_delete.lower()
        name_delete = name_delete.strip()
        if len(name_delete) <= 0:
            label_infotext_main.config(text="You have to type in the name")
        else:
            deletepassword(name_delete)
        delete.destroy()

    def make_ready_delete_all():
        sureDeleteWindow()
        delete.destroy()

    label_title_delete = ttk.Label(delete, text="Delete Function", font=('Arial', 18))
    label_title_delete.pack(padx=10, pady=10)

    label_name_delete = ttk.Label(delete, text="Name of password", font=('Arial', 12))
    label_name_delete.pack()

    entry = ttk.Entry(delete)
    entry.pack()

    button_close = ttk.Button(delete, text="Delete Password", command=make_ready_delete)
    button_close.pack(padx=10, pady=10)

    button_delete_all = ttk.Button(delete, text="Delete all", command=make_ready_delete_all)
    button_delete_all.pack(padx=10, pady=10)

#########################(Search windows)#########################

def searchWindow():
    search = tk.Toplevel(root)
    search.title("Search Window")
    search.geometry("400x200")
    
    def make_ready_search():
        name_search = entry.get()
        name_search = name_search.lower()
        name_search = name_search.strip()
        if len(name_search) <= 0:
            label_infotext_main.config(text="You have to type in the name")
        else:
            searchpassword(name_search)
        search.destroy()

    def make_ready_search_all():
        search_all()
        search.destroy()

    label_title_search = ttk.Label(search, text="Search Function", font=('Arial', 18))
    label_title_search.pack(padx=10, pady=10)

    label_name_search = ttk.Label(search, text="Name of password", font=('Arial', 12))
    label_name_search.pack()

    entry = ttk.Entry(search)
    entry.pack()

    button_close = ttk.Button(search, text="Search Password", command=make_ready_search)
    button_close.pack(padx=10, pady=10)

    button_search_all = ttk.Button(search, text="Search all passwords", command=make_ready_search_all,)
    button_search_all.pack(padx=10, pady=10)

def search_all():
    search_all = tk.Toplevel(root)
    search_all.title("Search all Window")
    search_all.geometry("400x400")

    textbox_searchall = tk.Text(search_all)
    textbox_searchall.pack()

    search_all_text(textbox_searchall, search_all)

#########################(Create window)#########################

def createWindow():
    create = tk.Toplevel(root)
    create.title("Create Window")
    create.geometry("400x250")

    def make_ready_create():
        name_create = entry.get()
        name_create = name_create.lower()
        name_create = name_create.strip()
        if len(name_create) <= 0:
            label_infotext_main.config(text="You have to type in a name")
            create.destroy()
        else:
            length_create = slider.get()
            length_create = int(length_create)
            create.destroy()
            makepassword(name_create, length_create)

    label_title_create = ttk.Label(create, text="Create Function", font=('Arial', 18))
    label_title_create.pack(padx=10, pady=10)

    label_name_create = ttk.Label(create, text="Name of password", font=('Arial', 12))
    label_name_create.pack()

    entry = ttk.Entry(create)
    entry.pack()

    label_length_create = ttk.Label(create, text="Length of Password", font=('Arial', 12))
    label_length_create.pack(padx=10, pady=10)

    slider = tk.Scale(create, from_=4, to=25, orient="horizontal")
    slider.pack()

    button_close = ttk.Button(create, text="Create Password", command=make_ready_create)
    button_close.pack(padx=10, pady=10)

#########################(Sure windows)#########################

def sureKeyWindow():

    surekwin = tk.Toplevel(root)
    surekwin.title("Are you sure?")
    surekwin.geometry("350x150")

    def new_key_ready():
        surekwin.destroy()
        new_key()

    label_title_sure = tk.Label(surekwin, text="Are you sure you want to make a new key?", font=("Arial", 12))
    label_title_sure.pack(padx=10, pady=10)
    button_yes_sure = tk.Button(surekwin, text="Yes", command=new_key_ready, font=("Arial", 12))
    button_yes_sure.place(x=80, y=75)
    button_no_sure = tk.Button(surekwin, text="No", command=surekwin.destroy, font=("Arial", 12))
    button_no_sure.place(x=230, y=75)


def sureDeleteWindow():

    suredwin = tk.Toplevel()
    suredwin.title("Are you sure?")
    suredwin.geometry("380x150")

    def delete_all_ready():
        suredwin.destroy()
        deleteallpassword()

    label_title_sure = tk.Label(suredwin, text="Are you sure you want to delete all your passwords?", font=("Arial", 12))
    label_title_sure.pack(padx=10, pady=10)
    button_yes_sure = tk.Button(suredwin, text="Yes", command=delete_all_ready, font=("Arial", 12))
    button_yes_sure.place(x=80, y=75)
    button_no_sure = tk.Button(suredwin, text="No", command=suredwin.destroy, font=("Arial", 12))
    button_no_sure.place(x=230, y=75)

#########################(Menu window)#########################

def menuWindow():

    global label_infotext_main

    menu = tk.Toplevel()
    menu.geometry("800x500")
    menu.title("Password Generator ")
    menu.protocol("WM_DELETE_WINDOW", lambda: quit_program(menu))

    label_title_main = tk.Label(menu, text="Password Generator", font=('Arial', 18))
    label_title_main.pack(padx=20, pady=20)

    button_delete = tk.Button(menu, text="Delete", font=('Arial', 18), command=deleteWindow, background="red")
    button_delete.pack(pady=20)
    button_search = tk.Button(menu, text="Search", font=('Arial', 18), command=searchWindow, background="blue")
    button_search.pack(pady=20)
    button_create = tk.Button(menu, text="Create", font=('Arial', 18), command=createWindow, background="green")
    button_create.pack(pady=20)
    button_key = tk.Button(menu, text="Key", font=('Arial', 18), command=make_key, background="yellow")
    button_key.pack(pady=20)

    label_infotext_main = tk.Label(menu, text="Please select one of the functions", font=('Arial', 18))
    label_infotext_main.pack(padx=30, pady=30)

#########################(Account making window)#########################

def makeaccWindow():
    acc = tk.Toplevel()
    acc.geometry("300x220")
    acc.title("Make Account ")
    acc.protocol("WM_DELETE_WINDOW", lambda: quit_program(acc))

    def makeaccfunc():
        username = entry_username_acc.get()
        password = entry_password_acc.get()
        username = username.lower()
        if len(username) >= 6:
            if len(password) >= 8:
                if "\\" in username or "\\" in password:
                    label_fail_acc.config(text="Please do not use '\\'")
                else:   
                    make_account(username, password)
                    acc.withdraw()
            else:
                label_fail_acc.config(text="Password failed!")
        else:
            label_fail_acc.config(text="Username failed!")

    label_username_acc = ttk.Label(acc, text="Username: (Atleast 6 chars)", font=('Arial', 12))
    label_username_acc.pack()

    entry_username_acc = ttk.Entry(acc)
    entry_username_acc.pack(pady=10)

    label_password_acc = ttk.Label(acc, text="Password: (Atleast 8 chars)", font=('Arial', 12))
    label_password_acc.pack()

    entry_password_acc = ttk.Entry(acc)
    entry_password_acc.pack(pady=10)

    label_fail_acc = ttk.Label(acc, text="", font=('Arial', 12))
    label_fail_acc.pack()

    button_delete = tk.Button(acc, text="Login", font=('Arial', 12), command=makeaccfunc, background="red")
    button_delete.pack(pady=20)

#########################(Root/Login window)#########################

root = tk.Tk()

root.geometry("300x220")
root.title("Login ")

def loginfunc():
    username = entry_username_root.get()
    password = entry_password_root.get()
    username = username.lower()
    with open(loginname, "r") as file:
        line = file.readline()
    line = line.split(":")
    real_username = decrypt(line[0], get_key())
    real_password = decrypt(line[1], get_key())
    if username == real_username:
        if password == real_password:
            menuWindow()
            root.withdraw()
        else:
            label_fail_root.config(text="Password is wrong!")
    else:
        label_fail_root.config(text="Username is wrong!")

label_username_root = ttk.Label(root, text="Username:", font=('Arial', 12))
label_username_root.pack()

entry_username_root = ttk.Entry()
entry_username_root.pack(pady=10)

label_password_root = ttk.Label(root, text="Password:", font=('Arial', 12))
label_password_root.pack()

entry_password_root = ttk.Entry()
entry_password_root.pack(pady=10)

label_fail_root = ttk.Label(root, text="", font=('Arial', 12))
label_fail_root.pack()

button_login_root = tk.Button(root, text="Login", font=('Arial', 12), command=loginfunc, background="red")
button_login_root.pack(pady=20)

isExists = os.path.exists(loginname)
if not isExists:
    root.withdraw()
    makeaccWindow()

root.mainloop()


