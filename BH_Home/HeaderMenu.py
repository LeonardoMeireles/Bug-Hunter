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

dotenv_file = join(dirname(__file__), '.env')
load_dotenv(dotenv_file)

import mysql.connector

#Color Palette: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#121212"
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

class HeaderMenu(tk.Frame):
    def __init__(self, master, controller, bH, user_id):
        #Header do aplicativo
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = forest_Green)


        #Logo BH
        self.user_Image = tk.PhotoImage(file = "Assets/bh_Icon.png") #Precisa mudar para o icone do BH
        bh_logo = tk.Label(self, image = self.user_Image, bd = 0, padx = 100, background = forest_Green, activebackground  = "#dfdfdf")
        bh_logo.grid(row = 0, column = 0, sticky = 'w', pady = (10,10), padx = (20,10))
        #Dashboard
        def go_dashboard():
            return
        dashboard_btn = tk.Button(self, text = "Dashboard", font = ("Montserrat SemiBold", 11), command = go_dashboard, bg = forest_Green,
                                    activebackground =  forest_Green, bd = 0,  fg = "#dfdfdf")
        dashboard_btn.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "w")
        #Projetos
        def select_project():
            return
        def add_project():
            return
        projectsM = tk.Menubutton(self, text = "Projetos", font = ("Montserrat SemiBold", 11),  fg = "#dfdfdf")
        projectsM.config(bg = forest_Green, activebackground =  forest_Green, bd = 0)
        projectsM.menu = tk.Menu(projectsM, tearoff=0,  fg = "white", bg = teal_Green)
        projectsM["menu"] = projectsM.menu
        #Selecionando o nome de todos os projetos
        cursor.execute("SELECT name FROM Projects")
        project_s = tk.StringVar(self)
        test = cursor.fetchone()
        #Verificando se já existe projetos
        if test != None:
            ProjectList = list(cursor.fetchall())
            project_s.set(ProjectList[0])
            for project in cursor:
                projectsM.menu.add_checkbutton(label = project[0], command = select_project)
            projectsM.menu.add_checkbutton(label = "Add Project", font = ("Montserrat", 8), command = add_project)
            
        else:
            projectsM.menu.add_checkbutton(label = "Add Project", font = ("Montserrat", 8), command = add_project)
        projectsM.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "w")
        #Visto recentemente / Recently Viewed
        def go_RV():
            return
        rv_btn = tk.Button(self, text = "Visto Recentemente", font = ("Montserrat SemiBold", 11), command = go_RV, bg = forest_Green,
                            activebackground =  forest_Green, bd = 0,  fg = "#dfdfdf")
        rv_btn.grid(row = 0, column = 3, padx = 10, pady = 10, sticky = "w")
        #Adicionar
        def add_header():
            return
        self.plus_img = tk.PhotoImage(file = "Assets/User_Interface/plus.png") #precisa ser self se não o garbage colector pega
        add_Hbtn = tk.Button(self, image = self.plus_img, command = lambda: add_header,
                            borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        add_Hbtn.grid(row = 0, column = 4, padx = (10,280), pady = (10,10), sticky = "w")
        #Notificações
        def show_notifications():
            return
        self.notification_img = tk.PhotoImage(file = "Assets/User_Interface/notification.png") #precisa ser self se não o garbage colector pega
        notification_btn = tk.Button(self, image = self.notification_img, command = lambda: show_notifications,
                            borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        notification_btn.grid(row = 0, column = 5, padx = 10, pady = (10,10), sticky = "e")
        self.columnconfigure(5, weight=1)
        #User Img
        def click_userimg():
            return
        self.user_img = tk.PhotoImage(file = "Assets/User_Interface/profile_user.png") #precisa ser self se não o garbage colector pega
        user_btn = tk.Button(self, image = self.user_img, command = lambda: click_userimg,
                            borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        user_btn.grid(row = 0, column = 6, padx = 10, pady = (10,10), sticky = "e")
        

'''if __name__ == "__main__":
    app = HomeWindow()
    app.mainloop()'''