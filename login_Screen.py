import tkinter as tk
from PIL import ImageTk, Image

import sqlite3

#Color Palette: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#030303"
lime_Green = "#6ECB5A"

class BugHutner(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Bug Hunter")
        self.iconbitmap("References/Icones/FeelsGoodMan.ico")
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
        login_label.grid(row = 0,  column = 0, columnspan = 3, sticky = 'w', padx = 85, pady = 10)

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
        username_in.grid(row = 1, column = 0, columnspan = 2, sticky = 'w', padx = 32, pady = 10)

        self.user_Image = tk.PhotoImage(file = "Images/user.png")
        user_icon = tk.Label(self, image = self.user_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        user_icon.grid(row = 1, column = 0, sticky = 'w')

        #Criando a entrada para a senha
        def holder_PText(event):
            current = password_in.get()
            if current == "Senha":
                password_in.delete(0, tk.END)
                password_in.config(fg = black)
            elif current == "":
                password_in.insert(0, "Senha")
                password_in.config(fg = "#c2c2c2")



        password_in = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2")
        password_in.insert(0, "Senha")
        password_in.bind("<FocusIn>", holder_PText)
        password_in.bind("<FocusOut>", holder_PText)
        password_in.grid(row = 2, column = 0, columnspan = 2, sticky = 'n'+'w'+'e'+'s', padx = 32, pady = 12)

        self.password_Image = tk.PhotoImage(file = "Images/password.png")
        password_icon = tk.Label(self, image = self.password_Image, bd = 0, padx = 100, background = teal_Green, activebackground  = teal_Green)
        password_icon.grid(row = 2, column = 0, sticky = 'w')

        #Botão que redireciona para se registrar
        forgotP_btn = tk.Button(self, text = "Esqueci a senha", command = lambda: controller.show_frame("ForgotPWindow"),
                                font = ("Montserrat",10), bg = teal_Green, fg = "#002e29", activebackground =  "#01695d",  borderwidth = 0)
        forgotP_btn.grid(row = 3, column = 1, padx = 15, sticky = 'w')

        #Botão de lembrar desse usuário
        def remember_user():
            return

        remember_box = tk.Checkbutton(self, text = "Lembrar deste usuário", font = ("Montserrat",10), bg = teal_Green, fg = "#002e29", activebackground = teal_Green)
        remember_box.deselect()
        remember_box.grid(row = 3, column = 0, sticky = 'w', padx = 4)

        #Botão de login
        def login():
            return

        login_btn = tk.Button(self, text = "Login", command = login, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d")
        login_btn.grid(row = 4, column = 0, columnspan = 2, sticky = 'w', padx = 2, pady = 10)
        login_btn.configure(height = 1, width = 33)

        #Botão de Registrar-se
        register_btn = tk.Button(self, text = "Criar uma conta", command = lambda: controller.show_frame("RegisterWindow"),
                                font = ("Montserrat"), bg = teal_Green, fg = "#002e29", activebackground =  teal_Green, activeforeground = black, borderwidth = 0)
        register_btn.grid(row = 5, column = 0, columnspan = 2, sticky = 'w' + 'n', padx = 105, pady = 10)

class RegisterWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Images/back_arrow.png") #precisa ser self se não o garbage colector pega
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
        new_email.grid(row = 2, column = 0, sticky = "w", padx = 70, pady = 10)

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
        new_username.grid(row = 3, column = 0, columnspan = 2, sticky = 'w', padx = 70, pady = 10)

        #Criando a entrada para a senha
        def holder_PText(event):
            current = new_password.get()
            if current == "Senha":
                new_password.delete(0, tk.END)
                new_password.config(fg = black)
            elif current == "":
                new_password.insert(0, "Senha")
                new_password.config(fg = "#c2c2c2")


        new_password = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_password.insert(0, "Senha")
        new_password.bind("<FocusIn>", holder_PText)
        new_password.bind("<FocusOut>", holder_PText)
        new_password.grid(row = 4, column = 0, sticky = "w", padx = 70, pady = 10)

        #Confirmar senha
        def holder_PCText(event):
            current = new_passwordC.get()
            if current == "Confirmar senha":
                new_passwordC.delete(0, tk.END)
                new_passwordC.config(fg = black)
            elif current == "":
                new_passwordC.insert(0, "Confirmar senha")
                new_passwordC.config(fg = "#c2c2c2")


        new_passwordC = tk.Entry(self, font = ("Montserrat"), fg = "#c2c2c2", width = 25)
        new_passwordC.insert(0, "Confirmar senha")
        new_passwordC.bind("<FocusIn>", holder_PCText)
        new_passwordC.bind("<FocusOut>", holder_PCText)
        new_passwordC.grid(row = 5, column = 0, sticky = "w", padx = 70, pady = (10,26))

        #Botão para criar a conta
        def criar_Conta():
            return
        register_btn = tk.Button(self, text = "Criar", command = criar_Conta, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d", width = 27)
        register_btn.grid(row = 6, column = 0, columnspan = 2, sticky = 'w', padx = 69)

class ForgotPWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Images/back_arrow.png") #precisa ser self se não o garbage colector pega
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

if __name__ == "__main__":
    app = BugHutner()
    app.mainloop()