try:
    import os
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
white82 = "#dfdfdf"

class HeaderMenu(tk.Frame):
    def __init__(self, master, controller, bH, user_id):
        #Header do aplicativo
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = forest_Green)
        db = bH.db

        #Logo BH
        self.user_Image = tk.PhotoImage(file = "Assets/bh_Icon.png")
        bh_logo = tk.Label(self, image = self.user_Image, bd = 0, padx = 100, background = forest_Green, activebackground  = white82)
        bh_logo.grid(row = 0, column = 0, sticky = 'w', pady = (10,10), padx = (22,6))

        #Página Inicial
        dashboard_btn = tk.Button(self, text = "Página Inicial", font = ("Montserrat SemiBold", 11), command = lambda: controller.show_frame("HomeWindow"), bg = forest_Green,
                                    activebackground =  forest_Green, bd = 0,  fg = white82)
        dashboard_btn.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "w")

        #Projetos
        def go_projects():
            return
        projectsM = tk.Button(self, text = "Projetos", font = ("Montserrat SemiBold", 11),  fg = white82, command = lambda: controller.show_frame("AllProjectsWindow"))
        projectsM.config(bg = forest_Green, activebackground =  forest_Green, bd = 0)
        projectsM.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "w")
        
        '''#Selecionando o nome de todos os projetos
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
        projectsM.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "w") '''
        
        #Adicionar
        def add_problem():
            return
        self.plus_img = tk.PhotoImage(file = "Assets/User_Interface/plus.png")
        add_Hbtn = tk.Menubutton(self, image = self.plus_img, borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        add_Hbtn.grid(row = 0, column = 4, padx = (10,280), pady = (10,10), sticky = "w")
        add_Hbtn.menu = tk.Menu(add_Hbtn, tearoff=0,  fg = "white", bg = forest_Green, bd = 0, activebackground = teal_Green)
        add_Hbtn["menu"] = add_Hbtn.menu
        add_Hbtn.menu.add_command (label = "Adicionar Projeto", font = ("Montserrat", 9), command = lambda: controller.show_frame("NewProjectWindow"))
        add_Hbtn.menu.add_command (label = "Adicionar Problema", font = ("Montserrat", 9), command = lambda: controller.show_frame("NewProblemWindow"))

        #Notificações
        def show_notifications():
            return
        self.notification_img = tk.PhotoImage(file = "Assets/User_Interface/notification.png")
        notification_btn = tk.Button(self, image = self.notification_img, command = lambda: show_notifications,
                            borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        notification_btn.grid(row = 0, column = 5, padx = 10, pady = (10,10), sticky = "e")
        self.columnconfigure(5, weight=1)

        #User Img
        def click_userimg():
            return
        self.user_img = tk.PhotoImage(file = "Assets/User_Interface/profile_user.png")
        user_btn = tk.Button(self, image = self.user_img, command = lambda: click_userimg,
                            borderwidth = 0, background = forest_Green, activebackground  = forest_Green)
        user_btn.grid(row = 0, column = 6, padx = 10, pady = (10,10), sticky = "e")