from tkinter import *
import os
from PIL import ImageTk,Image
import tkinter

global root
root=Tk()
root.geometry("500x300+300+300")
root.resizable(width=False,height=False)

def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()

def loginUI():

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    frame = Frame(master=root,relief=RAISED)
    frame.grid(row=0,column=0,padx=170,pady=10)

    login_label=Label(master=frame,text="LOGIN",bg="orange",width="15",height="2", font=15)
    login_label.grid(row=0,column=0) 

    username_label = Label(master=frame, text="Username *")
    username_label.grid(row=1,column=0) 
    user_entry=Entry(master=frame,textvariable=username)
    user_entry.grid(row=2,column=0)

    password_label = Label(master=frame, text="Password *")
    password_label.grid(row=3,column=0)
    password_entry=Entry(master=frame,show = '*',textvariable=password)
    password_entry.grid(row=4,column=0)

    login_button=Button(master=frame,text="Login",width=12, height=1,bg="blue",command=Login_handle)
    login_button.grid(row=7,column=0,pady=10)
    register_button=Button(master=frame,text="Register",width=12, height=1,bg="blue",command=lambda: Register_button(frame))
    register_button.grid(row=8,column=0)

    return frame

def server():
    root.title("SERVER LOGIN")
    root.iconphoto(False, PhotoImage(file='Image/Server_icon.png'))
    frame = loginUI()
    IP_label = Label(master=frame, text="Create a IP Server*")
    IP_label.grid(row=5,column=0)
    IP_entry=Entry(master=frame)
    IP_entry.grid(row=6,column=0)
    root.mainloop()
    return
    
def client():
    root.title("CLIENT LOGIN")
    root.iconphoto(False, PhotoImage(file='Image/Clients_icon.png'))
    frame = loginUI()
    IP_label = Label(master=frame, text="IP Server*")
    IP_label.grid(row=5,column=0)
    IP_entry=Entry(master=frame)
    IP_entry.grid(row=6,column=0)
    root.mainloop()
    return

def Back_button(frame,function):
    clear_frame(frame)
    return function

def Register_button(frame):
    clear_frame(frame)

    global username_registration
    global password_registration
    global password_r_registration
    global username_entry_registration
    global password_entry_registration
    global password_r_entry_registration
    username_registration = StringVar()
    password_registration = StringVar()
    password_r_registration=StringVar()

    frame_register = Frame(master=root,relief=RAISED)
    frame_register.grid(row=0,column=0,padx=170,pady=10)

    login_label=Label(master=frame_register,text="REGISTER",bg="orange",width="15",height="2",font=15)
    login_label.grid(row=0,column=0) 

    username_label = Label(master=frame_register, text="Username *")
    username_label.grid(row=1,column=0) 
    username_entry_registration=Entry(master=frame_register,textvariable=username_registration)
    username_entry_registration.grid(row=2,column=0)

    password_label = Label(master=frame_register, text="Password *")
    password_label.grid(row=3,column=0)
    password_entry_registration=Entry(master=frame_register,show='*',textvariable=password_registration)
    password_entry_registration.grid(row=4,column=0)

    password_r_label = Label(master=frame_register, text="Re-enter password *")
    password_r_label.grid(row=5,column=0)
    password_r_entry_registration=Entry(master=frame_register,show='*',textvariable=password_r_registration)
    password_r_entry_registration.grid(row=6,column=0)

    register_button=Button(master=frame_register,text="Register",width=12, height=1,bg="blue")
    register_button.grid(row=7,column=0,pady=10)
    back_button=Button(master=frame_register,text="Back",width=12, height=1,bg="blue",command=lambda: Back_button(frame_register,loginUI()))
    back_button.grid(row=8,column=0)
    return

def Login_handle():
    username_check=username.get()
    password_check=password.get()

    f = open("Data_Test/user_pass.txt", "r")
    if (f.readline().replace('\n', '')==username_check):
        print("success")
    else:
        print("failure")
    return

def Register_handle():
        
    return

client()

