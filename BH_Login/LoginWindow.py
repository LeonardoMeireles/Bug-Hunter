import hashlib
import os
import tkinter as tk
from os.path import dirname, join

from dotenv import load_dotenv
from PIL import Image, ImageTk


#Paleta de Cores: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#030303"
lime_Green = "#6ECB5A"
red = "#b80018"


dotenv_file = join(dirname(__file__), '.env')
load_dotenv(dotenv_file)

import mysql.connector

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

class LoginWindow(tk.Frame):

    def __init__(self, master, controller, BugHunter):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 35, pady = 15, bg = teal_Green) #Dentro do Frame

        #Titulo da página
        self.iconL = tk.PhotoImage(file = "Assets/bh_Login.png")
        login_icon = tk.Label(self, image = self.iconL, font = ("Montserrat SemiBold", 44), bg = teal_Green, bd = 0)
        login_icon.grid(row = 0,  column = 0, columnspan = 3, sticky = 'w', padx = 113, pady = (5,0))

        #Criando a entrada para o Username
        def holder_UText(event):
            current = username_in.get()
            if current == "Usuário":
                username_in.delete(0, tk.END)
                username_in.config(fg = black)
            elif current == "":
                username_in.insert(0, "Usuário")
                username_in.config(fg = "#c2c2c2")

        username_in = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 28)
        username_in.insert(0, "Usuário")
        username_in.bind("<FocusIn>", holder_UText)
        username_in.bind("<FocusOut>", holder_UText)
        username_in.grid(row = 1, column = 0, columnspan = 2, sticky = 'w', padx = 32, pady = (5,0))

        self.user_Image = tk.PhotoImage(file = "Assets/User_Interface/user.png")
        user_icon = tk.Label(self, image = self.user_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        user_icon.grid(row = 1, column = 0, sticky = 'w', pady = (5,0))

        #Criando a entrada para a senha
        def holder_PText(event):
            current = password_in.get()
            if current == "Senha":
                password_in.delete(0, tk.END)
                password_in.config(fg = black)
                password_in.config(show = "*")
            elif current == "":
                password_in.insert(0, "Senha")
                password_in.config(fg = "#c2c2c2")
                password_in.config(show = "")



        password_in = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2")
        password_in.insert(0, "Senha")
        password_in.bind("<FocusIn>", holder_PText)
        password_in.bind("<FocusOut>", holder_PText)
        password_in.grid(row = 2, column = 0, columnspan = 2, sticky = 'n'+'w'+'e', padx = 32, pady = (26,0), ipady = 0)

        self.password_Image = tk.PhotoImage(file = "Assets/User_Interface/password.png")
        password_icon = tk.Label(self, image = self.password_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        password_icon.grid(row = 2, column = 0, sticky = 'w' + 'n', pady = (23,0))

        #Botão que redireciona para se registrar
        forgotP_btn = tk.Button(self, text = "Esqueci a senha", command = lambda: controller.show_frame("ForgotPWindow"),
                                font = ("Montserrat SemiBold",10), bg = teal_Green, fg = "#002e29", activebackground =  teal_Green,  borderwidth = 0)
        forgotP_btn.grid(row = 5, column = 1, padx = 15, sticky = 'w')

        #Botão de lembrar desse usuário
        def remember_user():
            return

        remember_box = tk.Checkbutton(self, text = "Lembrar deste usuário", font = ("Montserrat SemiBold",10), bg = teal_Green, fg = "#002e29", activebackground = teal_Green)
        remember_box.deselect()
        remember_box.grid(row = 5, column = 0, sticky = 'w', padx = 4)

        #Mensagem de erro do usuário
        u_errormsg = tk.Label(self, font = ("Montserrat",10), bg = teal_Green, fg = "#b80018")
        u_errormsg.grid(row = 2, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 30, pady = 0)
        
        #Mensagem de erro da senha
        p_errormsg = tk.Label(self, font = ("Montserrat",10), bg = teal_Green, fg = "#b80018")
        p_errormsg.grid(row = 3, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 30, pady = 0)
        
        #Botão de login
        def login():
            username = str(username_in.get())
            password = str(password_in.get())
            #Não foi inserido usuário
            if (username == "Usuário") or (username == ""):
                u_errormsg.config(text = "* Inserir usuário")
                if (password == "Senha"):
                    p_errormsg.config(text = "* Inserir senha")
                    return
            #Não foi inserido senha
            if (password == "Senha") or (password == ""):
                p_errormsg.config(text = "* Inserir senha")
                return
            #Checando usuário
            cursor_u = db.cursor()
            cursor_u.execute("SELECT user_id FROM Users WHERE username = %s", (username, ) )
            msg_u = cursor_u.fetchone()  
            if not msg_u:
                u_errormsg.config(text = "* Este usuário não existe")
                return
            #Checando senha
            cursor_sh = db.cursor()
            cursor_sh.execute("SELECT salt, hash FROM Users WHERE username = %s", (username, ) )
            sh = cursor_sh.fetchone() #salt e hash do usuário
            salt = sh[0]
            hash = sh[1]
            cursor_sh.close()
            check_p = hashlib.sha512( salt.encode('ascii') + password.encode('ascii') ).hexdigest()
            if check_p != hash:
                p_errormsg.config(text = "* Senha incorreta")
                return
            #Login autorizado
            else:
                user_id = msg_u[0]
                BugHunter.enter_BH(user_id)
        login_btn = tk.Button(self, text = "Login", command = login, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d")
        login_btn.grid(row = 6, column = 0, columnspan = 2, sticky = 'w', padx = 2, pady = 10)
        login_btn.configure(height = 1, width = 33)
    
        #Botão de Registrar-se
        register_btn = tk.Button(self, text = "Criar uma conta", command = lambda: controller.show_frame("RegisterWindow"),
                                font = ("Montserrat"), bg = teal_Green, fg = "#002e29", activebackground =  teal_Green, activeforeground = black, borderwidth = 0)
        register_btn.grid(row = 7, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 105, pady = 2)