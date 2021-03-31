import hashlib
import os
import re
import secrets
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

class RegisterWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Assets/User_Interface/back_arrow.png") #precisa ser self se não o garbage colector pega
        back_btn = tk.Button(self, image = self.back_btnImage, command = lambda: controller.show_frame("LoginWindow"),
                            borderwidth = 0, background = teal_Green, activebackground  = teal_Green)
        back_btn.grid(row = 0, column = 0, padx = 2, pady = (10,0), sticky = "w" + 'n')

        #Titulo da página
        register_label = tk.Label(self, text = "Criar conta", font = ("Montserrat SemiBold", 44), bg = teal_Green)
        register_label.grid(row = 0,  column = 0, padx = 45, pady = (20,0), sticky = 'n'+'w')

        #Criando a entrada para o E-mail
        def holder_UText(event):
            current = new_email.get()
            if current == "E-mail":
                new_email.delete(0, tk.END)
                new_email.config(fg = black)
            elif current == "":
                new_email.insert(0, "E-mail")
                new_email.config(fg = "#c2c2c2")

        new_email = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_email.insert(0, "E-mail")
        new_email.bind("<FocusIn>", holder_UText)
        new_email.bind("<FocusOut>", holder_UText)
        new_email.grid(row = 2, column = 0, sticky = "w", padx = 70, pady = (0,14))

        #Criando a entrada para o Nome
        def holder_UText(event):
            current = new_name.get()
            if current == "Nome":
                new_name.delete(0, tk.END)
                new_name.config(fg = black)
            elif current == "":
                new_name.insert(0, "Nome")
                new_name.config(fg = "#c2c2c2")

        new_name = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_name.insert(0, "Nome")
        new_name.bind("<FocusIn>", holder_UText)
        new_name.bind("<FocusOut>", holder_UText)
        new_name.grid(row = 3, column = 0, columnspan = 2, sticky = 'w', padx = 70, pady = (5,14))

        #Criando a entrada para o Username
        def holder_UText(event):
            current = new_username.get()
            if current == "Usuário":
                new_username.delete(0, tk.END)
                new_username.config(fg = black)
            elif current == "":
                new_username.insert(0, "Usuário")
                new_username.config(fg = "#c2c2c2")

        new_username = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_username.insert(0, "Usuário")
        new_username.bind("<FocusIn>", holder_UText)
        new_username.bind("<FocusOut>", holder_UText)
        new_username.grid(row = 4, column = 0, columnspan = 2, sticky = 'w', padx = 70, pady = (5,14))

        #Criando a entrada para a senha
        def holder_PText(event):
            current = new_password.get()
            if current == "Senha":
                new_password.delete(0, tk.END)
                new_password.config(fg = black)
                new_password.config(show = "*")
            elif current == "":
                new_password.insert(0, "Senha")
                new_password.config(fg = "#c2c2c2", show = "")

        new_password = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_password.insert(0, "Senha")
        new_password.bind("<FocusIn>", holder_PText)
        new_password.bind("<FocusOut>", holder_PText)
        new_password.grid(row = 5, column = 0, sticky = "w", padx = 70, pady = (5,14))

        #Confirmar senha
        def holder_PCText(event):
            current = new_passwordC.get()
            if current == "Confirmar senha":
                new_passwordC.delete(0, tk.END)
                new_passwordC.config(fg = black)
                new_passwordC.config(show = "*")
            elif current == "":
                new_passwordC.insert(0, "Confirmar senha")
                new_passwordC.config(fg = "#c2c2c2", show = "")


        new_passwordC = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_passwordC.insert(0, "Confirmar senha")
        new_passwordC.bind("<FocusIn>", holder_PCText)
        new_passwordC.bind("<FocusOut>", holder_PCText)
        new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,20))
        
        #Mensagem de erro
        error_msg = tk.Label(self, text = "", background = teal_Green, fg = red)
        error_msg.grid(row = 7, column = 0, sticky = "w", padx = 70)

        #Função para limpar todas as entrys
        def limpar_entrys():
            new_email.delete(0, tk.END)
            new_name.delete(0, tk.END)
            new_username.delete(0, tk.END)
            new_password.delete(0, tk.END)
            new_passwordC.delete(0, tk.END)
            new_email.insert(0, "E-mail")
            new_email.config(fg = "#c2c2c2")
            new_name.insert(0, "Nome")
            new_name.config(fg = "#c2c2c2")
            new_username.insert(0, "Usuário")
            new_username.config(fg = "#c2c2c2")
            new_password.insert(0, "Senha")
            new_password.config(fg = "#c2c2c2", show = "")
            new_passwordC.insert(0, "Confirmar senha")
            new_passwordC.config(fg = "#c2c2c2", show = "")

        #Botão para criar a conta    
        def criar_Conta():
            #Confirmando se o usuário prencheu as entradas necessárias
            error_msg.config(text = "")
            if ( new_email.get() == "E-mail" ) or (new_email.get() == ""):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Inserir e-mail")
                return
            elif ( new_name.get() == "Nome") or (new_name.get() == ""):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Inserir nome")
                return
            elif ( new_username.get() == "Usuário" ) or (new_username.get() == ""):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Inserir usuário")
                return
            elif ( new_password.get() == "Senha" ) or (new_password.get() == ""):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Inserir senha")
                return
            elif ( new_passwordC.get() == "Confirmar senha" ) or (new_passwordC.get() == ""):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Confirme a senha")
                return
            #Confirmando se as entradas são validas  
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email.get()):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Email invalido")
                return
            elif (new_password.get() != new_passwordC.get()):
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Senhas não combinam")
                return
            #Verificando se e-mail já existe
            cursor_e = db.cursor()
            cursor_e.execute("SELECT email FROM Users WHERE email = %s", (new_email.get(), ) )
            msg_e = cursor_e.fetchone()  
            if msg_e:
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Este e-mail já esta sendo usado")
                return
            cursor_e.close()
            #Verificando se usuário já existe
            cursor_u = db.cursor()
            cursor_u.execute("SELECT username FROM Users WHERE username = %s", (new_username.get(), ) )
            msg_u = cursor_u.fetchone()  
            if msg_u:
                new_passwordC.grid(row = 6, column = 0, sticky = "w", padx = 70, pady = (5,2))
                register_btn.grid(row = 8, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)
                error_msg.config(text = "* Este usuário já esta sendo usado")
                return
            cursor_u.close()
            #Está tudo certo, inserir usuário no db

            #Formando um salt para a senha do usuário
            salt = secrets.token_hex(8).encode('ascii')
            #Aplicando hash na senha
            hash = hashlib.sha512( salt + str(new_password.get()).encode('ascii') ).hexdigest()
            #Armazenando tudo no db
            add_user = """INSERT INTO Users
                        (email, name, username, salt, hash)
                        VALUES (%s, %s, %s, %s, %s)"""
            user_data = (str(new_email.get()), str(new_name.get()), str(new_username.get()), salt, hash )
            cursor.execute(add_user, user_data)
            db.commit()
            error_msg.config(text = "Cadastro conluido!", fg = "#002e29")
            limpar_entrys()
            back_btn.invoke()
            return
                
        register_btn = tk.Button(self, text = "Criar", command = criar_Conta, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d", width = 27)
        register_btn.grid(row = 7, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 69)