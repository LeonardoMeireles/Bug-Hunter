try:
    import os
    import tkinter as tk
    import tkinter.scrolledtext as scrolledtext
    from os.path import dirname, join
    import sys
    import datetime

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


class ProblemWindow(tk.Frame):
    def __init__(self, master, controller, bH, user_id, last, prob_id, proj_name, proj_id):
        #Frame de login
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.config(bg = dark_grey)
        self.prob_id = prob_id
        db = bH.db

        #Pegando todos a informação do probelma
        cursorAP = db.cursor(buffered=True)
        cursorAP.execute("SELECT * from Problems WHERE problem_id = %s", (prob_id, ))
        problem = cursorAP.fetchone()
        cursorAP.close()

        #Titulo da página
        titleP = tk.Frame(self, bg = "#014039")
        titleP.grid(row = 0, column = 0, sticky = "new", columnspan = 100)
        self.columnconfigure(0, weight = 1)
        page_name = tk.Label(titleP, text = "Problema", font = ("Montserrat SemiBold", 10), fg = "#d3d3d3", bg = "#014039")
        page_name.grid(row = 0, column = 0, sticky = "nsw", padx = 20)

        self.rightArrow = tk.PhotoImage(file = "Assets/User_Interface/right_arrow.png")
        typeP = tk.Label(self, text = problem[2].replace("_", " "), font = ("Montserrat", 16), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
        typeP.grid(row = 1, column = 0, padx = 20, pady = (12,5), sticky = "w")
        reporterL = tk.Label(self, text = "Por " + problem[3].replace("_", " ") + " | " + proj_name.replace("_", " "), font = ("Montserrat", 12), foreground = "#a3a3a3", borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
        reporterL.grid(row = 2, column = 0, padx = 20, pady = (0,10), sticky = "nw")

        self.closeIMG = tk.PhotoImage(file = "Assets/User_Interface/close.png")
        closeX = tk.Button(self, image = self.closeIMG, bd = 0, background = dark_grey, activebackground  = dark_grey, command = lambda: controller.show_frame(last))
        closeX.grid(row = 1, column = 1, sticky = "e", pady = 20, padx = 17)

        #Local que mostrara o problema
        def _on_mousewheel(event):
          self.canvasP.yview_scroll(int(-1*(event.delta/120)), "units")

        projectsF = tk.Frame(self, bg = black, bd = 0)
        projectsF.grid(row = 3, column = 0, sticky = "nsew", padx = 17, pady = (5,20), columnspan = 4)
        self.rowconfigure(3, weight = 1)
        self.canvasP = tk.Canvas(projectsF, bg = black, bd = 0, highlightthickness = 0)
        self.canvasP.pack(side=tk.LEFT, anchor = tk.N, fill = tk.BOTH, expand = tk.TRUE)
        problemCF = tk.Frame(self.canvasP, bg = black, borderwidth = 0, highlightthickness = 0)
        self.canvasP.create_window((0,0), window = problemCF, anchor = "nw")
        self.canvasP.configure(background = black)
        self.canvasP.bind_all("<MouseWheel>", _on_mousewheel)

        def defAberto(statusB, cursorSP):
            statusB.config(text = "Aberto", bg = ativo, activebackground  = ativo)
            cursorSP.execute("""UPDATE Problems SET status = "Aberto" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return

        def defEA(statusB, cursorSP):
            statusB.config(text = "Em andamento", bg = ativo, activebackground  = ativo)
            cursorSP.execute("""UPDATE Problems SET status = "Em andamento" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return
        
        def defPT(statusB, cursorSP):
            statusB.config(text = "Para ser testado", bg = planejamento, activebackground  = planejamento)
            cursorSP.execute("""UPDATE Problems SET status = "Para ser testado" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return
        
        def defFechado(statusB, cursorSP):
            statusB.config(text = "Fechado", bg = cancelado, activebackground  = cancelado)
            cursorSP.execute("""UPDATE Problems SET status = "Fechado" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return

        def invokeStatusS(invokeN, status):
            if status == "Aberto":
                statusB.menu.invoke(0)
            elif status == "Em andamento":
                statusB.menu.invoke(1)
            elif status == "Para ser testado":
                statusB.menu.invoke(2)
            elif status == "Fechado":
                statusB.menu.invoke(3)

        #Cursor usado para modificar status e prioridade
        cursorSP = db.cursor()

        #Alocando todas as informações do problema
        statusP = tk.Label(problemCF, text = "STATUS", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        statusP.grid(row = 0, column = 0, padx = 18, pady = (10,5), sticky = "nw")

        statusS = tk.StringVar()
        statusS.set(problem[4])
        statusB = tk.Menubutton(problemCF, text = "Ativo", font = ("Montserrat", 12), foreground = white82, borderwidth = 0, background = ativo, activebackground  = ativo,
                                activeforeground = white82)
        statusB.grid(row = 1, column = 0, padx = 20, pady = (8,5), sticky = "w")
        statusB.menu = tk.Menu(statusB, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        statusB["menu"] = statusB.menu
        statusB.menu.add_radiobutton(label = "Aberto", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defAberto(statusB, cursorSP))
        statusB.menu.add_radiobutton(label = "Em andamento", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defEA(statusB, cursorSP))
        statusB.menu.add_radiobutton(label = "Para ser testado", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defPT(statusB, cursorSP))
        statusB.menu.add_radiobutton(label = "Fechado", font = ("Montserrat", 9), variable = statusS, selectcolor = teal_Green, command = lambda: defFechado(statusB, cursorSP))
        invokeStatusS(statusB, problem[4])

        discriptionL = tk.Label(problemCF, text = "DESCRIÇÃO", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        discriptionL.grid(row = 2, column = 0, padx = 18, pady = 10, sticky = "nw")
        descricaoE = tk.Text(problemCF, undo=True, bg = black, fg = white82, bd = 0, width = 50, height = 10)
        descricaoE.config( font = ("Montserrat", 12) )
        descricaoE.insert(tk.END, problem[6])
        descricaoE.grid(row = 3, column = 0, sticky = "new", padx = 20, pady = 10)

        #Prioridade do problema
        def defNA(statusB):
            statusB.config(text = "Não-urgente", bg = ativo, activebackground  = ativo)
            cursorSP.execute("""UPDATE Problems SET priority = "Não-urgente" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return

        def defG(statusB):
            statusB.config(text = "Grave", bg = planejamento, activebackground  = planejamento)
            cursorSP.execute("""UPDATE Problems SET priority = "Grave" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return
        
        def defC(statusB):
            statusB.config(text = "Crítico", bg = cancelado, activebackground  = cancelado)
            cursorSP.execute("""UPDATE Problems SET priority = "Crítico" WHERE problem_id = %s """, (prob_id, ))
            db.commit()
            return


        def invokeStatusP(prioridadeB, status):
            if status == "Não-urgente":
                prioridadeB.menu.invoke(0)
                return
            elif status == "Grave":
                prioridadeB.menu.invoke(1)
                return
            prioridadeB.menu.invoke(2)

        prioridadeS = tk.StringVar()
        prioridadeS.set(problem[5])
        priorityL = tk.Label(problemCF, text = "PRIORIDADE", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        priorityL.grid(row = 4, column = 0, padx = 18, pady = 10, sticky = "nw")
        prioridadeB = tk.Menubutton(problemCF, text = "Aberto", font = ("Montserrat", 14), foreground = white82, borderwidth = 0, background = ativo, activebackground  = ativo,
                                activeforeground = white82)
        prioridadeB.grid(row = 5, column = 0, padx = 20, pady = (8,5), sticky = "w")
        prioridadeB.menu = tk.Menu(prioridadeB, tearoff=0,  foreground = white82, bg = black, bd = 0, activebackground = black)
        prioridadeB["menu"] = prioridadeB.menu
        prioridadeB.menu.add_radiobutton(label = "Não-urgente", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defNA(prioridadeB))
        prioridadeB.menu.add_radiobutton(label = "Grave", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defG(prioridadeB))
        prioridadeB.menu.add_radiobutton(label = "Crítico", font = ("Montserrat", 9), variable = prioridadeS, selectcolor = teal_Green, command = lambda: defC(prioridadeB))
        invokeStatusP(prioridadeB, problem[5])

        commentL = tk.Label(problemCF, text = "COMENTÁRIOS", font = ("Montserrat", 12), foreground = "#777777", borderwidth = 0, background = black, activebackground  = black,
                                activeforeground = "#777777" )
        commentL.grid(row = 6, column = 0, padx = 18, pady = 10, sticky = "nw")

        cursorC = db.cursor(buffered=True)
        cursorC.execute("SELECT * from Comments WHERE problem_id = %s ORDER BY date ASC", (prob_id, ))
        comments = cursorC.fetchall()
        cursorC.close()

        commentsF = tk.Frame(problemCF, bg = black)
        commentsF.grid(row = 7, column = 0, padx = 18, pady = 10, sticky = "nsew")

        self.user_img = tk.PhotoImage(file = "Assets/User_Interface/profile_user.png")

        i = 1
        #Adicionando os comentários no frame
        for comment in comments:
            c_frame = tk.Frame(commentsF, bg = dark_grey, height = 20, bd = 2)
            c_frame.grid(row = i, column = 0, sticky = "nsew", pady = 5)

            cursorU = db.cursor()
            cursorU.execute("SELECT * from Users WHERE user_id = %s", (comment[3], ))
            user = cursorU.fetchone()
            cursorU.close()

            c_userIMG = tk.Label(c_frame, image = self.user_img, bd = 0, background = dark_grey, activebackground  = white82)
            c_userIMG.grid(row = 0, column = 0, sticky = "nw", padx = (10,0), pady = 12)

            c_Uname = tk.Label(c_frame, text = user[2], font = ("Montserrat SemiBold", 16), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = black,
                                activeforeground = white82)
            c_Uname.grid(row = 0, column = 0, sticky = "nw", padx = 42, pady = 5)

            c_commentF = tk.Frame(c_frame, width = 50, height = 20)
            c_commentF.grid(row = 1, column = 0, sticky = "new", padx = 42, pady = 10)
            c_commentF.grid_propagate(False)
            c_commentE = tk.Text(c_commentF, undo=True, bg = dark_grey, fg = white82, bd = 0, width = 50, height = 5)
            c_commentE.config( font = ("Montserrat", 12) )
            c_commentE.insert(tk.END, comment[1])
            c_commentE.config(state = tk.DISABLED)
            c_commentE.pack()

            dt = datetime.datetime.strptime(str(comment[4]), '%Y-%m-%d').strftime('%m/%d/%Y')
            c_date = tk.Label(c_frame, text = dt, font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82, width = 8)
            c_date.grid(row = 2, column = 0, sticky = "nwse", padx = 20, pady = 5)

            i += 1

        NCommentF = tk.Frame(commentsF, bg = dark_grey, height = 20, bd = 2)
        NCommentF.grid(row = i, column = 0, sticky = "nsew", pady = 5)

        userIMG = tk.Label(NCommentF, image = self.user_img, bd = 0, background = dark_grey)
        userIMG.grid(row = 0, column = 0, sticky = "nw", padx = 10, pady = 5, ipady = 5)

        new_commentF = tk.Frame(NCommentF, width = 50, height = 20)
        new_commentF.grid(row = 0, column = 0, sticky = "nw", padx = (50,10), pady = 10)
        new_commentF.grid_propagate(False)
        new_commentE = scrolledtext.ScrolledText(new_commentF, undo=True, bg = "#777777", fg = "#d3d3d3", bd = 0, width = 50, height = 5)
        new_commentE['font'] = ("Montserrat", '12')
        new_commentE.pack()
        
        def addComment(commentsF, NCommentF, new_commentE, new_commentF, add_commentBtn, userIMG, i):
            Ncomment = new_commentE.get("1.0", tk.END)

            #A data atual
            today = datetime.datetime.today()
            d1 = today.strftime("%d/%m/%Y")
            
            #Adicionando o comentário na db
            add_comment = "INSERT INTO Comments (comment, problem_id, user_id, date) VALUES (%s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'))"
            comment_data = (str(Ncomment), str(prob_id), str(user_id), d1)
            cursorC = db.cursor()
            cursorC.execute(add_comment, comment_data)
            db.commit()
            cursorC.close()

            #Alocando o novo comentário
            cursorU = db.cursor()
            cursorU.execute("SELECT * from Users WHERE user_id = %s", (user_id, ))
            user = cursorU.fetchone()
            cursorU.close()


            c_frame = tk.Frame(commentsF, bg = dark_grey, height = 20, bd = 2)
            c_frame.grid(row = i, column = 0, sticky = "nsew", pady = 5)

            c_userIMG = tk.Label(c_frame, image = self.user_img, bd = 0, background = dark_grey, activebackground  = white82)
            c_userIMG.grid(row = 0, column = 0, sticky = "nw", padx = (10,0), pady = 12)

            c_Uname = tk.Label(c_frame, text = user[2], font = ("Montserrat SemiBold", 14), foreground = white82, borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82)
            c_Uname.grid(row = 0, column = 0, sticky = "nw", padx = 42, pady = 5)

            c_commentF = tk.Frame(c_frame, width = 50, height = 20)
            c_commentF.grid(row = 1, column = 0, sticky = "new", padx = 42, pady = 10)
            c_commentF.grid_propagate(False)
            c_commentE = tk.Text(c_commentF, undo=True, bg = dark_grey, fg = white82, bd = 0, width = 50, height = 5)
            c_commentE.config( font = ("Montserrat", 12) )
            c_commentE.insert(tk.END, Ncomment)
            c_commentE.config(state = tk.DISABLED)
            c_commentE.pack()

            c_date = tk.Label(c_frame, text = str(d1), font = ("Montserrat", 10), foreground = "#bfbfbf", borderwidth = 0, background = dark_grey, activebackground  = dark_grey,
                                activeforeground = white82, width = 8)
            c_date.grid(row = 2, column = 0, sticky = "nwse", padx = 20, pady = 5)

            i += 1

            NCommentF.grid(row = i, column = 0, sticky = "nsew", pady = 5)
            new_commentE.delete('1.0', tk.END)

        #Botão de adicionar comentário
        self.IMGAddCommentBtn = tk.PhotoImage(file = "Assets/User_Interface/addComment.png")
        add_commentBtn = tk.Button(NCommentF, image = self.IMGAddCommentBtn, bd = 0, background = dark_grey,
                                    activebackground  = dark_grey, command = lambda: addComment(commentsF, NCommentF, new_commentE, new_commentF, add_commentBtn, userIMG, i))
        add_commentBtn.grid(row = 1, column = 0, sticky = "ne", padx = 5, pady = 10)


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