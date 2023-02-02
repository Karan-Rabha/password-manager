import random
import string
import re
from tkinter import * 
from tkinter import messagebox, filedialog
from file import save_file, get_data
from emailsender import send_email
import os



SAVE_TO_FOLDER_PATH=""

try:
    with open("path.txt", "r") as f:
        SAVE_TO_FOLDER_PATH= f.read()
except FileNotFoundError:
    with open("path.txt", "w+") as f:
        f.write(os.getcwd())
        f.seek(0)
        SAVE_TO_FOLDER_PATH= f.read()


def set_folder_path():
    global SAVE_TO_FOLDER_PATH
    folder_path = filedialog.askdirectory(initialdir=SAVE_TO_FOLDER_PATH)
    if folder_path:
        with open("path.txt", "w+") as f1:
            f1.write(folder_path)
            f1.seek(0)
            SAVE_TO_FOLDER_PATH= f1.read()


def generate_password():
    UNWANTED_PUNCTUATION = "[-'~`\",_\/.:;^|]"
    
    password_length= int(password_length_value.get()) #getting the value of password length
    password = ''.join(random.choices(string.ascii_letters + string.digits + re.sub(UNWANTED_PUNCTUATION,"",string.punctuation), k=password_length))
    website_data_value.set("Website")
    user_selected_check = website.get()
    try:
        user_data_check = get_data(SAVE_TO_FOLDER_PATH)
        data_available = user_data_check[user_selected_check]
        if data_available:
            website.delete(0, END)
            email.delete(0, END)
    except KeyError:
        if user_selected_check == "Please select an website" or user_selected_check == "No data available":
            website.delete(0, END)
            email.delete(0, END)

    new_password.delete(0, END)
    new_password.insert(0, password)

    
def save_password():
    ## entered user data
    userdata = {"website":website.get(),"email":email.get(), "password":new_password.get()}
    userweb= userdata["website"]
    usermail= userdata["email"]
    check_entry_field = ("","Please select an website", "No data available", "Please fill in this field")

    # checking if the fields are valid or not if not valid don't save the data
    if userweb == "" and usermail == "" or userweb == "Please select an website" and usermail == "Please select an website" or userweb == "No data available" and usermail == "No data available":
        website.delete(0, END)
        email.delete(0, END)
        website.insert(0, "Please fill in this field")
        email.insert(0, "Please fill in this field")
    elif userweb in ("", "Please select an website", "No data available", "Please fill in this field", "Already present"):
        website.delete(0, END)
        website.insert(0, "Please fill in this field")
        if usermail in check_entry_field:
            email.delete(0, END)
            email.insert(0, "Please fill in this field")
    elif usermail in check_entry_field:
        email.delete(0, END)
        email.insert(0, "Please fill in this field")
        if userweb in check_entry_field:
            website.delete(0, END)
            website.insert(0, "Please fill in this field")
    else:
        try:
            userdata_check = get_data(SAVE_TO_FOLDER_PATH)
            web_available = userdata_check[userweb]
            if web_available:
                website.delete(0, END)
                website.insert(0, "Already present")
        except KeyError:
            ## calling two functions one sends email and other save the file locally and returns true or false
            # success = send_email(userdata) and save_file(userdata, SAVE_TO_FOLDER_PATH)

            success = save_file(userdata, SAVE_TO_FOLDER_PATH) #delete after testing

            ## loading newly saved data
            new_user_data = get_data(SAVE_TO_FOLDER_PATH) ## from file import
            new_options = [data for data in new_user_data]
            menu = website_drop_down_menu["menu"]
            menu.delete(0, "end")
            for option in new_options:
                menu.add_command(label=option, command=lambda value=option: website_data_value.set(value))

            ## checks if success or fail
            if success:
                messagebox.showinfo("Success", "Password was saved successfully")
            else:
                messagebox.showerror("Error", "Password could not be saved")


def get_saved_data():
    new_user_data = get_data(SAVE_TO_FOLDER_PATH)
    new_user_selected = website_data_value.get()

    website.delete(0, END)
    email.delete(0, END)
    new_password.delete(0, END)
    if new_user_selected == "Website":
        website.insert(0, "Please select an website")
        email.insert(0, "Please select an website")
        new_password.insert(0, "Please select an website")
    elif new_user_selected == "No data":
        website.insert(0, "No data available")
        email.insert(0, "No data available")
        new_password.insert(0, "No data available")
    else:
        website.insert(0, new_user_selected)
        email.insert(0, new_user_data[new_user_selected]["email"])
        new_password.insert(0, new_user_data[new_user_selected]["password"])
    
    
    
## -----------------------------------------------  UI setup  --------------------------------------------------------
window = Tk()
window.title("Password Generator")
window.config(padx=10, pady=10, bg='#F0F0FF')
window.minsize(width=300, height=400)

## ------ password length ---------
PASSWORD_LENGTH_OPTIONS = ["8", "16", "32"]

password_length_label= Label(text="Password Length: ")
password_length_label.grid(row=1, column=0, pady=5)

#Set the drop_down initial value
password_length_value= StringVar()
password_length_value.set("16")

#Create a dropdown Menu
password_length_drop_down_menu= OptionMenu(window, password_length_value, *PASSWORD_LENGTH_OPTIONS)
password_length_drop_down_menu.config(bg= "#FFFFE4")
password_length_drop_down_menu["menu"].config(bg= "#FFFFF8")
password_length_drop_down_menu.place(x=120, y=1)

save_to_button= Button(text="Save to", bg="#CACAFF", command=set_folder_path)
save_to_button.place(x=250, y=3)

## ------ website saved data ---------
website_data_label= Label(text="Website Data: ")
website_data_label.grid(row=2, column=0, pady=15)

website_options = [data for data in get_data(SAVE_TO_FOLDER_PATH)] ## from import file retriving the data in a list

#Set the drop_down initial value
website_data_value= StringVar()
website_data_value.set("Website")

#Create a dropdown Menu
try:
    website_drop_down_menu= OptionMenu(window, website_data_value, *website_options)
except TypeError:
    website_drop_down_menu= OptionMenu(window, website_data_value, "No data")
website_drop_down_menu.config(bg= "#FFFFE4")
website_drop_down_menu["menu"].config(bg= "#FFFFF8")
website_drop_down_menu.grid(row=2, column=1)

## ------ website ----------------
website_label= Label(text="Website: ")
website_label.grid(row=3, column=0, pady=5)

website = Entry(width=30)
website.grid(row=3, column=1, columnspan=2, pady=5)

## ------ Email ----------------
email_label = Label(text="Email/Username: ")
email_label.grid(row=4, column=0, pady=5)

email = Entry(width=30)
email.grid(row=4, column=1, columnspan=2, pady=5)

## ------ New password -------------
new_password_label= Label(text="Your New Password: ")
new_password_label.grid(row=5, column=0, pady=5)

new_password= Entry(width=30)
new_password.grid(row=5, column=1, pady=5, padx=5)

## ------ password generate button ---------
generate_password_button= Button(text="Generate Password", width=40, bg="#BCBCEE", command=generate_password)
generate_password_button.grid(row= 6, column=0, columnspan=2, pady=5)

## ------ get button ---------
get_data_button= Button(text="Get data", width=40, bg="#BCBCEE", command=get_saved_data)
get_data_button.grid(row= 7, column=0, columnspan=2, pady=5)

## ------ save password button ---------
save_password_button= Button(text="Save Password", width=40, bg="#BCBCEE", command=save_password)
save_password_button.grid(row= 8, column=0, columnspan=2, pady=5)

## ------ save password button ---------
window.mainloop()
