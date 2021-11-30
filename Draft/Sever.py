import socket
import json
import threading
from tkinter import *
from tkinter import Button, Frame, Label
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import ImageTk, Image
import MySQL
from tkinter import filedialog
# '127.0.0.1'
# 192.168.1.3
port = 12345
format = 'utf8'

class HomePage_Server(Frame):  # test chơi chơi
    def __init__(self, main_frame, windows):
        Frame.__init__(self, main_frame)
        self.configure(bg="grey")
        homepage_label = Label(
            master=self, text="SERVER")
        homepage_label.pack()
        frame1 = Frame(master=self, width=100, height=100, bg="red")
        logout_button = Button(master=self, text="Logout", width=12, height=1,
                               bg="blue", fg="white", command=lambda: self.logout_server(windows))
        logout_button.pack()
        frame1.pack()

    def logout_server(self,windows):
        s.close()
        windows.switchPage(loginServer)
        return

def client_side(conn, check_dis):
    while (True):
        try:
            command = conn.recv(1024).decode(format)
            conn.sendall(command.encode(format))
        except:
            pass
        finally:
            if (command == "LOGIN"):
                check_login_client(conn)
            elif(command == "REGISTER"):
                create_account(conn)
                return
            elif(command == "DISCONNECT"):
                check=disconnect_client(conn)
                if (check==True):
                    check_dis=True
                    break
            elif (command == 'DATA'):
                send_data_to_client(conn)
                pass            
    return check

def send_data_to_client(conn):

    filename = conn.recv(1024).decode(format)
    conn.sendall(filename.encode(format))

    data = MySQL.take_data_from_json(filename)
    
    if (data==False):
        conn.sendall("Fail".encode(format))
        conn.recv(1024).decode(format)
        return
    else:
        conn.sendall("Success".encode(format))
        conn.recv(1024).decode(format)
        
    data=data['results']
    for item in data:
        conn.sendall(json.dumps(item).encode(format))
        conn.recv(1024).decode(format)
        
    conn.sendall("done".encode(format))
    conn.recv(1024).decode(format)
    pass

def disconnect_client(conn):
    try:
        conn.sendall("ACCEPT".encode(format))
        conn.recv(1024).decode(format)
        conn.close()
    except:
        print("error")
        return False
    finally:
        return True

def check_SQL(user, psw):
    loginInfo = MySQL.getLoginInfo('client.json')
    for i in loginInfo:
        if (user == i['username']):
            if (psw == i['password']):
                return 1
            else:
                return 0

    return -1


def check_login_client(conn):

    username = conn.recv(1024).decode(format)
    conn.sendall(username.encode(format))

    password = conn.recv(1024).decode(format)
    conn.sendall(password.encode(format))

    check = check_SQL(username, password)

    if (check == 1):
        conn.sendall("SUCCESSFUL".encode(format))
    elif (check == 0):
        conn.sendall("WRONG PASSWORD".encode(format))
    else:
        conn.sendall("USERNAME NOT AVAILABLE".encode(format))

    conn.recv(1024).decode(format)


def create_account(conn):
    username = conn.recv(1024).decode(format)
    conn.sendall(username.encode(format))

    password = conn.recv(1024).decode(format)
    conn.sendall(password.encode(format))

    check = check_SQL(username, password)

    if (check == 1 or check == 0):
        conn.sendall("USERNAME AVAILABLE".encode(format))
    else:
        conn.sendall("CREATE ACCOUNT SUCCESSFUL".encode(format))
        MySQL.add_new_user(username,password,"client.json")

    conn.recv(1024).decode(format)
    return


