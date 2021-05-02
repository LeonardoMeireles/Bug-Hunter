try:
    import os
    import tkinter as tk
    from os.path import dirname, join
    import sys

    from dotenv import load_dotenv
    from PIL import Image, ImageTk

except Exception as e:
    print("Algumas bibliotecas estão faltando: {}".format(e))

from BH_Home.ProblemWindow import ProblemWindow

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


class ProjectWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id, last, proj_name):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)
        self.proj_name = proj_name
        db = bH.db

        #Titulo da página
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "new", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = self.proj_name, font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 16)
        
        self.rightArrow = tk.PhotoImage(file = "Assets/User_Interface/right_arrow.png")
        arrowR = tk.Label(self, image = self.rightArrow, bd = 0, background = dark_grey, activebackground  = dark_grey)
        arrowR.grid(row = 1, column = 0, padx = 20, pady = 10, sticky = "w")
        typeP = tk.Label(self, text = proj_name, font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
        typeP.grid(row = 1, column = 0, padx = 35, pady = 10, sticky = "w")

        self.newP = tk.PhotoImage(file = "Assets/User_Interface/newproblemBtn.png")
        addP_btn = tk.Button(self, image = self.newP, bd = 0, background = dark_grey, activebackground  = dark_grey, command = lambda: controller.show_frame("NewProjectWindow"))
        addP_btn.grid(row = 1, column = 1, padx = 10, pady = (10,5), sticky = "w")

        self.closeIMG = tk.PhotoImage(file = "Assets/User_Interface/close.png")
        closeX = tk.Button(self, image = self.closeIMG, bd = 0, background = dark_grey, activebackground  = dark_grey, command = lambda: controller.show_frame(last))
        closeX.grid(row = 1, column = 2, sticky = "e", pady = 20, padx = 17)

        #Local que mostrara os projetos
        projectsF = tk.Frame(self, bg = black)
        projectsF.grid(row = 2, column = 0, sticky = "nsew", padx = 17, pady = (5,20), columnspan = 4)
        self.rowconfigure(2, weight = 1)
        canvasP = tk.Canvas(projectsF)
        canvasP.pack(side=tk.LEFT, anchor = tk.N)
        myproblemsCF = tk.Frame(canvasP, bg = black)
        myproblemsCF.pack(fill = "both")
        yscrollbarP = tk.Scrollbar(projectsF, orient = "vertical", command = canvasP.yview, background  = black, activebackground  = black, troughcolor = black)
        yscrollbarP.pack(side = tk.RIGHT, fill = "y")
        #Pegando todos os probelmas do projeto
        cursorAP = db.cursor(buffered=True)
        cursorAP.execute("""
                        SELECT 
                            po.problem_id,
                            po.project_id,
                            po.name,
                            po.reporter,
                            po.status,
                            po.priority,
                            po.description,
                            po.date
                        FROM Problems as po
                        JOIN Projects as pj
                        ON po.project_id = pj.project_id
                        WHERE pj.name = %s
                        ORDER BY po.problem_id DESC
                        """, (proj_name, ))
        problems = cursorAP.fetchall()
        cursorAP.close()
        nomeP = tk.Label(myproblemsCF, text = "NOME DO PROBLEMA", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        nomeP.grid(row = 0, column = 0, padx = 10, sticky = "nw")
        
        reporterP = tk.Label(myproblemsCF, text = "RELATOR", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        reporterP.grid(row = 0, column = 0, padx = 250, sticky = "nw")

        statusP = tk.Label(myproblemsCF, text = "STATUS", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        statusP.grid(row = 0, column = 0, padx = 400, sticky = "nw")

        priorityP = tk.Label(myproblemsCF, text = "PRIORIDADE", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        priorityP.grid(row = 0, column = 0, padx = 550, sticky = "nw")

        dateP = tk.Label(myproblemsCF, text = "DATA", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        dateP.grid(row = 0, column = 0, padx = 750, sticky = "nw")

        def enterProblem(problem_id):
            bH.frames["ProblemWindow"] = ProblemWindow(master = bH.container, controller = self.controller, bH = bH, user_id = user_id, last = "AllProjectsWindow",
                                                        prob_id = problem_id, proj_name = proj_name)
            bH.frames["ProblemWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))
            controller.show_frame("ProblemWindow")

        #Alocando os projetos
        i = 1
        for problem in problems:
            p_frame = tk.Frame(myproblemsCF, bg = black, height = 20, bd = 2)

            p_frame.grid(row = i, column = 0, sticky = "nsew")
            name_with_space = problem[2].replace("_", " ")
            p_name = tk.Label(p_frame, text = name_with_space, font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 15)
            p_name.grid(row = 0, column = 0, sticky = "nsew", padx = (22, 25), pady = 5)
            p_name.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))

            p_reporter = tk.Label(p_frame, text = problem[3], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 8)
            p_reporter.grid(row = 0, column = 1, sticky = "nsew", padx = (47,20), pady = 5)
            p_reporter.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))

            p_status = tk.Label(p_frame, text = problem[4], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 15)
            p_status.grid(row = 0, column = 2, sticky = "nwse", padx = (5,15), pady = 5)
            p_status.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))

            p_priority = tk.Label(p_frame, text = problem[5], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 10)
            p_priority.grid(row = 0, column = 3, sticky = "nwse", padx = (28, 40), pady = 5)
            p_priority.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))

            p_date = tk.Label(p_frame, text = problem[7], font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = white82, width = 10)
            p_date.grid(row = 0, column = 4, sticky = "nsew", padx = 52, pady = 5)
            p_date.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))

            p_frame.bind("<Enter>",lambda event, a=p_name, b=p_reporter, c=p_status, d=p_priority, e=p_date: 
                            changeOnHover(a, b, c, d, e))
            p_frame.bind("<Leave>",lambda event, a=p_name, b=p_reporter, c=p_status, d=p_priority, e=p_date: 
                            changeOnLeave(a, b, c, d, e))
            p_frame.bind("<Button-1>", lambda event, a = problem[0]: enterProblem(a))
            i += 1

def changeOnHover(a, b, c, d, e):
    a.config(fg = forest_Green)
    b.config(fg = forest_Green)
    c.config(fg = forest_Green)
    d.config(fg = forest_Green)
    e.config(fg = forest_Green)
  
def changeOnLeave(a, b, c, d, e):
    a.config(fg = white82)
    b.config(fg = white82)
    c.config(fg = white82)
    d.config(fg = white82)
    e.config(fg = white82)
