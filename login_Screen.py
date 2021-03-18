import tkinter as tk
from PIL import ImageTk, Image

import re

import secrets
import hashlib

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_file = join(dirname(__file__), '.env')
load_dotenv(dotenv_file)

import mysql.connector

#Color Palette: 
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

class BugHutner(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Bug Hunter")
        self.iconbitmap("Assets/bh_Icon.ico")
        self.geometry("800x800")
        self.resizable(width = 0, height = 0)

        #O container ira guardar uma pilha de frames, que podera ser modificado, para que a página que desejamos fique no topo
        container = tk.Frame(self) 
        container.configure(background = black)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Os frames do programa
        self.frames = {}
        self.frames["LoginWindow"] = LoginWindow(master = container, controller = self)
        self.frames["LoginWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame

        self.frames["RegisterWindow"] = RegisterWindow(master = container, controller = self)
        self.frames["RegisterWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame

        self.frames["ForgotPWindow"] = ForgotPWindow(master = container, controller = self)
        self.frames["ForgotPWindow"].grid(row = 0, column = 0, padx=190, pady=200, sticky = "nsew") #Fora do frame

        self.show_frame("LoginWindow")

    
    #Mostra o frame de acordo com o nome passado
    def show_frame(self, window_name):
        frame = self.frames[window_name]
        frame.tkraise()

class LoginWindow(tk.Frame):

    def __init__(self, master, controller):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 40, pady = 15, bg = teal_Green) #Dentro do Frame


        #Titulo da página
        login_label = tk.Label(self, text = "Login", font = ("Montserrat", 44), bg = teal_Green)
        login_label.grid(row = 0,  column = 0, columnspan = 3, sticky = 'w', padx = 85, pady = (10,0))

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
        username_in.grid(row = 1, column = 0, columnspan = 2, sticky = 'w', padx = 32, pady = (10,0))

        self.user_Image = tk.PhotoImage(file = "Assets/user.png")
        user_icon = tk.Label(self, image = self.user_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        user_icon.grid(row = 1, column = 0, sticky = 'w', pady = (10,0))

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
        password_in.grid(row = 2, column = 0, columnspan = 2, sticky = 'n'+'w'+'e', padx = 32, pady = (30,0), ipady = 0)

        self.password_Image = tk.PhotoImage(file = "Assets/password.png")
        password_icon = tk.Label(self, image = self.password_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        password_icon.grid(row = 2, column = 0, sticky = 'w' + 'n', pady = (28,0))

        #Botão que redireciona para se registrar
        forgotP_btn = tk.Button(self, text = "Esqueci a senha", command = lambda: controller.show_frame("ForgotPWindow"),
                                font = ("Montserrat",10), bg = teal_Green, fg = "#002e29", activebackground =  teal_Green,  borderwidth = 0)
        forgotP_btn.grid(row = 5, column = 1, padx = 15, sticky = 'w')

        #Botão de lembrar desse usuário
        def remember_user():
            return

        remember_box = tk.Checkbutton(self, text = "Lembrar deste usuário", font = ("Montserrat",10), bg = teal_Green, fg = "#002e29", activebackground = teal_Green)
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
            cursor_u.execute("SELECT username FROM Users WHERE username = %s", (username, ) )
            msg_u = cursor_u.fetchone()  
            if not msg_u:
                u_errormsg.config(text = "* Este usuário não existe")
                return
            #Checando senha
            cursor_sh = db.cursor()
            cursor_sh.execute("SELECT salt, hash FROM Users WHERE username = %s", (username, ) )
            sh = cursor_u.fetchone() #salt e hash do usuário
            salt = sh[0]
            hash = sh[1]
            cursor_sh.close()
            check_p = hashlib.sha512( salt.encode('ascii') + password.encode('ascii') ).hexdigest()
            if check_p != hash:
                p_errormsg.config(text = "* Senha incorreta")
                return
            #Login autorizado
            else:
                print("Autorizo")
                test = tk.Toplevel()
                test.title("Teste para login")
        login_btn = tk.Button(self, text = "Login", command = login, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d")
        login_btn.grid(row = 6, column = 0, columnspan = 2, sticky = 'w', padx = 2, pady = 10)
        login_btn.configure(height = 1, width = 33)
    
        #Botão de Registrar-se
        register_btn = tk.Button(self, text = "Criar uma conta", command = lambda: controller.show_frame("RegisterWindow"),
                                font = ("Montserrat"), bg = teal_Green, fg = "#002e29", activebackground =  teal_Green, activeforeground = black, borderwidth = 0)
        register_btn.grid(row = 7, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 105, pady = 10)

class RegisterWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Assets/back_arrow.png") #precisa ser self se não o garbage colector pega
        back_btn = tk.Button(self, image = self.back_btnImage, command = lambda: controller.show_frame("LoginWindow"),
                            borderwidth = 0, background = teal_Green, activebackground  = teal_Green)
        back_btn.grid(row = 0, column = 0, padx = 2, pady = (10,0), sticky = "w" + 'n')

        #Titulo da página
        register_label = tk.Label(self, text = "Criar conta", font = ("Montserrat", 44), bg = teal_Green)
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

class ForgotPWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Assets/back_arrow.png") #precisa ser self se não o garbage colector pega
        back_btn = tk.Button(self, image = self.back_btnImage, command = lambda: controller.show_frame("LoginWindow"),
                            borderwidth = 0, background = teal_Green, activebackground  = teal_Green)
        back_btn.grid(row = 0, column = 0, padx = 2, pady = (10,0), sticky = "w" + "n")

        #Titulo da página
        register_label = tk.Label(self, text = "Recuperar Senha", font = ("Montserrat", 30), bg = teal_Green)
        register_label.grid(row = 0,  column = 0, padx = 30, pady = (45,10), sticky = 'n'+'w'+'e'+'s')

        #Criando a entrada para o E-mail
        def holder_UText(event):
            current = rec_email.get()
            if current == "E-mail":
                rec_email.delete(0, tk.END)
                rec_email.config(fg = black)
            elif current == "":
                rec_email.insert(0, "E-mail")
                rec_email.config(fg = "#c2c2c2")

        rec_email = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        rec_email.insert(0, "E-mail")
        rec_email.bind("<FocusIn>", holder_UText)
        rec_email.bind("<FocusOut>", holder_UText)
        rec_email.grid(row = 2, column = 0, sticky = "w", padx = 70, pady = 10)

        #Botão para criar a conta
        def criar_Conta():
            return
        register_btn = tk.Button(self, text = "Recuperar senha", command = criar_Conta, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d", width = 27)
        register_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10)

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
    app = BugHutner()
    center(app)
    app.attributes('-alpha', 1.0)
    app.mainloop()