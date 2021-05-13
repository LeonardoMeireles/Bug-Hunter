try:
    import os
    import tkinter as tk
    from os.path import dirname, join
    import sys

    from dotenv import load_dotenv
    from PIL import Image, ImageTk

except Exception as e:
    print("Algumas bibliotecas estão faltando: {}".format(e))

#Login Window
from BH_Login.LoginWindow import LoginWindow
from BH_Login.RegisterWindow import RegisterWindow
from BH_Login.ForgotPWindow import ForgotPWindow

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
global db
db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
    )

cursor = db.cursor()

#Criando as Tabelas
#cursor.execute("CREATE TABLE Users (user_id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), name VARCHAR(255), username VARCHAR(50), salt VARCHAR(16), hash VARCHAR(512))")
#cursor.execute("CREATE TABLE Projects (project_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(500), category VARCHAR(50), status VARCHAR(50), date DATE)")
#cursor.execute("CREATE TABLE Problems (problem_id INT AUTO_INCREMENT PRIMARY KEY, project_id INT(4), name VARCHAR(255), reporter VARCHAR(255), status VARCHAR(50), priority VARCHAR(50), description VARCHAR(1000), date DATE)")
#cursor.execute("CREATE TABLE User_Projects (entry_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT(4), project_id INT(4))")
#cursor.execute("CREATE TABLE Activity (activity_id INT AUTO_INCREMENT PRIMARY KEY, type INT(2), user_id INT(4), problem_id INT(4), project_id INT(4), date DATE)")
#cursor.execute("CREATE TABLE Comments (comment_id INT AUTO_INCREMENT PRIMARY KEY, comment VARCHAR(1000), problem_id INT(4), user_id INT(4), date DATE)")

class BugHunter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.db = db
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
        self.geometry("400x400")
        self.resizable(width = 0, height = 0)

        self.state = False #boolean pra mostrar se está me fullscreen ou n

        #O container ira guardar uma pilha de frames, que podera ser modificado, para que a página que desejamos fique no topo
        global container
        self.container = tk.Frame(self) 
        self.container.configure(background = black)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        #Os frames do programa
        self.frames = {}
        self.frames["LoginWindow"] = LoginWindow(master = self.container, controller = self, BugHunter = self)
        self.frames["LoginWindow"].grid(row = 0, column = 0, sticky = "nsew")

        self.frames["RegisterWindow"] = RegisterWindow(master = self.container, controller = self)
        self.frames["RegisterWindow"].grid(row = 0, column = 0, sticky = "nsew")

        self.frames["ForgotPWindow"] = ForgotPWindow(master = self.container, controller = self)
        self.frames["ForgotPWindow"].grid(row = 0, column = 0, sticky = "nsew")
        


        self.show_frame("LoginWindow")

    def enter_BH(self, user_id):
        #Excluido os frames de login
        self.frames["RegisterWindow"].grid_forget()
        self.frames["RegisterWindow"].destroy()
        self.frames["ForgotPWindow"].grid_forget()
        self.frames["ForgotPWindow"].destroy()

        #Home Window
        from BH_Home.HeaderMenu import HeaderMenu
        from BH_Home.HomeWindow import HomeWindow
        from BH_Home.AllProjectsWindow import AllProjectsWindow
        from BH_Home.NewProjectWindow import NewProjectWindow
        from BH_Home.NewProblemWindow import NewProblemWindow

        #Adicionando o Header que sera presente em todos as outras páginas do BH
        self.frames["HeaderMenu"] = HeaderMenu(master = self.container, controller = self, bH = self, user_id = user_id)
        self.frames["HeaderMenu"].grid(row = 0, column = 0, sticky = "new")

        self.frames["HomeWindow"] = HomeWindow(master = self.container, controller = self, bH = self, user_id = user_id)
        self.frames["HomeWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))

        self.frames["AllProjectsWindow"] = AllProjectsWindow(master = self.container, controller = self, bH = self, user_id = user_id)
        self.frames["AllProjectsWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))

        self.frames["NewProjectWindow"] = NewProjectWindow(master = self.container, controller = self, bH = self, user_id = user_id)
        self.frames["NewProjectWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))

        self.frames["NewProblemWindow"] = NewProblemWindow(master = self.container, controller = self, bH = self, user_id = user_id)
        self.frames["NewProblemWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))

        self.frames["LoginWindow"].grid_forget()
        self.frames["LoginWindow"].destroy()

        #Entrando no BH
        self.resizable(True, True)
        self.geometry("1000x800")
        self.show_frame("HomeWindow")
        center(self)

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