class registerServer(Frame):
    def __init__(self, main_frame, windows):
        Frame.__init__(self, main_frame)

        self.username_registration = StringVar()
        self.password_registration = StringVar()
        self.password_r_registration = StringVar()

        self.configure(bg="aliceblue")

        self.register_mana = Frame(master=self)
        self.register_mana.configure(bg="aliceblue")
        self.register_mana.pack()

        login_label = Label(master=self.register_mana, text="REGISTER",
                            bg="aliceblue", width="17", height="2", fg="darkblue", font='Tahoma 19 bold')
        login_label.pack()

        username_label = Label(master=self.register_mana, text="Username *",
                               bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        username_label.pack()
        username_entry_registration = Entry(
            master=self.register_mana, highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1, width=40, textvariable=self.username_registration)
        username_entry_registration.pack()

        password_label = Label(master=self.register_mana, text="Password *",
                               bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        password_label.pack()
        password_entry_registration = Entry(
            master=self.register_mana, show='*', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1, width=40, textvariable=self.password_registration)
        password_entry_registration.pack()

        password_r_label = Label(
            master=self.register_mana, text="Re-enter password *", bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        password_r_label.pack()
        password_r_entry_registration = Entry(
            master=self.register_mana, show='*', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1, width=40, textvariable=self.password_r_registration)
        password_r_entry_registration.pack()

        register_button = Button(master=self.register_mana, text="Register", width=12,
                                 height=1, bg="lightblue", fg="black", command=lambda: self.Register_handle(windows))
        register_button.pack(pady=10)

        back_button = Button(master=self.register_mana, text="Back", width=12, height=1,
                             bg="lightblue", fg="black", command=lambda: windows.switchPage(loginServer))
        back_button.pack()

    def Register_handle(self, windows):

        if(self.username_registration.get() == "" or self.password_registration.get() == "" or self.password_r_registration.get() == ""):
            messagebox.showerror(
                'Error', "PLEASE ENTER ALL INFORMATION REQUIRE")

        elif(self.password_registration.get() != self.password_r_registration.get()):
            messagebox.showerror('Error', "RE-PASSWORD DOESN'T MATCH")

        else:

            loginInfo = MySQL.getLoginInfo("server.json")

            for i in loginInfo:
                if (self.username_registration.get() == i[0]):
                    messagebox.showerror('Error', "USERNAME AVAILABLE")
                    return

            MySQL.add_new_user(str(self.username_registration.get()), str(
                self.password_registration.get()), "server.json")
            messagebox.showinfo('SUCCESSFUL', "CREATE ACCOUNT SUCCESSFUL")
            windows.switchPage(loginServer)
        return


class loginServer(Frame):
    def __init__(self, main_frame, windows):

        Frame.__init__(self, main_frame)

        self.username = StringVar()
        self.password = StringVar()
        self.IP = StringVar()
        self.configure(bg="aliceblue")

        frame_mana = Frame(master=self)
        frame_mana.configure(bg="aliceblue")
        frame_mana.pack()

        

        login_label = Label(master=frame_mana, text="LOGIN", bg="aliceblue",
                            width="17", height="2", font='Tahoma 19 bold', fg="darkblue")
        login_label.pack()

        """ img = ImageTk.PhotoImage(Image.open("Image/Logo_Start.png"))
        imglabel = Label(frame_mana, image=img, bg="aliceblue", width=30, height=40).pack() """

        username_label = Label(master=frame_mana, text="Username *",
                               bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        username_label.pack()
        user_entry = Entry(master=frame_mana,
                           textvariable=self.username, width=40, bg='white', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        user_entry.pack()

        password_label = Label(master=frame_mana, text="Password *",
                               bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        password_label.pack()
        password_entry = Entry(master=frame_mana, show='*',
                               textvariable=self.password, width=40, bg='white', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        password_entry.pack()

        IP_label = Label(master=frame_mana, text="Enter Your IP Computer*",
                         bg="aliceblue", fg="darkblue", font='Tahoma 9 bold')
        IP_label.pack()
        IP_entry = Entry(master=frame_mana,
                         textvariable=self.IP, width=40, bg='white', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        IP_entry.pack()

        login_button = Button(master=frame_mana, text="Login", width=12, height=1,
                              fg="black", bg="lightblue", highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1, command=lambda: self.Login_handle(windows))
        login_button.pack(pady=10)
        register_button = Button(master=frame_mana, text="Register", width=12, height=1,
                                 fg="black", bg="lightblue", highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1, command=lambda: windows.switchPage(registerServer))
        register_button.pack()

    def Login_handle(self, windows):

        user = self.username.get()
        psw = self.password.get()

        if (user == "" or psw == ""):
            messagebox.showerror(
                'Error', "PLEASE ENTER ALL INFORMATION REQUIRE")
            return False

        loginInfo = MySQL.getLoginInfo("server.json")

        for i in loginInfo:
            if (user == i['username']):
                if (psw == i['password']):

                    messagebox.showinfo('Error', "LOGIN SUCCESSFUL")

                    create_server(self.IP.get())

                    windows.switchPage(HomePage_Server)
                    return True

                else:
                    messagebox.showerror('Error', "WRONG PASSWORD")
                    return False

        messagebox.showerror('Error', "NOT EXIST USERNAME")
        return False


class serverGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x300+300+100")
        # self.resizable(width=False,height=False)
        self.title("SERVER LOGIN")
        self.iconphoto(False, PhotoImage(file='Image/Server_icon.png'))

        self.main_frame = Frame(master=self, bg="grey")
        self.main_frame.pack(fill='both', expand=True)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.dictionary_frame = {}  # dictionary để lưu trữ những frame của server
        self.list_frame = (loginServer, registerServer, HomePage_Server)

        self.add_frame()

        self.dictionary_frame[loginServer].tkraise()  # switch between frame

    def add_frame(self):
        for i in self.list_frame:
            frame = i(self.main_frame, self)
            frame.grid(row=0, column=0, sticky="news")
            self.dictionary_frame[i] = frame

    def switchPage(self, pageName):
        self.dictionary_frame[pageName].tkraise()

    def clear_widget(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()


def create_connection(s):
    try:
        while True:
            conn, addr = s.accept()
            print("client connected")
            clientThread = threading.Thread(target=client_side, args=(conn, addr))
            clientThread.daemon = True
            clientThread.start()
            print("end client_side")
            if(clientThread=="Break"): 
                print("finish client session")
                break

    except:
        s.close()

    finally:
        s.close()


def create_server(SERVER):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER, port))
    s.listen()
    print("Waiting Client")
    clientThread = threading.Thread(target=create_connection, args=(s,))
    clientThread.daemon = True
    clientThread.start()
##########################################################

clock=threading.Thread(target=MySQL.alarm, args=())
clock.daemon = True
clock.start()

root = serverGUI()
root.mainloop()
