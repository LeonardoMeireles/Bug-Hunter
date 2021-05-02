try:
    import os
    import tkinter as tk
    from os.path import dirname, join
    import sys

    from dotenv import load_dotenv
    from PIL import Image, ImageTk

except Exception as e:
    print("Algumas bibliotecas estão faltando: {}".format(e))

from BH_Home.ProjectWindow import ProjectWindow

dotenv_file = join(dirname(__file__), '.env')
load_dotenv(dotenv_file)

import mysql.connector

#Color Palette: 
teal_Green = "#028476"
forest_Green = "#015D53"
black = "#121212"
lime_Green = "#6ECB5A"
grey = "#3a3d45"
dark_grey = "#202021"
white82 = "#dfdfdf"


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

class AllProjectsWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)

        #Titulo da página
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "new", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = "Projetos", font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 16)

        #Seleção do tipo de projeto
        def my_proj(typeP):
            typeP.config( text = "Meus Projetos")
            return

        def finished_proj(typeP):
            typeP.config( text = "Projetos Concluidos")
            return

        def all_proj(typeP):
            typeP.config( text = "Todos os Projetos")
            return
        
        self.rightArrow = tk.PhotoImage(file = "Assets/User_Interface/right_arrow.png")
        arrowR = tk.Label(self, image = self.rightArrow, bd = 0, background = dark_grey, activebackground  = dark_grey)
        arrowR.grid(row = 1, column = 0, padx = 20, pady = 10, sticky = "w")
        typeP = tk.Menubutton(self, text = "Todos os Projetos", font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
        typeP.grid(row = 1, column = 0, padx = 35, pady = 10, sticky = "w")
        typeP.menu = tk.Menu(typeP, tearoff=0,  foreground = white82, bg = grey, bd = 0, activebackground = grey)
        typeP["menu"] = typeP.menu
        typeP.menu.add_radiobutton(label = "Todos os Projetos", font = ("Montserrat", 9), command = lambda: all_proj(typeP), selectcolor = teal_Green)
        typeP.menu.add_radiobutton(label = "Meus Projetos", font = ("Montserrat", 9), command = lambda: my_proj(typeP), selectcolor = teal_Green)
        typeP.menu.add_radiobutton(label = "Projetos Concluidos", font = ("Montserrat", 9), command = lambda: finished_proj(typeP), selectcolor = teal_Green)
        typeP.menu.invoke(0)

        self.newP = tk.PhotoImage(file = "Assets/User_Interface/newprojectBtn.png")
        addP_btn = tk.Button(self, image = self.newP, bd = 0, background = dark_grey, activebackground  = dark_grey, command = lambda: controller.show_frame("NewProjectWindow"))
        addP_btn.grid(row = 1, column = 1, padx = 16, pady = (10,5))

        #Local que mostrara os projetos

        def _on_mousewheel(event):
          self.canvasP.yview_scroll(int(-1*(event.delta/120)), "units")

        projectsF = tk.Frame(self, bg = black, bd = 0)
        projectsF.grid(row = 2, column = 0, sticky = "nsew", padx = 17, pady = (5,20), columnspan = 4)
        self.rowconfigure(2, weight = 1)
        self.canvasP = tk.Canvas(projectsF, bg = black, bd = 0, highlightthickness = 0)
        self.canvasP.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        myproblemsCF = tk.Frame(self.canvasP, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasP.create_window((0,0), window = myproblemsCF, anchor = "nw")
        self.canvasP.configure(background = black)
        self.canvasP.bind_all("<MouseWheel>", _on_mousewheel)

        #Pegando todos os projetos
        cursorAP = db.cursor()
        cursorAP.execute("SELECT * from Projects ORDER BY date ASC")
        projects = cursorAP.fetchall()
        cursorAP.close()
        nomeP = tk.Label(myproblemsCF, text = "NOME DO PROJETO", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        nomeP.grid(row = 0, column = 0, padx = 10, sticky = "nw")
        
        nomeP = tk.Label(myproblemsCF, text = "STATUS", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        nomeP.grid(row = 0, column = 0, padx = 250, sticky = "nw")

        nomeP = tk.Label(myproblemsCF, text = "CATEGORIA", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        nomeP.grid(row = 0, column = 0, padx = 400, sticky = "nw")

        nomeP = tk.Label(myproblemsCF, text = "DATA", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        nomeP.grid(row = 0, column = 0, padx = 600, sticky = "nw")

        def enterProject(project_name):
            bH.frames["ProjectWindow"] = ProjectWindow(master = bH.container, controller = self.controller, bH = bH, user_id = user_id, last = "AllProjectsWindow",  proj_name = project_name)
            bH.frames["ProjectWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))
            controller.show_frame("ProjectWindow")

        #Imagem para o botão de join project
        self.joinpIMG = tk.PhotoImage(file = "Assets/User_Interface/joinprojectBtn.png")
        self.leavepIMG = tk.PhotoImage(file = "Assets/User_Interface/leaveprojectBtn.png")

        def join_project(user_id, jlPBTN, project_id):
            cursorJoin = db.cursor()
            addUP = """INSERT INTO User_Projects
                        (user_id, project_id)
                        VALUES (%s, %s)"""
            user_data = (str(user_id), str(project_id))
            cursorJoin.execute(addUP, user_data)
            db.commit()
            cursorJoin.close()
            jlPBTN.config(image = self.leavepIMG)
            jlPBTN.bind("<Button-1>", lambda event, a = user_id, b = jlPBTN, c = project[0]: leave_project(a, b, c))
            return
        
        def leave_project(user_id, jlPBTN, project_id):
            cursorLeave = db.cursor()
            addUP = """DELETE FROM User_Projects
                        WHERE user_id = %s AND project_id = %s"""
            user_data = (str(user_id), str(project_id))
            cursorLeave.execute(addUP, user_data)
            db.commit()
            cursorLeave.close()
            jlPBTN.config(image = self.joinpIMG)
            jlPBTN.bind("<Button-1>", lambda event, a = user_id, b = jlPBTN, c = project[0]: join_project(a, b, c))
            return

        #Alocando os projetos
        i = 1
        for project in projects:
            p_frame = tk.Frame(myproblemsCF, bg = black, height = 20, bd = 2)

            p_frame.grid(row = i, column = 0, sticky = "nsew")
            name_with_space = project[1].replace("_", " ")
            p_name = tk.Label(p_frame, text = name_with_space, font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 15)
            p_name.grid(row = 0, column = 0, sticky = "nsew", padx = (10, 30), pady = 5)
            p_name.bind("<Button-1>", lambda event, a = project[1]: enterProject(a))

            p_status = tk.Label(p_frame, text = project[4], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 8)
            p_status.grid(row = 0, column = 1, sticky = "nsew", padx = 48, pady = 5)
            p_status.bind("<Button-1>", lambda event, a = project[1]: enterProject(a))

            p_category = tk.Label(p_frame, text = project[3], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 8)
            p_category.grid(row = 0, column = 2, sticky = "nwse", padx = (37,30), pady = 5)
            p_category.bind("<Button-1>", lambda event, a = project[1]: enterProject(a))

            p_date = tk.Label(p_frame, text = project[5], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 10)
            p_date.grid(row = 0, column = 3, sticky = "nsew", padx = (78,80), pady = 5)

            cursorCheck = db.cursor(buffered=True)
            cursorCheck.execute("SELECT entry_id FROM User_Projects WHERE user_id = %s AND project_id = %s", (user_id, project[0], ) )
            checkP = cursorCheck.fetchone()
            cursorCheck.close()
            if not checkP:
                jlPBTN = tk.Button(p_frame, image = self.joinpIMG, bd = 0, background = black, activebackground  = black)
                jlPBTN.bind("<Button-1>", lambda event, a = user_id, b = jlPBTN, c = project[0]: join_project(a, b, c))
                jlPBTN.grid(row = 0, column = 4, sticky = "nsew", padx = 20, pady = 5)
            if checkP:
                jlPBTN = tk.Button(p_frame, image = self.leavepIMG, bd = 0, background = black, activebackground  = black)
                jlPBTN.bind("<Button-1>", lambda event, a = user_id, b = jlPBTN, c = project[0]: leave_project(a, b, c))
                jlPBTN.grid(row = 0, column = 4, sticky = "nsew", padx = 20, pady = 5)

            p_date.bind("<Button-1>", lambda event, a = project[1]: enterProject(a))
            
            p_frame.bind("<Enter>",lambda event, a=p_name, b=p_status, c=p_category, d=p_date: 
                            changeOnHover(a, b, c, d))
            p_frame.bind("<Leave>",lambda event, a=p_name, b=p_status, c=p_category, d=p_date: 
                            changeOnLeave(a, b, c, d))
            p_frame.bind("<Button-1>", lambda event, a = project[1]: enterProject(a))
            checkP = None
            i += 1

def changeOnHover(a, b, c, d):
    a.config(fg = forest_Green)
    b.config(fg = forest_Green)
    c.config(fg = forest_Green)
    d.config(fg = forest_Green)
  
def changeOnLeave(a, b, c, d):
    a.config(fg = white82)
    b.config(fg = white82)
    c.config(fg = white82)
    d.config(fg = white82)
