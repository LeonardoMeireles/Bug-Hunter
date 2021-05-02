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

class HomeWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)

        #Titulo da págin
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "new", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = "Página Inicial", font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 16)

        def _on_mousewheel(event):
            self.canvasMP.yview_scroll(int(-1*(event.delta/120)), "units")

        #Frame que armazena problemas dos projetos que o usuário faz parte
        myproblemsF = tk.Frame(self, bg = black)
        myproblemsF.grid(row = 1, column = 0, sticky = "nsew", padx = 17, pady = 10, columnspan = 4)
        canvasFrameMP = tk.Frame(myproblemsF, bg = black)
        canvasFrameMP.grid(row = 1, column = 0, ipadx = 5)
        self.canvasMP = tk.Canvas(canvasFrameMP, bg = black, bd = 0, highlightthickness = 0)
        self.canvasMP.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        mpCF = tk.Frame(self.canvasMP, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasMP.create_window((0,0), window = mpCF, anchor = "nw")
        self.canvasMP.configure(background = black)
        self.canvasMP.bind_all("<MouseWheel>", _on_mousewheel)

        def forget_MPF():
            canvasFrameMP.grid_forget()

        def return_MPF():
            canvasFrameMP.grid(row = 1, column = 0, ipadx = 5)

        def showP(arrowP, myproblemsF, canvasFrameMP):
            arrowP.config( image = self.downArrow, command = lambda: hideP(arrowP,myproblemsF, mpCF))
            return_MPF()
            return

        def hideP(arrowP, myproblemsF, canvasFrameMP):
            arrowP.config( image = self.upArrow, command = lambda: showP(arrowP, myproblemsF, mpCF))
            forget_MPF()
            return

        def enterProblem(problem_id, proj_name):
                bH.frames["ProblemWindow"] = ProblemWindow(master = bH.container, controller = self.controller, bH = bH, user_id = user_id, last = "HomeWindow",
                                                            prob_id = problem_id, proj_name = proj_name)
                bH.frames["ProblemWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))
                controller.show_frame("ProblemWindow")    

        def reloadP(mpCF):
            cursorProjects = db.cursor(buffered=True)
            cursorProjects.execute("""
                                    SELECT po.problem_id
                                    FROM Problems as po
                                    LEFT JOIN User_Projects as up
                                    ON po.project_id = up.project_id
                                    WHERE user_id = %s AND po.status <> "Fechado"
                                    ORDER BY po.problem_id DESC
                                    """,
                                    (user_id, ))
            projectsMP = cursorProjects.fetchall()
            cursorProjects.close()

            i = 1
            for pID in projectsMP:
                p_frame = tk.Frame(mpCF, bg = black, height = 25, bd = 2)
                p_frame.grid(row = i, column = 0, sticky = "nsew", pady = 5, padx = 30, columnspan = 4)

                cursorMP = db.cursor()
                cursorMP.execute("""
                                SELECT 
                                    po.name,
                                    po.date,
                                    pj.name
                                FROM Problems po
                                JOIN Projects pj
                                    ON pj.project_id = po.project_id
                                WHERE po.problem_id = %s""", (str(pID[0]), ))
                problem = cursorMP.fetchone()
                cursorMP.close()

                p_name = tk.Label(p_frame, text = problem[0], font = ("Montserrat SemiBold", 12), foreground = white82, borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_name.grid(row = 0, column = 0, sticky = "nw", padx = 18, pady = (8,0))
                p_name.bind("<Button-1>", lambda event, a = pID[0], b = problem[2] : enterProblem(a, b))

                p_date = tk.Label(p_frame, text = problem[1], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_date.grid(row = 0, column = 1, sticky = "ne", padx = 10, pady = 13)
                p_date.bind("<Button-1>", lambda event, a = pID[0], b = problem[2] : enterProblem(a, b))
                

                p_projectName = tk.Label(p_frame, text = problem[2], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82, width = 8)
                p_projectName.grid(row = 1, column = 0, sticky = "nw", padx = 18, pady = 2)
                p_projectName.bind("<Button-1>", lambda event, a = pID[0], b = problem[2] : enterProblem(a, b))
            
                p_frame.bind("<Enter>",lambda event, a=p_name, b=p_date, c=p_projectName: 
                                changeOnHover(a, b, c))
                p_frame.bind("<Leave>",lambda event, a=p_name, b=p_date, c=p_projectName: 
                                changeOnLeave(a, b, c))
                p_frame.bind("<Button-1>", lambda event, a = pID[0], b = problem[2] :
                                enterProblem(a, b))

                i += 1
            return

        self.downArrow = tk.PhotoImage(file = "Assets/User_Interface/down_arrow.png")
        self.upArrow = tk.PhotoImage(file = "Assets/User_Interface/up_arrow.png")
        arrowP = tk.Button(myproblemsF, image = self.downArrow, bd = 0, background = black, activebackground  = black, command = lambda: hideP(arrowP, myproblemsF, canvasFrameMP))
        arrowP.grid(row = 0, column = 0, pady = (12,10), padx = 15, sticky = "nw")

        problemsL = tk.Label(myproblemsF, text = "Meus Problemas", font = ("Montserrat", 14), bg = black, fg = white82)
        problemsL.grid(row = 0, column = 0, sticky = "nw", padx = 45, pady = 5)

        self.reload_img = tk.PhotoImage(file = "Assets/User_Interface/reload.png")
        reloadPButton = tk.Button(myproblemsF, image = self.reload_img, bd = 0, background = black, activebackground  = black, command = lambda: reloadP(mpCF))
        reloadPButton.grid(row = 0, column = 1, sticky = "ne", padx = 10, pady = 12)
        myproblemsF.columnconfigure(1, weight = 1)
        reloadP(mpCF)

        ''' #Frame que mostra as atividades recentes de projetos que o usuário participa
        activitiesF = tk.Frame(self, bg = black)
        activitiesF.grid(row = 1, column = 4, sticky = "nsew", padx = 17, pady = 10, columnspan = 4)
        canvasFrameA = tk.Frame(activitiesF, bg = black)
        canvasFrameA.grid(row = 1, column = 1, columnspan = 2, ipadx = 5)
        self.canvasA = tk.Canvas(canvasFrameA, bg = black, bd = 0, highlightthickness = 0)
        self.canvasA.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        aCF = tk.Frame(self.canvasA, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasA.create_window((0,0), window = aCF, anchor = "nw")
        self.canvasA.configure(background = black)
        self.canvasA.bind_all("<MouseWheel>", _on_mousewheel)

        def showA(arrowA, activitiesF, canvasFrameA):
            arrowA.config( image = self.downArrow, command = lambda: hideP(arrowA, activitiesF, aCF))
            canvasFrameA.grid(row = 1, column = 0, columnspan = 2)
            return

        def hideA(arrowA, activitiesF, canvasFrameA):
            arrowA.config( image = self.upArrow, command = lambda: showP(arrowA, activitiesF, aCF))
            canvasFrameA.grid_forget()
            return

        #Preciso arrumar a chamada MYSQL
        def reloadA(mpCF):
            cursorProjects = db.cursor(buffered=True)
            cursorProjects.execute("""
                                    SELECT *
                                    FROM Activity as ac
                                    LEFT JOIN User_Projects as up
                                    ON ac.project_id = up.project_id
                                    WHERE user_id = %s
                                    ORDER BY ac.activity_id DESC
                                    """,
                                    (user_id, ))
            listA = cursorProjects.fetchall()
            cursorProjects.close()

            i = 1
            for act in listA:
                p_frame = tk.Frame(mpCF, bg = black, height = 20, bd = 2)
                p_frame.grid(row = i, column = 0, sticky = "nsew", pady = 5, padx = 15, columnspan = 4)

                p_name = tk.Label(p_frame, text = problem[0], font = ("Montserrat SemiBold", 12), foreground = white82, borderwidth = 0, background = black,
                                    activeforeground = white82, width = 15)
                p_name.grid(row = 0, column = 0, sticky = "nw", padx = 5, pady = 5)

                p_date = tk.Label(p_frame, text = problem[1], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_date.grid(row = 0, column = 1, sticky = "ne", padx = 10, pady = 5)
                

                p_projectName = tk.Label(p_frame, text = problem[2], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82, width = 8)
                p_projectName.grid(row = 1, column = 0, sticky = "nw", padx = 20, pady = 5)

                i += 1
                return

        arrowA = tk.Button(activitiesF, image = self.downArrow, bd = 0, background = black, activebackground  = black, command = lambda: hideA(arrowA))
        arrowA.grid(row = 0, column = 0, pady = (10,10), padx = 8)

        recentL = tk.Label(activitiesF, text = "Atividade Recente", font = ("Montserrat", 14), bg = black, fg = white82)
        recentL.grid(row = 0, column = 1, sticky = "nsew", padx = 2, pady = 5)
        
        reloadA = tk.Button(activitiesF, image = self.reload_img, bd = 0, background = black, activebackground  = black, command = lambda: reloadA)
        reloadA.grid(row = 0, column = 2, sticky = "e", padx = 8)
        activitiesF.columnconfigure(2, weight = 1) '''

        #Frame que armazena todos os problemas
        allproblemsF = tk.Frame(self, bg = black)
        allproblemsF.grid(row = 2, column = 0, sticky = "nsew", padx = 17, pady = 10, columnspan = 4)
        canvasFrameAP = tk.Frame(allproblemsF, bg = black)
        canvasFrameAP.grid(row = 1, column = 0, ipadx = 5)
        self.canvasAP = tk.Canvas(canvasFrameAP, bg = black, bd = 0, highlightthickness = 0)
        self.canvasAP.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        apCF = tk.Frame(self.canvasAP, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasAP.create_window((0,0), window = apCF, anchor = "nw")
        self.canvasAP.configure(background = black)
        self.canvasAP.bind_all("<MouseWheel>", _on_mousewheel)

        def forget_APF():
            canvasFrameAP.grid_forget()

        def return_APF():
            canvasFrameAP.grid(row = 1, column = 0, ipadx = 5)

        def showAP(arrowAP, myproblemsF, canvasFrameMP):
            arrowAP.config( image = self.downArrow, command = lambda: hideP(arrowAP,myproblemsF, mpCF))
            return_APF()
            return

        def hideAP(arrowAP, myproblemsF, canvasFrameMP):
            arrowAP.config( image = self.upArrow, command = lambda: showP(arrowAP, myproblemsF, mpCF))
            forget_APF()
            return

        def enterProblem(problem_id, proj_name):
                bH.frames["ProblemWindow"] = ProblemWindow(master = bH.container, controller = self.controller, bH = bH, user_id = user_id, last = "HomeWindow",
                                                            prob_id = problem_id, proj_name = proj_name)
                bH.frames["ProblemWindow"].grid(row = 0, column = 0, sticky = "nsew", pady = (53, 0))
                controller.show_frame("ProblemWindow")    

        def reloadAP(apCF):
            cursorAP = db.cursor()
            cursorAP.execute("""
                                    SELECT
                                        po.name,
                                        po.date,
                                        po.problem_id,
                                        pj.name
                                    FROM Problems as po
                                    JOIN Projects as pj
                                    ON po.project_id = pj.project_id
                                    WHERE po.status <> "Fechado"
                                    ORDER BY po.problem_id DESC
                                    """
                                    )
            allproblems = cursorAP.fetchall()
            cursorAP.close()

            i = 1
            for problem in allproblems:
                p_frame = tk.Frame(apCF, bg = black, height = 25, bd = 2)
                p_frame.grid(row = i, column = 0, sticky = "nsew", pady = 5, padx = 27, columnspan = 4)

                p_name = tk.Label(p_frame, text = problem[0], font = ("Montserrat SemiBold", 12), foreground = white82, borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_name.grid(row = 0, column = 0, sticky = "nw", padx = 18, pady = (8,0))
                p_name.bind("<Button-1>", lambda event, a = problem[2], b = problem[3] : enterProblem(a, b))

                p_date = tk.Label(p_frame, text = problem[1], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_date.grid(row = 0, column = 1, sticky = "ne", padx = 10, pady = 13)
                p_date.bind("<Button-1>", lambda event, a = problem[2], b = problem[3] : enterProblem(a, b))
                

                p_projectName = tk.Label(p_frame, text = problem[3], font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = black,
                                    activeforeground = white82)
                p_projectName.grid(row = 1, column = 0, sticky = "nw", padx = 20, pady = 2)
                p_projectName.bind("<Button-1>", lambda event, a = problem[2], b = problem[3] : enterProblem(a, b))
            
                p_frame.bind("<Enter>",lambda event, a=p_name, b=p_date, c=p_projectName: 
                                changeOnHover(a, b, c))
                p_frame.bind("<Leave>",lambda event, a=p_name, b=p_date, c=p_projectName: 
                                changeOnLeave(a, b, c))
                p_frame.bind("<Button-1>", lambda event, a = problem[2], b = problem[3] :
                                enterProblem(a, b))

                i += 1
            return

        arrowAP = tk.Button(allproblemsF, image = self.downArrow, bd = 0, background = black, activebackground  = black, command = lambda: hideAP(arrowAP, allproblemsF, canvasFrameMP))
        arrowAP.grid(row = 0, column = 0, pady = (12,10), padx = 15, sticky = "nw")

        allproblemsL = tk.Label(allproblemsF, text = "Todos os problemas", font = ("Montserrat", 14), bg = black, fg = white82)
        allproblemsL.grid(row = 0, column = 0, sticky = "nw", padx = 45, pady = 5)

        reloadAPButton = tk.Button(allproblemsF, image = self.reload_img, bd = 0, background = black, activebackground  = black, command = lambda: reloadAP(apCF))
        reloadAPButton.grid(row = 0, column = 1, sticky = "ne", padx = 10, pady = 12)
        allproblemsF.columnconfigure(1, weight = 1)
        reloadAP(apCF)

def changeOnHover(a, b, c):
    a.config(fg = forest_Green)
    b.config(fg = forest_Green)
    c.config(fg = forest_Green)
            
def changeOnLeave(a, b, c):
    a.config(fg = white82)
    b.config(fg = white82)
    c.config(fg = white82)