import socket
import json
from sys import argv
import threading
from tkinter import *
from tkinter import Button, Frame, Label
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import *
import time

# '192.168.1.3'
format = 'utf8'

NO_ACCOUNT = "no-account"

class ConnectPage(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x200+300+300")
        self.title("CLIENT")
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

        self.button_connect = Button(master=self.connect_frame, text="Connect",
                                     width=12, relief='ridge', borderwidth=3, command=self.connect_to_server)
        self.button_connect.grid(row=2, column=0, padx=10)

        self.button_connect = Button(master=self.connect_frame, text="Exit",
                                     width=12, relief='ridge', borderwidth=3, command=self.destroy)
        self.button_connect.grid(row=2, column=1)

    def connect_to_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.IP.get(), int(self.port.get())))
            print("connected to server")
            self.destroy()

            s.sendall("CONNECT".encode(format))
            s.recv(1024).decode(format)

            login = clientGUI(s)
            login.mainloop()
        except:
            messagebox.showerror('Error', "Can't connect to server")
            print("can't connect to server")


class HomePage_Client(Frame):
    def __init__(self, main_frame, windows, s):

        Frame.__init__(self, main_frame)
        #windows.resizable(width=False, height=False)
        self.configure(bg="white")
        homepage_label = Label(master=self, text="VIETNAM CURRENCY RATE",
                               font='Tahoma 19 bold', bg="white", relief='groove', borderwidth=5)
        homepage_label.pack(fill=BOTH)

        self.HomePage_manager = Frame(
            master=self, bg="white", relief='ridge', borderwidth=5)
        self.HomePage_manager.pack(fill=BOTH, side=LEFT)

        self.table_manager = Frame(
            master=self, bg="grey", relief='ridge', borderwidth=5, height=900)
        self.table_manager.pack(fill=BOTH, side=LEFT, expand=1)
        #####
        self.my_canvas = Canvas(
            self.table_manager, scrollregion=(0, 0, 500, 500))
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(
            master=self.table_manager, orient=VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(
            scrollregion=self.my_canvas.bbox("all")))

        self.second_frame = Frame(self.my_canvas)

        self.my_canvas.create_window(
            (0, 0), window=self.second_frame, anchor="nw")
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        #####
        self.width = 20

        global temp_label
        temp_label = Label(master=self.HomePage_manager,
                           font='Tahoma 12', bg="white")
        temp_label.grid(row=0, column=0, pady=10)

        self.date_label = Label(
            master=self.HomePage_manager, text="DATE", font='Tahoma 10', bg="white")
        self.date_label.grid(row=1, column=0)

        self.cal = DateEntry(master=self.HomePage_manager,
                             width=15, foreground="grey", date_pattern='dd/mm/yyyy')
        self.cal.grid(row=2, column=0, pady=10, padx=5)


        self.date_label = Label(
            master=self.HomePage_manager, text="CURRENCY", font='Tahoma 10', bg="white")
        self.date_label.grid(row=3, column=0)

        self.option_list = []
        self.Combo = ttk.Combobox(self.HomePage_manager, values=self.option_list, state="readonly", width="15")
        self.Combo.set("Choose currency")
        self.Combo.grid(row=4, column=0, pady=10)

        search_button = Button(master=self.HomePage_manager, text="Search",
                               width=10, command=lambda: self.show_data(s, windows))
        search_button.grid(row=5, column=0, pady=10)

        self.reset = Button(master=self.HomePage_manager, text="Reset", width=10,
                            command=lambda: self.reset_button(s, windows), state=DISABLED)
        self.reset.grid(row=6, column=0)

        logout_button = Button(master=self.HomePage_manager, text="Logout",
                               width=10, command=lambda:  self.logout_button(s,windows))
        logout_button.grid(row=7, column=0, pady=100)

    def show_data(self, s,windows):
        try:

            s.sendall("DATA".encode(format))
            s.recv(1024).decode(format)

            filename = self.cal.get_date().strftime("%d-%m-%Y")+'.json'
            s.sendall(filename.encode(format))
            s.recv(1024).decode(format)

            mess = s.recv(1024).decode(format)
            s.sendall(mess.encode(format))

            if (mess == "Fail"):
                messagebox.showerror(
                    'Error', "Not found data on "+self.cal.get_date().strftime("%d-%m-%Y"))
                return

            windows.clear_widget(self.second_frame)

            self.cash = Label(master=self.second_frame, text='Buy Cash',
                              fg='blue', font='Tahoma 12', bg="white", width=self.width)
            self.cash.grid(row=0, column=0, padx=1, pady=1)
            windows.update()
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

            self.transfer = Label(master=self.second_frame, text='Buy Transfer',
                                  fg='blue', font='Tahoma 12', bg="white", width=self.width)
            self.transfer.grid(row=0, column=1, padx=1, pady=1)
            windows.update()
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

            self.currency = Label(master=self.second_frame, text='Currency',
                                  fg='blue', font='Tahoma 12', bg="white", width=self.width)
            self.currency.grid(row=0, column=2, padx=1, pady=1)
            windows.update()
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

            self.sell = Label(master=self.second_frame, text='Sell',
                              font='Tahoma 12', fg='blue', bg="white", width=self.width)
            self.sell.grid(row=0, column=3, padx=1, pady=1)
            windows.update()
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

            self.data = []
            while(True):
                mess = s.recv(1024).decode(format)
                s.sendall(mess.encode(format))
                if (mess == 'done'):
                    break
                data = json.loads(mess)
                self.data.append(data)

            i = 1

            if (self.Combo.get() != "Choose currency"):
                for item in self.data:
                    if (item['currency'] == self.Combo.get()):

                        data_label = Label(
                            master=self.second_frame, text=item['buy_cash'], font='Tahoma 12', bg="white", width=self.width)
                        data_label.grid(row=i, column=0, padx=1, pady=1)
                        windows.update()
                        self.my_canvas.configure(
                            scrollregion=self.my_canvas.bbox("all"))

                        data_label = Label(
                            master=self.second_frame, text=item['buy_transfer'], font='Tahoma 12', bg="white", width=self.width)
                        data_label.grid(row=i, column=1, padx=1, pady=1)
                        windows.update()
                        self.my_canvas.configure(
                            scrollregion=self.my_canvas.bbox("all"))

                        data_label = Label(
                            master=self.second_frame, text=item['currency'], font='Tahoma 12', bg="white", width=self.width)
                        data_label.grid(row=i, column=2, padx=1, pady=1)
                        windows.update()
                        self.my_canvas.configure(
                            scrollregion=self.my_canvas.bbox("all"))

                        data_label = Label(
                            master=self.second_frame, text=item['sell'], font='Tahoma 12', bg="white", width=self.width)
                        data_label.grid(row=i, column=3, padx=1, pady=1)
                        windows.update()
                        self.my_canvas.configure(
                            scrollregion=self.my_canvas.bbox("all"))

            else:
                for item in self.data:
                    data_label = Label(
                        master=self.second_frame, text=item['buy_cash'], font='Tahoma 12', bg="white", width=self.width)
                    data_label.grid(row=i, column=0, padx=1, pady=1)
                    windows.update()
                    self.my_canvas.configure(
                        scrollregion=self.my_canvas.bbox("all"))

                    data_label = Label(
                        master=self.second_frame, text=item['buy_transfer'], font='Tahoma 12', bg="white", width=self.width)
                    data_label.grid(row=i, column=1, padx=1, pady=1)
                    windows.update()
                    self.my_canvas.configure(
                        scrollregion=self.my_canvas.bbox("all"))

                    data_label = Label(
                        master=self.second_frame, text=item['currency'], font='Tahoma 12', bg="white", width=self.width)
                    self.option_list.append(item['currency'])
                    data_label.grid(row=i, column=2, padx=1, pady=1)
                    windows.update()
                    self.my_canvas.configure(
                        scrollregion=self.my_canvas.bbox("all"))

                    data_label = Label(
                        master=self.second_frame, text=item['sell'], font='Tahoma 12', bg="white", width=self.width)
                    data_label.grid(row=i, column=3, padx=1, pady=1)
                    windows.update()
                    self.my_canvas.configure(
                        scrollregion=self.my_canvas.bbox("all"))

                    i += 1
                self.Combo['values'] = self.option_list

            self.reset['state'] = 'normal'
        except:
            messagebox.showerror('Error', "Server isn't respond")

    def reset_button(self,s,windows):
        self.Combo.set("Choose currency")
        self.show_data(s, windows)

    def logout_button(self,s,windows):
        try:
            s.sendall("LOGOUT".encode(format))
            s.recv(1024).decode(format)
            windows.switchPage(loginClient)
        except:
            messagebox.showerror('Error', "Server isn't respond")



