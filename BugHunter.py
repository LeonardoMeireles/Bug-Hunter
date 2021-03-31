try:
    import hashlib
    import os
    import secrets
    import tkinter as tk
    from os.path import dirname, join
    import sys

    from dotenv import load_dotenv
    from PIL import Image, ImageTk

except Exception as e:
    print("Algumas bibliotecas estão faltando: {}".format(e))

#Login Window
from BH_Login.LoginWindow import *
from BH_Login.RegisterWindow import *
from BH_Login.ForgotPWindow import *

#Home Window
from BH_Home.HeaderMenu import *
from BH_Home.HomeWindow import *

dotenv_file = join(dirname(__file__), '.env')
load_dotenv(dotenv_file)

import mysql.connector

#Paleta de Cores: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#030303"
lime_Green = "#6ECB5A"
red = "#b80018"

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")

#Conectando ao Banco de Dados
db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
    )

cursor = db.cursor()

#Criando a Table para guardar informações de Login
#cursor.execute("CREATE TABLE Users (user_id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), name VARCHAR(255), username VARCHAR(50), salt VARCHAR(16), hash VARCHAR(512))")
#cursor.execute("CREATE TABLE Projects (project_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), category VARCHAR(50))")

class BugHunter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        width_screen = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()

        ''' 
        -------------CONFIGURANDO TITLE BAR PRÓPRIA-----------------

        self.overrideredirect(1)

        title_bar = tk.Frame(self, bg = black, relief = tk.SUNKEN, bd = 0)
        title_bar.pack(expand = 1, fill = "x")
        titulo = tk.Label(title_bar, text = "Bug Hunter", fg = teal_Green, bg = black, font = "Montserrat")
        titulo.pack(anchor = tk.CENTER)

        def hide_screen():
            self.overrideredirect(0)
            self.inconify()

        window2 = tk.Canvas(self, bg = "light blue", highlightthickness = 0)

        titulo.pack(anchor = tk.LEFT)
        close_btn = tk.Button(title_bar, text = "X", bg = "grey", highlightbackground = "white", command = self.destroy)
        close_btn.pack(side = tk.RIGHT)
        minimize_btn = tk.Button(title_bar, text = "-", bg = "grey", highlightbackground = "white", command = self.hide_screen)
        minimize_btn.pack(side = tk.RIGHT)
        window2.pack(expand = 1, fill = "both")

        --------------------------------------------------------------'''

        self.title("Bug Hunter")
        self.iconbitmap("Assets/bh_Icon.ico")
        self.geometry("800x800")
        self.resizable(width = 0, height = 0)

        self.state = False #boolean pra mostrar se está me fullscreen ou n

        #O container ira guardar uma pilha de frames, que podera ser modificado, para que a página que desejamos fique no topo
        global container
        container = tk.Frame(self) 
        container.configure(background = black)
        container.pack(side="top", fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        #Os frames do programa
        self.frames = {}
        self.frames["LoginWindow"] = LoginWindow(master = container, controller = self, BugHunter = self)
        self.frames["LoginWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame

        self.frames["RegisterWindow"] = RegisterWindow(master = container, controller = self)
        self.frames["RegisterWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame

        self.frames["ForgotPWindow"] = ForgotPWindow(master = container, controller = self)
        self.frames["ForgotPWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame
        


        self.show_frame("LoginWindow")

    def enter_BH(self, user_id):
        #Excluido os frames de login
        self.frames["LoginWindow"].grid_forget()
        self.frames["LoginWindow"].destroy()
        self.frames["RegisterWindow"].grid_forget()
        self.frames["RegisterWindow"].destroy()
        self.frames["ForgotPWindow"].grid_forget()
        self.frames["ForgotPWindow"].destroy()

        #Entrando no BH
        self.resizable(True, True)
        self.geometry("1000x800")
        #Adicionando o Header que sera presente em todos as outras páginas do BH
        self.frames["HeaderMenu"] = HeaderMenu(master = container, controller = self, bH = self, user_id = user_id)
        self.frames["HeaderMenu"].grid(row = 0, column = 0, sticky = "new")
        self.frames["HomeWindow"] = HomeWindow(master = container, controller = self, bH = self, user_id = user_id)
        self.frames["HomeWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))

        self.show_frame("HomeWindow")
        return
    
    #Mostra o frame de acordo com o nome passado
    def show_frame(self, window_name):
        frame = self.frames[window_name]
        frame.tkraise()
    
#Metodo para centralizar a tela quando abrir o programa
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

if __name__ == "__main__":
    app = BugHunter()
    center(app)
    app.attributes('-alpha', 1.0)
    app.mainloop()
