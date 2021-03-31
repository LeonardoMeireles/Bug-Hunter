import hashlib
import os
import tkinter as tk
from os.path import dirname, join

from dotenv import load_dotenv
from PIL import Image, ImageTk

#Color Palette: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#030303"
lime_Green = "#6ECB5A"
red = "#b80018"

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

class ForgotPWindow(tk.Frame):
    def __init__(self, master, controller):
        #Frame de Registro
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(highlightbackground = forest_Green, width = 400, height = 400, padx = 5, pady = 2, bg = teal_Green) #Dentro do Frame

        self.back_btnImage = tk.PhotoImage(file = "Assets/User_Interface/back_arrow.png") #precisa ser self se não o garbage colector pega
        back_btn = tk.Button(self, image = self.back_btnImage, command = lambda: controller.show_frame("LoginWindow"),
                            borderwidth = 0, background = teal_Green, activebackground  = teal_Green)
        back_btn.grid(row = 0, column = 0, padx = 2, pady = (10,0), sticky = "w" + "n")

        #Titulo da página
        forgot_label = tk.Label(self, text = "Recuperar Senha", font = ("Montserrat SemiBold", 30), bg = teal_Green)
        forgot_label.grid(row = 0,  column = 0, padx = 30, pady = (45,10), sticky = 'n'+'w'+'e'+'s')

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
        forgot_btn = tk.Button(self, text = "Recuperar senha", command = criar_Conta, font = ("Montserrat"), bg = forest_Green, activebackground =  "#01695d", width = 27)
        forgot_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10)