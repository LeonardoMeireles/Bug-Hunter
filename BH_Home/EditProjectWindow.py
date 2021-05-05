try:
    import os
    import tkinter as tk
    import tkinter.scrolledtext as scrolledtext
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
grey = "#3a3d45"
dark_grey = "#202021"
white82 = "#dfdfdf"
ativo = "#3592e3"
atrasado = "#d9aa55"
planejamento = "#bbbf69"
cancelado = "#d94f48"
concluido = "#6ebd6c"


class EditProjectWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id, last, proj_id):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)
        db = bH.db

        #Pegando todos a informação do projeto
        cursorAP = db.cursor(buffered=True)
        cursorAP.execute("SELECT * from Projects WHERE project_id = %s", (proj_id, ))
        project = cursorAP.fetchone()
        cursorAP.close()

        #Titulo da página
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "new", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = "Editar Projeto " +project[1], font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 20)

        self.rightArrow = tk.PhotoImage(file = "Assets/User_Interface/right_arrow.png")
        arrowR = tk.Label(self, image = self.rightArrow, bd = 0, background = dark_grey, activebackground  = dark_grey)
        arrowR.grid(row = 1, column = 0, padx = 20, pady = 10, sticky = "w")
        typeP = tk.Label(self, text = project[1], font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
        typeP.grid(row = 1, column = 0, padx = 35, pady = 10, sticky = "w")

        self.closeIMG = tk.PhotoImage(file = "Assets/User_Interface/close.png")
        closeX = tk.Button(self, image = self.closeIMG, bd = 0, background = dark_grey, activebackground  = dark_grey, command = lambda: controller.show_frame(last))
        closeX.grid(row = 1, column = 1, sticky = "e", pady = 20, padx = 17)

        #Local que mostrara o projeto
        def _on_mousewheel(event):
          self.canvasP.yview_scroll(int(-1*(event.delta/120)), "units")

        projectsF = tk.Frame(self, bg = black, bd = 0)
        projectsF.grid(row = 3, column = 0, sticky = "nsew", padx = 17, pady = (5,20), columnspan = 4)
        self.rowconfigure(3, weight = 1)
        self.canvasP = tk.Canvas(projectsF, bg = black, bd = 0, highlightthickness = 0)
        self.canvasP.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        projectCF = tk.Frame(self.canvasP, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasP.create_window((0,0), window = projectCF, anchor = "nw")
        self.canvasP.configure(background = black)
        self.canvasP.bind_all("<MouseWheel>", _on_mousewheel)

        def defAtivo(statusB, statusS, cursorSP):
            statusB.config(text = "Ativo", bg = ativo, activebackground  = ativo)
            cursorSP.execute("""UPDATE Projects SET status = "Ativo" WHERE project_id = %s """, (proj_id, ))
            db.commit()
            statusS.set("Ativo")
            return

        def defAtrasado(statusB, statusS, cursorSP):
            statusB.config(text = "Atrasado", bg = ativo, activebackground  = ativo)
            cursorSP.execute("""UPDATE Projects SET status = "Atrasado" WHERE project_id = %s """, (proj_id, ))
            db.commit()
            statusS.set("Atrasado")
            return
        
        def defP(statusB, statusS, cursorSP):
            statusB.config(text = "Planejamento", bg = planejamento, activebackground  = planejamento)
            cursorSP.execute("""UPDATE Projects SET status = "Planejamento" WHERE project_id = %s """, (proj_id, ))
            db.commit()
            statusS.set("Planejamento")
            return
        
        def defCancelado(statusB, statusS, cursorSP):
            statusB.config(text = "Cancelado", bg = cancelado, activebackground  = cancelado)
            cursorSP.execute("""UPDATE Projects SET status = "Cancelado" WHERE project_id = %s """, (proj_id, ))
            db.commit()
            statusS.set("Cancelado")
            return
        
        def defConcluido(statusB, statusS, cursorSP):
            statusB.config(text = "Concluido", bg = cancelado, activebackground  = cancelado)
            cursorSP.execute("""UPDATE Projects SET status = "Concluido" WHERE project_id = %s """, (proj_id, ))
            db.commit()
            statusS.set("Concluido")
            return

        def invokeStatusS(invokeN, status):
            if status == "Ativo":
                statusB.menu.invoke(0)
            elif status == "Atrasado":
                statusB.menu.invoke(1)
            elif status == "Planejamento":
                statusB.menu.invoke(2)
            elif status == "Cancelado":
                statusB.menu.invoke(3)
            elif status == "Concluido":
                statusB.menu.invoke(4)

        #Cursor usado para modificar status e prioridade
        cursorSP = db.cursor()

        #Alocando todas as informações do problema
        statusP = tk.Label(projectCF, text = "STATUS", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        statusP.grid(row = 0, column = 0, padx = 18, pady = (10,5), sticky = "nw")

        statusS = tk.StringVar()
        statusS.set(project[4])
        statusB = tk.Menubutton(projectCF, text = "Ativo", font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = ativo, activebackground  = ativo,
                                activeforeground = white82)
        statusB.grid(row = 1, column = 0, padx = 20, pady = (8,5), sticky = "w")
        statusB.menu = tk.Menu(statusB, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        statusB["menu"] = statusB.menu
        statusB.menu.add_radiobutton(label = "Ativo", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defAtivo(statusB, statusS, cursorSP))
        statusB.menu.add_radiobutton(label = "Atrasado", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defAtrasado(statusB, statusS, cursorSP))
        statusB.menu.add_radiobutton(label = "Planejamento", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defP(statusB, statusS, cursorSP))
        statusB.menu.add_radiobutton(label = "Cancelado", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defCancelado(statusB, statusS, cursorSP))
        statusB.menu.add_radiobutton(label = "Concluido", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defConcluido(statusB, statusS, cursorSP))
        invokeStatusS(statusB, project[4])

        discriptionL = tk.Label(projectCF, text = "DESCRIÇÃO", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        discriptionL.grid(row = 2, column = 0, padx = 18, pady = 10, sticky = "nw")
        descricaoE = tk.Text(projectCF, undo=True, bg = black, fg = white82, bd = 0, width = 50, height = 10)
        descricaoE.config( font = ("Montserrat", 12) )
        descricaoE.insert(tk.END, project[2])
        descricaoE.grid(row = 3, column = 0, sticky = "new", padx = 20, pady = 10)


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