class registerClient(Frame):
    def __init__(self, main_frame, windows, s):
        Frame.__init__(self, main_frame)

        self.username_registration = StringVar()
        self.password_registration = StringVar()
        self.password_r_registration = StringVar()
        self.configure(bg="#0099CC")

        self.register_manager = Frame(master=self)
        self.register_manager.configure(bg="#0099CC")
        self.register_manager.pack()

        login_label = Label(master=self.register_manager, text="REGISTER", bg="#0099CC",
                            width="15", height="2", fg="aliceblue", font='Tahoma 21 bold')
        login_label.pack()

        username_label = Label(master=self.register_manager, text="Username *",
                               bg="#0099CC", fg="aliceblue", font='Tahoma 12 bold')
        username_label.pack()
        username_entry_registration = Entry(master=self.register_manager, textvariable=self.username_registration,
                                            width=50, bg='beige',  highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        username_entry_registration.pack()
        username_entry_registration.focus()

        password_label = Label(master=self.register_manager, text="Password *",
                               bg="#0099CC", fg="aliceblue", font='Tahoma 12 bold')
        password_label.pack()
        password_entry_registration = Entry(
            master=self.register_manager, show='*', textvariable=self.password_registration, width=50, bg='beige',  highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        password_entry_registration.pack()

        password_r_label = Label(
            master=self.register_manager, text="Re-enter password *", bg="#0099CC", fg="aliceblue", font='Tahoma 12 bold')
        password_r_label.pack()
        password_r_entry_registration = Entry(
            master=self.register_manager, show='*', textvariable=self.password_r_registration, width=50, bg='beige',  highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        password_r_entry_registration.pack()

        register_button = Button(master=self.register_manager, text="Register", width=12,
                                 height=1, bg="#666699", fg="white", command=lambda: self.Register_handle(windows, s))
        register_button.pack(pady=10)
        back_button = Button(master=self.register_manager, text="Back", width=12, height=1,
                             bg="#666699", fg="white", command=lambda: windows.switchPage(loginClient))
        back_button.pack()

    def Register_handle(self, windows, s):

        if(self.username_registration.get() == "" or self.password_registration.get() == "" or self.password_r_registration.get() == ""):
            messagebox.showerror(
                'Error', 'PLEASE ENTER ALL INFORMATION REQUIRE!')

        elif(self.password_registration.get() != self.password_r_registration.get()):
            messagebox.showerror('Error', "RE-PASSWORD DOESN'T MATCH")
        else:

            try:
                s.sendall("REGISTER".encode(format))
                s.recv(1024).decode(format)
            except:
                messagebox.showerror('Error', "Server isn't respond")

            s.sendall(self.username_registration.get().encode(format))
            s.recv(1024).decode(format)

            s.sendall(self.password_registration.get().encode(format))
            s.recv(1024).decode(format)

            check_register = s.recv(1024).decode(format)
            s.sendall(check_register.encode(format))

            if (check_register == "CREATE ACCOUNT SUCCESSFUL"):
                messagebox.showinfo('SUCCESSFUL', check_register)
                windows.switchPage(loginClient)
            else:
                messagebox.showerror('Error', check_register)

        return False


class loginClient(Frame):
    def __init__(self, main_frame, windows, s):
        Frame.__init__(self, main_frame)
        self.username = StringVar()
        self.password = StringVar()

        self.configure(bg="#0099CC")

        self.login_frame_manager = Frame(master=self)
        self.login_frame_manager.configure(bg="#0099CC")
        self.login_frame_manager.pack()

        login_label = Label(master=self.login_frame_manager, text="LOGIN", bg="#0099CC",
                            width="15", height="2", fg="aliceblue", font='Tahoma 21 bold')
        login_label.pack()

        username_label = Label(master=self.login_frame_manager,
                               text="Username *", bg="#0099CC", fg="aliceblue", font='Tahoma 12 bold')
        username_label.pack()
        user_entry = Entry(master=self.login_frame_manager,
                           textvariable=self.username, width=50, bg='beige',  highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        user_entry.pack()
        user_entry.focus()

        password_label = Label(
            master=self.login_frame_manager, text="Password *", bg="#0099CC", fg="aliceblue", font='Tahoma 12 bold')
        password_label.pack()
        password_entry = Entry(
            master=self.login_frame_manager, show='*', textvariable=self.password, width=50, bg='beige', highlightbackground="darkgray", highlightcolor="darkgray", highlightthickness=1)
        password_entry.pack()

        login_button = Button(master=self.login_frame_manager, text="Login", width=12,
                              height=1, fg="white", bg="#666699", command=lambda: self.Login_handle(windows, s))  # ,command=lambda: self.Login_handle(windows)
        login_button.pack(pady=10)

        register_button = Button(master=self.login_frame_manager,
                                 text="Register", width=12, height=1, fg="white", bg="#666699", command=lambda: windows.switchPage(registerClient))
        register_button.pack()

        Disconnect_button = Button(master=self.login_frame_manager,
                                   text="Disconnect", width=12, height=1, fg="white", bg="#666699", command=lambda: self.Disconnect(windows, s))
        Disconnect_button.pack(pady=10)

    def Login_handle(self, windows, s):
        user = self.username.get()
        psw = self.password.get()

        if (user == "" or psw == ""):
            messagebox.showerror(
                'Error', 'PLEASE ENTER ALL INFORMATION REQUIRE!')
        else:
            try:
                s.sendall("LOGIN".encode(format))
                s.recv(1024).decode(format)
                
                s.sendall(user.encode(format))
                s.recv(1024).decode(format)

                s.sendall(psw.encode(format))
                s.recv(1024).decode(format)

                check_log = s.recv(1024).decode(format)
                s.sendall(check_log.encode(format))

                if (check_log == "SUCCESSFUL"):
                    messagebox.showinfo('Error', check_log)
                    temp_label['text'] = "USERNAME: "+user
                    windows.switchPage(HomePage_Client)
                else:
                    messagebox.showerror('Error', check_log)
            except:
                messagebox.showerror('Error', "Server isn't respond")
            return

    def Disconnect(self, windows, s):
        try:
            s.sendall("DISCONNECT".encode(format))
            s.recv(1024).decode(format)
            
            check = s.recv(1024).decode(format)
            s.sendall(check.encode(format))

            if (check == "ACCEPT"):
                s.close()
                print("disconnected server")
                windows.destroy()
                client = ConnectPage()
                client.mainloop()
        except:
            messagebox.showerror('Error', "Server isn't respond")

class clientGUI(Tk):
    def __init__(self, s):
        Tk.__init__(self)
        self.geometry("500x300+300+100")
        self.title("CLIENT")
        self.resizable(width=False, height=False)
        #self.iconphoto(False, PhotoImage(file='Image/Clients_icon.png'))
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window(s))

        self.main_frame = Frame(master=self, bg="grey")
        self.main_frame.pack(fill='both', expand=True)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.dictionary_frame = {}  # dictionary để lưu trữ những frame của server
        self.list_frame = (loginClient, registerClient, HomePage_Client)

        self.add_frame(s)

        self.switchPage(loginClient)  # switch between frame

    def add_frame(self,s):

        for i in self.list_frame:
            frame = i(self.main_frame, self, s)
            frame.grid(row=0, column=0, sticky="news")
            self.dictionary_frame[i] = frame

    def switchPage(self, pageName):
        if (pageName == HomePage_Client):
            self.geometry("915x450+100+200")
        elif (pageName == loginClient and pageName == registerClient):
            self.geometry("500x300+300+300")

        self.dictionary_frame[pageName].tkraise()

    def clear_widget(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def close_window(self,s):
        try:
            s.sendall("CLOSE WINDOW".encode(format))
            s.recv(1024).decode(format)

            check=s.recv(1024).decode(format)
            s.sendall(check.encode(format))

            if (check=="ACCEPT"):
                print("close window")
                self.destroy()
                s.close()

        except:
            messagebox.showerror('Error', "Server isn't respond")
            self.destroy()
            
        

####################################################
client = ConnectPage()
client.mainloop()
