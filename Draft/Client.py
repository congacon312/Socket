import socket
import threading
from tkinter import *
from tkinter import Button, Frame, Label
from tkinter import messagebox
import MySQL 
#'192.168.1.3'
port = 12345
format='utf8'
class HomePage_Client(Frame):#test chơi chơi
    def __init__(self,main_frame,windows):
        Frame.__init__(self,main_frame)
        self.configure(bg="grey")
        homepage_label = Label(master = self,text="CURRENT CLIENT ON THE SERVER")
        homepage_label.pack()
        frame1 = Frame(master=self, width=100, height=100, bg="red")
        logout_button=Button(master=self,text="Logout",width=12, height=1,bg="blue",fg="white",command=lambda: windows.switchPage(loginClient))
        logout_button.pack()
        frame1.pack()

class registerClient(Frame):
    def __init__(self,main_frame,windows):
        Frame.__init__(self,main_frame)

        self.username_registration = StringVar()
        self.password_registration = StringVar()
        self.password_r_registration=StringVar()
        self.configure(bg="orange")

        self.register_manager=Frame(master=self)
        self.register_manager.pack()

        login_label=Label(master=self.register_manager,text="REGISTER",bg="red",width="15",height="2",font=15)
        login_label.pack()

        username_label = Label(master=self.register_manager, text="Username *")
        username_label.pack()
        username_entry_registration=Entry(master=self.register_manager,textvariable=self.username_registration)
        username_entry_registration.pack()

        password_label = Label(master=self.register_manager, text="Password *")
        password_label.pack()
        password_entry_registration=Entry(master=self.register_manager,show='*',textvariable=self.password_registration)
        password_entry_registration.pack()

        password_r_label = Label(master=self.register_manager, text="Re-enter password *")
        password_r_label.pack()
        password_r_entry_registration=Entry(master=self.register_manager,show='*',textvariable=self.password_r_registration)
        password_r_entry_registration.pack()

        register_button=Button(master=self.register_manager,text="Register",width=12, height=1,bg="blue",fg="white",command=lambda: self.Register_handle(windows))
        register_button.pack(pady=10)
        back_button=Button(master=self.register_manager,text="Back",width=12, height=1,bg="blue",fg="white",command=lambda: windows.switchPage(loginClient))
        back_button.pack()

    def Register_handle(self,windows):

        if(self.username_registration.get()=="" or self.password_registration.get()=="" or self.password_r_registration.get()==""):
            messagebox.showerror('Error', 'PLEASE ENTER ALL INFORMATION REQUIRE!')
        
        elif(self.password_registration.get()!=self.password_r_registration.get()):
            messagebox.showerror('Error', "RE-PASSWORD DOESN'T MATCH")
        else:

            s.sendall("REGISTER".encode(format))
            s.recv(1024).decode(format)

            s.sendall(self.username_registration.get().encode(format))
            s.recv(1024).decode(format)

            s.sendall(self.password_registration.get().encode(format))
            s.recv(1024).decode(format)

            check_register = s.recv(1024).decode(format)
            s.sendall(check_register.encode(format))

            if (check_register=="CREATE ACCOUNT SUCCESSFUL"):
                windows.switchPage(loginClient)
                messagebox.showinfo('SUCCESSFUL', check_register)
            else:
                messagebox.showerror('Error', check_register)

        return False

class loginClient(Frame):
    def __init__(self,main_frame,windows):
        Frame.__init__(self,main_frame)
        self.username = StringVar()
        self.password = StringVar()
        self.IP = StringVar()

        self.configure(bg="orange")

        self.login_frame_manager = Frame(master=self)
        self.login_frame_manager.pack()

        login_label=Label(master=self.login_frame_manager,text="LOGIN",bg="red",width="15",height="2", font=15)
        login_label.pack()

        username_label = Label(master=self.login_frame_manager, text="Username *")
        username_label.pack()
        user_entry=Entry(master=self.login_frame_manager,textvariable= self.username)
        user_entry.pack()

        password_label = Label(master=self.login_frame_manager, text="Password *")
        password_label.pack()
        password_entry=Entry(master=self.login_frame_manager,show = '*',textvariable=self.password)
        password_entry.pack()

        IP_label = Label(master=self.login_frame_manager, text="IP Server*")
        IP_label.pack()
        IP_entry=Entry(master=self.login_frame_manager,textvariable=self.IP)
        IP_entry.pack()

        login_button=Button(master=self.login_frame_manager,text="Login",width=12, height=1,fg="white",bg="blue",command=lambda: self.Login_handle(windows))#,command=lambda: self.Login_handle(windows)
        login_button.pack(pady=10)
        register_button=Button(master=self.login_frame_manager,text="Register",width=12, height=1,fg="white",bg="blue",command=lambda: windows.switchPage(registerClient))
        register_button.pack()

    def Login_handle(self,windows):
        user=self.username.get()
        psw=self.password.get()
        IP=self.IP.get()

        if (user=="" or psw=="" or IP==""):
            messagebox.showerror('Error', 'PLEASE ENTER ALL INFORMATION REQUIRE!')
        else:
            global s
            try:
                s=connect_to_server(IP)

                s.sendall("LOGIN".encode(format))
                s.recv(1024).decode(format)

                s.sendall(user.encode(format))
                s.recv(1024).decode(format)

                s.sendall(psw.encode(format))
                s.recv(1024).decode(format)

                check_log = s.recv(1024).decode(format)
                s.sendall(check_log.encode(format))

                if (check_log=="SUCCESSFUL"):
                    messagebox.showinfo('Error', check_log)
                    windows.switchPage(HomePage_Client)
                else:
                    messagebox.showerror('Error', check_log)
    
            except:
                messagebox.showerror('Error', "CAN'T CONNECT TO IP SERVER ! PLEASE CHECK IP.")
        return False
class clientGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x300+300+300")
        self.title("CLIENT LOGIN")
        self.iconphoto(False, PhotoImage(file='Image/Clients_icon.png'))

        self.main_frame=Frame(master=self,bg="grey")
        self.main_frame.pack(fill='both', expand = True)
        
        self.main_frame.rowconfigure(0, weight=1)  
        self.main_frame.columnconfigure(0, weight=1)

        self.dictionary_frame={} #dictionary để lưu trữ những frame của server
        self.list_frame = (loginClient,registerClient,HomePage_Client)

        self.add_frame()
        
        self.dictionary_frame[loginClient].tkraise() #switch between frame

    def add_frame(self):
        for i in self.list_frame:
            frame=i(self.main_frame,self)
            frame.grid(row=0,column=0,sticky="news")
            self.dictionary_frame[i]=frame

    def switchPage(self,pageName):
        self.dictionary_frame[pageName].tkraise()

    def clear_widget(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

def connect_to_server(SERVER):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, port))
    return s
      
####################################################
client = clientGUI()
client.mainloop()