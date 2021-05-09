try:
    import os
    import tkinter as tk
    import tkinter.scrolledtext as scrolledtext
    from os.path import dirname, join
    import sys
    from datetime import date

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
grey = "#3a3d45"
dark_grey = "#202021"
white82 = "#dfdfdf"
ativo = "#3592e3"
atrasado = "#d9aa55"
planejamento = "#bbbf69"
cancelado = "#d94f48"
concluido = "#6ebd6c"

class NewProblemWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)
        self.user_id = user_id
        db = bH.db

        #Titulo da página
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "nsew", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = "Novo Problema", font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 16)

        #Local para coletar informações
        pF = tk.Frame(self, bg = black)
        pF.grid(row = 1, column = 0, sticky = "new", padx = 10, pady = (10,10), columnspan = 4)
        self.rowconfigure(2, weight = 1)

        def defProjeto(problem_proj, projectSelect):
            name = problem_proj.get()
            projectSelect.config(text = name)
            return

        #Carrega novamente os projetos (caso foi adicionado um projeto novo, deve clicar nesse botão para ele aparecer)
        def reloadProjects(projectSelect):
            db.commit()
            cursorPS = db.cursor()
            cursorPS.execute("SELECT * FROM Projects")
            projects = cursorPS.fetchall()
            if cursorPS.rowcount != 0:
                projectSelect.menu.delete(0, cursorPS.rowcount)
                for project in projects:
                    name_project = project[1]
                    nameP = name_project.replace("_", " ")
                    projectSelect.menu.add_radiobutton(label = nameP, font = ("Montserrat", 9), variable = problem_proj, selectcolor = teal_Green,
                                                        command = lambda: defProjeto(problem_proj, projectSelect))
            else:
                projectSelect.menu.add_radiobutton(label = "Não existem projetos", font = ("Montserrat", 9), variable = problem_proj, selectcolor = teal_Green)

            cursorPS.close()

        ProjetoL = tk.Label(pF, text = "Projeto", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        ProjetoL.grid(row = 0, column = 0, padx = 25, pady = 10, sticky = "w")
        self.refresh = tk.PhotoImage(file = "Assets/User_Interface/reload.png")
        problem_proj = tk.StringVar()
        problem_proj.set("ERROR")
        projectSelect = tk.Menubutton(pF, text = "Selecionar projeto", font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = "#777777", activebackground  = "#777777",
                                activeforeground = white82)
        projectSelect.grid(row = 1, column = 0, padx = 30, pady = (8,5), sticky = "w")
        projectSelect.menu = tk.Menu(projectSelect, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        projectSelect["menu"] = projectSelect.menu
        cursorPS = db.cursor()
        cursorPS.execute("SELECT * FROM Projects")
        projects = cursorPS.fetchall()
        if cursorPS.rowcount != 0:
            for project in projects:
                name_project = project[1]
                nameP = name_project.replace("_", " ")
                projectSelect.menu.add_radiobutton(label = nameP, font = ("Montserrat", 9), variable = problem_proj, selectcolor = teal_Green,
                                                    command = lambda: defProjeto(problem_proj, projectSelect))
        else:
            projectSelect.menu.add_radiobutton(label = "Não existem projetos", font = ("Montserrat", 9), variable = problem_proj, selectcolor = teal_Green)
        cursorPS.close()
        reloadP = tk.Button(pF, image = self.refresh, bd = 0, background = black, activebackground  = black, command = lambda: reloadProjects(projectSelect))
        reloadP.grid(row = 0, column = 0, padx = 100, pady = 10, sticky = "w")

        #Titulo do Problema
        tituloL = tk.Label(pF, text = "Titulo do problema", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        tituloL.grid(row = 2, column = 0, padx = 24, pady = 10, sticky = "w")
        tituloE = tk.Entry(pF, font = ("Montserrat", 12), fg = "#d3d3d3", bg = "#777777", bd = 0, width = 50)
        tituloE.grid(row = 3, column = 0, padx = 29, pady = 5, ipady = 4, sticky = "nsw")

        #Descrição do problema
        descricaoL = tk.Label(pF, text = "Descrição", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        descricaoL.grid(row = 4, column = 0, padx = 25, pady = 10, sticky = "w")
        descricaoF = tk.Frame(pF, width = 50, height = 20)
        descricaoF.grid(row = 5, column = 0, sticky = "new", padx = 30, pady = 10)
        descricaoF.grid_propagate(False)
        descricaoE = scrolledtext.ScrolledText(descricaoF, undo=True, bg = "#777777", fg = "#d3d3d3", bd = 0, width = 50, height = 10)
        descricaoE['font'] = ("Montserrat", '12')
        descricaoE.pack()

        #Prioridade do problema
        def defNA(statusB):
            statusB.config(text = "Não-urgente", bg = ativo, activebackground  = ativo)
            return

        def defG(statusB):
            statusB.config(text = "Grave", bg = atrasado, activebackground  = atrasado)
            return
        
        def defC(statusB):
            statusB.config(text = "Crítico", bg = cancelado, activebackground  = cancelado)
            return

        prioridadeS = tk.StringVar()
        prioridadeS.set("Aberto")
        prioridadeL = tk.Label(pF, text = "Prioridade", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        prioridadeL.grid(row = 6, column = 0, padx = 25, pady = 10, sticky = "w")
        prioridadeB = tk.Menubutton(pF, text = "Aberto", font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = ativo, activebackground  = ativo,
                                activeforeground = white82)
        prioridadeB.grid(row = 7, column = 0, padx = 30, pady = (8,5), sticky = "w")
        prioridadeB.menu = tk.Menu(prioridadeB, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        prioridadeB["menu"] = prioridadeB.menu
        prioridadeB.menu.add_radiobutton(label = "Não-urgente", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defNA(prioridadeB))
        prioridadeB.menu.add_radiobutton(label = "Grave", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defG(prioridadeB))
        prioridadeB.menu.add_radiobutton(label = "Crítico", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defC(prioridadeB))
        prioridadeB.menu.invoke(0)

        errorM = tk.Label(pF, text = " ", font = ("Montserrat", 12), fg = teal_Green, bg = black)
        errorM.grid(row = 8, column = 0, sticky = "w", padx = 25, pady = 5)

        def limpar_entrys():
            projectSelect.config(text = "Selecionar projeto")
            tituloE.delete(0, tk.END)
            descricaoE.delete('1.0', tk.END)
            prioridadeB.menu.invoke(0)
            return

        def addProblem(errorM):
            projectName = problem_proj.get()
            nameP = str(projectName.replace(" ", "_"))
            titulo = tituloE.get()
            descricao = descricaoE.get("1.0", tk.END)
            prioridade = prioridadeS.get()
            if ( titulo == ""):
                errorM.config(text = "Nomeie seu problema")
                return
            if (nameP == "ERROR"):
                errorM.config(text = "Não existem projetos")
                return

            #Project id do projeto selecionado
            cursorPI = db.cursor()
            find_pid = """SELECT project_id from Projects WHERE name = %s"""
            cursorPI.execute(find_pid, (nameP,))
            project_id = cursorPI.fetchone()
            cursorPI.close()

            #Nome do usuário que reportou o problema
            cursorN = db.cursor()
            cursorN.execute("SELECT name FROM Users WHERE user_id = " +str(self.user_id))
            reporter = cursorN.fetchone()
            cursorN.close()

            #A data atual
            from datetime import date
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            
            add_problem = "INSERT INTO Problems (name, project_id, reporter, status, priority, description, date) VALUES (%s, %s, %s, %s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'))"
            '''add_activity = "INSERT INTO Activity (type, user_id, problem_id, project_id, date) VALUES (%s, %s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'))"
            activity_data = ("0", str(self.user_id), str(cursorP.lastrowid), str(project_id[0]), str(d1))
            cursorP.execute(add_activity, activity_data) '''
            problem_data = (str(titulo), str(project_id[0]), str(reporter[0]), "Aberto", str(prioridade), str(descricao), str(d1) )
            cursorP = db.cursor()
            cursorP.execute(add_problem, problem_data)

            db.commit()
            cursorP.close()
            errorM.config(text = "Problema relatado!", fg = forest_Green)
            limpar_entrys()
            return


        self.addP = tk.PhotoImage(file = "Assets/User_Interface/addProjectBtn.png")
        adicionarB = tk.Button(pF, image = self.addP, bd = 0, background = black, activebackground  = black, command = lambda: addProblem(errorM))
        adicionarB.grid(row = 9, column = 0, padx = 25, pady = 20, sticky = "w")

        self.cancelP = tk.PhotoImage(file = "Assets/User_Interface/cancelProjectBtn.png")
        cancelB = tk.Button(pF, image = self.cancelP, bd = 0, background = black, activebackground  = black, command = lambda: limpar_entrys())
        cancelB.grid(row = 9, column = 0, padx = 140, pady = 20, sticky = "w")