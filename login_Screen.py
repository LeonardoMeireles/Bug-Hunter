import tkinter as tk
from PIL import ImageTk, Image

import sqlite3

#Color Palette: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#030303"
lime_Green = "#6ECB5A"

root = tk.Tk()
root.title("Bug Hunter")
root.iconbitmap("References/Icones/FeelsGoodMan.ico")
root.geometry("800x800")
root.resizable(width = 0, height = 0)
root.configure(background = black)

def change_Frame(frame_in):
    frame_in.tkraise()

#Frame de login
frame_login = tk.LabelFrame(root, width = 400, height = 400, padx = 40, pady = 40, bg = teal_Green) #Dentro do frame
frame_login.config(highlightbackground = forest_Green)
frame_login.grid(row = 0, column = 0, padx=190, pady=200) #Fora do frame

#Titulo da página
login_label = tk.Label(frame_login, text = "Login", font = ("Montserrat", 44), bg = teal_Green)
login_label.grid(row = 0,  column = 0, columnspan = 3, sticky = 'n'+'w'+'e'+'s', padx = 10, pady = 10)

#Criando a entrada para o Username
def holder_UText(event):
    current = username_in.get()
    if current == "Usuário":
        username_in.delete(0, tk.END)
    elif current == "":
            username_in.insert(0, "Usuário")

username_in = tk.Entry(frame_login, font = ("Montserrat"), fg = "#c2c2c2")
username_in.insert(0, "Usuário")
username_in.bind("<FocusIn>", holder_UText)
username_in.bind("<FocusOut>", holder_UText)
username_in.grid(row = 1, column = 0, columnspan = 3, sticky = 'n'+'w'+'e'+'s', padx = 20, pady = 10)

#Criando a entrada para a senha
def holder_PText(event):
    current = password_in.get()
    if current == "Senha":
        password_in.delete(0, tk.END)
    elif current == "":
            password_in.insert(0, "Senha")


password_in = tk.Entry(frame_login, font = ("Montserrat"), fg = "#c2c2c2")
password_in.insert(0, "Senha")
password_in.bind("<FocusIn>", holder_PText)
password_in.bind("<FocusOut>", holder_PText)
password_in.grid(row = 2, column = 0, columnspan = 3, sticky = 'n'+'w'+'e'+'s', padx = 20, pady = 10)

#Botão que redireciona para se registrar
def forgotP_window():
    return

forgotP_btn = tk.Label(frame_login, text = "Esqueci a senha", font = ("Montserrat", 10), bg = teal_Green, fg = forest_Green)
forgotP_btn.bind("<Button - 1>", forgotP_window())
forgotP_btn.grid(row = 3, column = 1, padx = 20)

#Botão de lembrar desse usuário
def remember_user():
    return

remember_box = tk.Checkbutton(frame_login, text = "Lembrar deste usuário", bg = teal_Green, fg = forest_Green)
remember_box.deselect()
remember_box.grid(row = 3, column = 0, sticky = 'w'+'e'+'n'+'s', padx = 20)

#Botão de login
def login():
    return

login_btn = tk.Button(frame_login, text = "Login", command = login, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d")
login_btn.grid(row = 4, column = 0, sticky = 'n'+'w'+'e'+'s', padx = 20, pady = 22)
login_btn.configure(height = 1, width = 1)

#Botão de Registrar-se
def register_window():
    r_form = tk.Tk()
    return

register_btn = tk.Button(frame_login, text = "Registrar-se", command = register_window, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d")
register_btn.grid(row = 4, column = 1, sticky = 'n'+'w'+'e'+'s', padx = 21, pady = 22)
register_btn.configure(width = 2)


#
tk.mainloop()