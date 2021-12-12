import socket
import json
import ipaddress
import threading
from tkinter import *
from tkinter import Button, Frame, Label
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import ImageTk, Image
import MySQL
from tkinter import filedialog
from datetime import datetime
# '127.0.0.1'
# 192.168.1.3
# 192.168.1.8

format = 'utf8'

NO_ACCOUNT = "no-account"

notification = []
Live_Account = []
id = []
address = []
# ----------------------------------------------------------------function--------------------------------


def Check_LiveAccount(username):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[(parse+1):]
        if parse_check == username:
            return False
    return True


def Remove_LiveAccount(conn: socket.socket, username):
    if username != NO_ACCOUNT:
        row = StringVar()
        for row in Live_Account:
            if row.find(str(username)) != -1:
                Live_Account.remove(row)
                id.remove(str(username))
                address.remove(str(conn.getsockname()))


def addNotification(conn: socket.socket, username, OPTION):
    now = datetime.now()

    notification.append(str(now) + " - " +
                        str(conn.getsockname()) + " - " + str(username) + " - " + str(OPTION))


def client_side(conn, check_dis):
    username = None

    while (True):
        try:
            command = conn.recv(1024).decode(format)
            conn.sendall(command.encode(format))
            if (command == "LOGIN"):
                username = check_login_client(conn)

            elif(command == "REGISTER"):
                create_account(conn)

            elif(command == "DISCONNECT"):
                addNotification(conn, "Client", "DISCONNECT")
                check = disconnect_client(conn, username)
                if (check == True):
                    print("end threading")
                    check_dis = 'break'
                    break
            
            elif (command == 'DATA'):
                addNotification(conn, username, "SEARCH")
                send_data_to_client(conn)

            elif (command == "CONNECT"):
                addNotification(conn, "Unknown client", "CONNECT")
            
            elif (command == 'CLOSE WINDOW'):
                Remove_LiveAccount(conn, username)
                addNotification(conn, username, "DISCONNECT")
                check = disconnect_client(conn, username)
                if (check == True):
                    print("end threading")
                    check_dis = 'break'
                    break

            elif (command == 'LOGOUT'):
                Remove_LiveAccount(conn, username)
                addNotification(conn, username, "LOGOUT")

        except:
            messagebox.showerror('Error', "Client isn't respond")
    return check_dis


def send_data_to_client(conn):

    filename = conn.recv(1024).decode(format)
    conn.sendall(filename.encode(format))

    data = MySQL.take_data_from_json(filename)

    if (data == False):
        conn.sendall("Fail".encode(format))
        conn.recv(1024).decode(format)
        return
    else:
        conn.sendall("Success".encode(format))
        conn.recv(1024).decode(format)

    data = data['results']
    for item in data:
        conn.sendall(json.dumps(item).encode(format))
        conn.recv(1024).decode(format)

    conn.sendall("done".encode(format))
    conn.recv(1024).decode(format)
    pass


def disconnect_client(conn, username):
    try:
        conn.sendall("ACCEPT".encode(format))
        conn.recv(1024).decode(format)
        conn.close()
        return True
    except:
        print("error")
        return False


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
    USER = NO_ACCOUNT

    username = conn.recv(1024).decode(format)
    conn.sendall(username.encode(format))

    password = conn.recv(1024).decode(format)
    conn.sendall(password.encode(format))

    check = check_SQL(username, password)

    if (check == 1):
        conn.sendall("SUCCESSFUL".encode(format))
        id.append(username)
        address.append(str(conn.getsockname()))
        account = str(address[address.__len__()-1]) + \
            "-"+str(id[id.__len__()-1])
        Live_Account.append(account)
        addNotification(conn, username, "LOG IN")
        USER = username

    elif (check == 0):
        conn.sendall("WRONG PASSWORD".encode(format))
    else:
        conn.sendall("USERNAME NOT AVAILABLE".encode(format))

    conn.recv(1024).decode(format)

    return USER


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
        MySQL.add_new_user(username, password, "Data/client.json")

    conn.recv(1024).decode(format)
    return

# ----------------------------------------------------Class ----------------------------------------------------------------


