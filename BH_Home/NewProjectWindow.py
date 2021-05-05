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

class NewProjectWindow(tk.Frame):
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
        page_name = tk.Label(titleP, text = "Novo Projeto", font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 16)

        #Local para coletar informações
        pF = tk.Frame(self, bg = black)
        pF.grid(row = 1, column = 0, sticky = "new", padx = 10, pady = (10,10), columnspan = 4)
        self.rowconfigure(2, weight = 1)

        tituloProjetoL = tk.Label(pF, text = "Título do projeto", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        tituloProjetoL.grid(row = 0, column = 0, padx = 25, pady = 10, sticky = "w")
        tituloProjetoE = tk.Entry(pF, font = ("Montserrat", 12), fg = "#d3d3d3", bg = "#777777", bd = 0, width = 50)
        tituloProjetoE.grid(row = 1, column = 0, padx = 29, pady = 5, ipady = 4, sticky = "nsw")

        categoriaL = tk.Label(pF, text = "Categoria", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        categoriaL.grid(row = 2, column = 0, padx = 24, pady = 10, sticky = "w")
        categoriaE = tk.Entry(pF, font = ("Montserrat", 12), fg = "#d3d3d3", bg = "#777777", bd = 0, width = 50)
        categoriaE.grid(row = 3, column = 0, padx = 29, pady = 5, ipady = 4, sticky = "nsw")

        descricaoL = tk.Label(pF, text = "Descrição", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        descricaoL.grid(row = 4, column = 0, padx = 25, pady = 10, sticky = "w")
        descricaoF = tk.Frame(pF, width = 50, height = 20)
        descricaoF.grid(row = 5, column = 0, sticky = "new", padx = 30, pady = 10)
        descricaoF.grid_propagate(False)
        descricaoE = scrolledtext.ScrolledText(descricaoF, undo=True, bg = "#777777", fg = "#d3d3d3", bd = 0, width = 50, height = 10)
        descricaoE['font'] = ("Montserrat", '12')
        descricaoE.pack()

        def defAtivado(statusB):
            statusB.config(text = "Ativo", bg = ativo, activebackground  = ativo)
            return
        
        def defAtrasado(statusB):
            statusB.config(text = "Atrasado", bg = atrasado, activebackground  = atrasado)
            return
        
        def defPlanejamento(statusB):
            statusB.config(text = "Planejamento", bg = planejamento, activebackground  = planejamento)
            return
        
        def defCancelado(statusB):
            statusB.config(text = "Cancelado", bg = cancelado, activebackground  = cancelado)
            return
        
        def defConcluido(statusB):
            statusB.config(text = "Concluido", bg = concluido, activebackground  = concluido)
            return

        statusP = tk.StringVar()
        statusP.set("Ativo")
        statusL = tk.Label(pF, text = "Status", font = ("Montserrat SemiBold", 12), fg = "#d3d3d3", bg = black)
        statusL.grid(row = 6, column = 0, padx = 25, pady = 10, sticky = "w")
        statusB = tk.Menubutton(pF, text = "Ativo", font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = ativo, activebackground  = ativo,
                                activeforeground = white82)
        statusB.grid(row = 7, column = 0, padx = 30, pady = (8,5), sticky = "w")
        statusB.menu = tk.Menu(statusB, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        statusB["menu"] = statusB.menu
        statusB.menu.add_radiobutton(label = "Ativo", font = ("Montserrat", 9), variable = statusP, selectcolor = teal_Green, command = lambda: defAtivado(statusB))
        statusB.menu.add_radiobutton(label = "Atrasado", font = ("Montserrat", 9), variable = statusP, selectcolor = teal_Green, command = lambda: defAtrasado(statusB))
        statusB.menu.add_radiobutton(label = "Planejamento", font = ("Montserrat", 9), variable = statusP, selectcolor = teal_Green, command = lambda: defPlanejamento(statusB))
        statusB.menu.add_radiobutton(label = "Cancelado", font = ("Montserrat", 9), variable = statusP, selectcolor = teal_Green, command = lambda: defCancelado(statusB))
        statusB.menu.add_radiobutton(label = "Concluido", font = ("Montserrat", 9), variable = statusP, selectcolor = teal_Green, command = lambda: defConcluido(statusB))
        statusB.menu.invoke(0)

        errorM = tk.Label(pF, text = " ", font = ("Montserrat", 12), fg = teal_Green, bg = black)
        errorM.grid(row = 8, column = 0, sticky = "w", padx = 25, pady = 5)

        def limpar_entrys():
            tituloProjetoE.delete(0, tk.END)
            categoriaE.delete(0, tk.END)
            descricaoE.delete('1.0', tk.END)
            statusB.menu.invoke(0)
            return

        def addProject(errorM):
            projectName = tituloProjetoE.get()
            nameP = projectName.replace(" ", "_")
            categoriaP = categoriaE.get()
            descricaoP = descricaoE.get("1.0", tk.END)
            status = statusP.get()
            if ( nameP == ""):
                errorM.config(text = "Nomeie seu projeto")
                return
            cursorP = db.cursor()
            add_project = """INSERT INTO Projects
                        (name, category, description, status, date)
                        VALUES (%s, %s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'))"""

            #A data atual
            from datetime import date

            today = date.today()
            d1 = today.strftime("%d/%m/%Y")

            project_data = (str(nameP), str(categoriaP), str(descricaoP), str(status), str(d1) )
            cursorP.execute(add_project, project_data)
            '''add_activity = "INSERT INTO Activity (type, user_id, project_id, date) VALUES (%s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'))"
            activity_data = ("1", str(self.user_id), str(cursorP.lastrowid), str(d1))
            cursorP.execute(add_activity, activity_data) '''
            db.commit()
            errorM.config(text = "Projeto cadastrado!", fg = forest_Green)
            limpar_entrys()
            cursorP.close()
            return


        self.addP = tk.PhotoImage(file = "Assets/User_Interface/addProjectBtn.png")
        adicionarB = tk.Button(pF, image = self.addP, bd = 0, background = black, activebackground  = black, command = lambda: addProject(errorM))
        adicionarB.grid(row = 9, column = 0, padx = 25, pady = 20, sticky = "w")

        self.cancelP = tk.PhotoImage(file = "Assets/User_Interface/cancelProjectBtn.png")
        cancelB = tk.Button(pF, image = self.cancelP, bd = 0, background = black, activebackground  = black, command = lambda: limpar_entrys())
        cancelB.grid(row = 9, column = 0, padx = 140, pady = 20, sticky = "w")