class ConnectPage(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x200+300+300")
        self.title("SERVER")
        #self.iconphoto(False, PhotoImage(file='Image/Clients_icon.png'))
        self.IP = StringVar()
        self.port = StringVar()

        self.connect_frame = Frame(master=self)
        self.connect_frame.pack(expand=True)

        self.IP_Label = Label(master=self.connect_frame,
                              text="IP Server: ", font='Tahoma 12')
        self.IP_Label.grid(row=0, column=0)

        self.IP_entry = Entry(master=self.connect_frame,
                              borderwidth=2, textvariable=self.IP)
        self.IP_entry.grid(row=0, column=1, columnspan=2)
        self.IP_entry.focus()

        self.port_label = Label(master=self.connect_frame,
                                text="Port", font='Tahoma 12')
        self.port_label.grid(row=1, column=0, pady=10)

        self.port_entry = Entry(master=self.connect_frame,
                                borderwidth=2, textvariable=self.port)
        self.port_entry.grid(row=1, column=1, columnspan=2)

        self.button_connect = Button(master=self.connect_frame, text="Create",
                                     width=12, relief='ridge', borderwidth=3, command=self.create_server)
        self.button_connect.grid(row=2, column=0, padx=10)

        self.button_connect = Button(master=self.connect_frame, text="Exit",
                                     width=12, relief='ridge', borderwidth=3, command=self.destroy)
        self.button_connect.grid(row=2, column=1)

    def create_connection(self):
        try:
            while True:
                conn, addr = self.s.accept()
                print("client connected")
                check_dis = ""
                clientThread = threading.Thread(
                    target=client_side, args=(conn, check_dis))
                clientThread.daemon = True
                clientThread.start()
                print(check_dis)
                if (check_dis == "break"):
                    print("finish client session")
                    conn.close()
                    break
        except:
            print("error: create_connection")
            pass

    def create_server(self):
        try:
            if (self.validate_ip_address() == False):
                messagebox.showerror(
                    'Error', "CAN'T CREATE SERVER WITH THIS IP !!! TRY ANOTHER IP.")
                return

            clock = threading.Thread(
                target=MySQL.alarm, args=())  # hẹn giờ cập nhập
            clock.daemon = True
            clock.start()

            global HOST
            global port
            HOST=self.IP.get()
            port=self.port.get()

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.IP.get(), int(self.port.get())))
            self.s.listen()
            print("Waiting Client")

            clientThread = threading.Thread(
                target=self.create_connection, args=())
            clientThread.daemon = True
            clientThread.start()

            self.destroy()
            gui = serverGUI()
            gui.mainloop()

        except:
            print("can't connect to server")
            return False

    def validate_ip_address(self):
        try:
            ipaddress.ip_address(self.IP.get())
            return True
        except ValueError:
            return False


class HomePage_Server(Frame):  # test chơi chơi
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="aliceblue")

        label_title = Label(self, text="\nACTIVE ACCOUNT ON SEVER\n",
                            font="Tahoma 22 bold", fg='#20639b', bg="aliceblue").pack()
        label_ipAndPort = Label(self, text="               HOST: " + str(HOST) + "                                                                                        " +
                                "PORT: " + str(port), bg='aliceblue', fg='blue', font="Tahoma 10 bold")
        label_ipAndPort.pack(pady=10)

        self.home = Frame(self, bg="aliceblue")

        self.notification = Frame(self.home)
        self.connect = Frame(self.home)
        label_notification = Label(
            self.home, text="NOTIFICATION", bg="aliceblue", fg='blue', font="Tahoma 11 bold")
        label_notification.grid(row=0, column=0)
        label_Account = Label(
            self.home, text="LIVE ACCOUNT", bg="aliceblue", fg='blue', font="Tahoma 11 bold")
        label_Account.grid(row=0, column=1)

        self.dataAccount = Listbox(self.connect, height=22,
                                   width=50,
                                   bg='floral white',
                                   activestyle='dotbox',
                                   font="Helvetica 10",
                                   fg='#20639b', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)

        self.dataNotification = Listbox(self.notification, height=22,
                                        width=70,
                                        bg='floral white',
                                        activestyle='dotbox',
                                        font="Helvetica 10",
                                        fg='#20639b', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)

        button_log = Button(self, text="REFRESH", bg="#20639b",
                            fg='floral white', command=self.Update_Client)
        button_back = Button(self, text="LOG OUT", bg="#20639b",
                             fg='floral white', command=lambda: controller.switchPage(loginServer))

        button_log.pack(side=BOTTOM, pady=5)
        button_log.configure(width=10)
        button_back.pack(side=BOTTOM, pady=5)
        button_back.configure(width=10)

        self.notification.grid(row=1, column=0)
        self.connect.grid(row=1, column=1)
        self.home.pack_configure()

        self.scrollAccount = Scrollbar(self.connect)
        self.scrollAccount.pack(side=RIGHT, fill=BOTH)
        self.dataAccount.config(yscrollcommand=self.scrollAccount.set)

        self.scrollAccount.config(command=self.dataAccount.yview)
        self.dataAccount.pack()

        self.scrollNotification = Scrollbar(self.notification)
        self.scrollNotification.pack(side=RIGHT, fill=BOTH)
        self.dataNotification.config(
            yscrollcommand=self.scrollNotification.set)

        self.scrollNotification.config(command=self.dataNotification.yview)
        self.dataNotification.pack()

    def Update_Client(self):
        self.dataAccount.delete(0, len(Live_Account))
        for i in range(len(Live_Account)):
            self.dataAccount.insert(i, Live_Account[i])

        self.dataNotification.delete(0, len(notification))
        for i in range(len(notification)):
            self.dataNotification.insert(i, notification[i])


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
                if (self.username_registration.get() == i['username']):
                    messagebox.showerror('Error', "USERNAME AVAILABLE")
                    return

            MySQL.add_new_user(str(self.username_registration.get()), str(
                self.password_registration.get()), "Data/server.json")
            messagebox.showinfo('SUCCESSFUL', "CREATE ACCOUNT SUCCESSFUL")
            windows.switchPage(loginServer)
        return


class loginServer(Frame):
    def __init__(self, main_frame, windows):

        Frame.__init__(self, main_frame)

        self.username = StringVar()
        self.password = StringVar()
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
        #self.iconphoto(False, PhotoImage(file='Image/Sever_icon.png'))

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
        if (pageName == HomePage_Server):
            self.geometry("960x640+10+10")
        elif (pageName == loginServer and pageName == registerServer):
            self.geometry("500x300+300+300")
        self.dictionary_frame[pageName].tkraise()

    def clear_widget(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()


##########################################################

root = ConnectPage()
root.mainloop()
