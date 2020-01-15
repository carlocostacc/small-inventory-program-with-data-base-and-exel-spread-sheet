import tkinter as tk
from tkinter import ttk
from operationclasses import*
import sqlite3
import datetime
import time
from exellogic import post_to_exel
from settings import *
import test
element_string_add = ""
element_string = ""
LargeFont = ('Verdana', 12)

conn = sqlite3.connect('contrat.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS contrats(EOI TEXT, date TEXT, element TEXT, bain TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS Used_contrats(EOI TEXT, date TEXT, element TEXT, bain TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS inventaire(item TEXT, date TEXT)')

test.createFolder(r"C:\Users\entrepot\Desktop\codebarre")
conn.commit()

def element_counter(listofelement):
    duplicateslist = []
    finallist = []
    for i in listofelement:
        count = listofelement.count(i)
        if count > 1:
            count = str(count)
            duplicateslist.append(count + " " + "x" + " " + i)
        else :
            finallist.append(i)
    for a in duplicateslist:
        if a not in finallist:
            finallist.append(a)
    listofelement = finallist
    print (listofelement)
    return listofelement

def popupmsg(msg):

    popup = tk.Tk()
    def leavemini():

        popup.destroy()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=Normalfont)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="okay", command=leavemini)
    B1.pack()
    popup.mainloop()


def delete_contrat():
    try:
        num_decontrat = input()
        c.execute("DELETE FROM contrats WHERE EOI = " + num_decontrat)
        contrat = Contrat(num_decontrat)
        contrat.element.clear()
        contrat.bain.clear()
        print("le contrat est effacé")
    except sqlite3.OperationalError:
        popupmsg("le contrat que vous tenter de supprimer n'existe pas, veullier vous referer au document exel")
        print("le contrat que vous tenter de supprimer n'existe pas, veullier vous referer au document exel")
    conn.commit()


def data_entry_for_element(EOI, element,bain):
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
    c.execute("INSERT INTO contrats (EOI, date, element, bain)VALUES(?, ?, ?, ?)", (EOI, date, element, bain))
    conn.commit()



def data_entry_for_retour(EOI, element):
    bain = "0"
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
    c.execute("INSERT INTO Used_contrats (EOI, date, element, bain)VALUES(?, ?, ?, ?)", (EOI, date, element, bain))
    conn.commit()


def read_all_db():
    c.execute("SELECT * FROM contrats")
    data = c.fetchall()


def read_from_db(num_EOI):
    c.execute("SELECT * FROM contrats WHERE EOI =" + num_EOI)
    if c.fetchone() is None:
        popupmsg("le contrat chercher n'existe pas dans la base de donnee")
        print("le contrat chercher n'existe pas dans la base de donnee")


def update(num_EOI, element_update):
    c.execute("SELECT * FROM contrats WHERE EOI =" + num_EOI)
    c.fetchone()
    if c.fetchone() is None :
        popupmsg("le contrat chercher n'existe pas dans la base de donnee")
        print("le contrat chercher n'existe pas dans la base de donnee")

        pass

    c.execute("UPDATE contrats SET element = " + element_update + "WHERE EOI = " + num_EOI)
    for row in c.fetchall():
        print(row)
    conn.commit()


class Display (tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Inventaire")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="save", command=lambda: post_to_exel)
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="file", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        exchangeChoice = tk.Menu(menubar, tearoff=0)

        exchangeChoice.add_command(label="ajout",
                                   command=lambda: popupmsg("not supported"))
        exchangeChoice.add_separator()
        exchangeChoice.add_command(label="ajout d'un element",
                                   command=lambda: popupmsg("not supported"))
        exchangeChoice.add_separator()

        exchangeChoice.add_command(label="ajout d'un bain",
                                   command=lambda: popupmsg("not supported"))
        exchangeChoice.add_separator()

        exchangeChoice.add_command(label="Retrait",
                                   command=lambda: popupmsg("not supported"))

        menubar.add_cascade(label="contrats", menu=exchangeChoice)


        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame (self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="nouvelle commande", font=LargeFont)
        label.pack(pady=10, padx=10)
        button = ttk.Button(self, text="nouvelle commande", command=Ajout_de_commande)
        button.pack()
        button2 = ttk.Button(self, text="faire un code barre", command=code_bar)
        button2.pack()
        button1 = ttk.Button(self, text="Ajout d'un element dans une commande", command=lambda: controller.show_frame(PageOne))
        button1.pack()



def Ajout_a_linventaire():
    while True :
        item = input()
        if item != "0":
            date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
            c.execute("INSERT INTO inventaire (item, date)VALUES(?, ?)", (item, date))
            conn.commit()
        else:
            return False


def retrait_a_linventaire():
    try:
        contrat = input()
        c.execute("DELETE FROM inventaire WHERE EOI = " + contrat)
    except sqlite3.OperationalError :
        popupmsg("le contrat que vous tenter de supprimer n'existe pas, veullier vous referer au document exel")
        print("le contrat que vous tenter de supprimer n'existe pas, veullier vous referer au document exel")

def code_bar():
    
    while True:
        codebar = input()
        if codebar != '0':
            try:
                test.print_bar_codes(codebar)
            except FileExistsError:
                print('le code barre que vous essayez de créer existe déjà')
        else:
            break
def Ajout_de_commande():
    global element_string

    num_decontrat = (input())
    print(num_decontrat)
    try:
        test.print_bar_codes(num_decontrat)
    except FileExistsError:
                print('le code barre que vous essayez de créer existe déjà')

    try:
        c.execute("DELETE FROM Used_contrats WERE EOI = " + num_decontrat)
        conn.commit()
        Contrat_retour(num_decontrat).element.clear()
        Contrat_retour(num_decontrat).bain.clear()
    except sqlite3.OperationalError :
        print("")

    contrat = Contrat(num_decontrat)
    Ajout_de_bain(num_decontrat)


    while True:

        produit = input()

        print(produit)

        if produit != "0":

            contrat.add_element(produit)

        else:

            contrat.element = element_counter(contrat.element)

            for i in contrat.element:
                element_string += i + ", "

            data_entry_for_element(num_decontrat, element_string,element_string_add )
            print(element_string)
            post_to_exel

            break

        
def Ajout_a_un_retour():
    global element_string_add
    element_string_add = ""
    num_de_contrat = input()
    contrat = Contrat_retour(num_de_contrat)
    try:
        c.execute("SELECT * FROM Used_contrats WHERE EOI =" + num_de_contrat)
    except sqlite3.OperationalError:
        popupmsg("Vous avez choisi un EOI inexistant ou qui n'est pas encore complété")
    if c.fetchone()is None:
        popupmsg("le contrat chercher n'existe pas dans la base de donnee")
        print("le contrat chercher n'existe pas dans la base de donnee")
        pass
    else:

        print("passed")

        while True:

            produit = input()

            if produit != "0":

                contrat.add_element(produit)

            else:
                contrat.element = element_counter(contrat.element)
                for i in contrat.element:
                    element_string_add += i + " "
                c.execute("SELECT * FROM Used_contrats WHERE EOI =" + num_de_contrat)
                for row in c.fetchall():
                    original = (row[2])
                final_string = original + "," + element_string_add
                print(final_string)
                c.execute("UPDATE Used_contrats SET element = ? WHERE EOI = ?", (final_string, num_de_contrat))
                conn.commit()

                break


def Ajout_element_commande():
    global element_string_add
    num_de_contrat = (input())
    print(num_de_contrat)
    contrat = Contrat(num_de_contrat)
    try:
        c.execute("SELECT * FROM contrats WHERE EOI =" + num_de_contrat)
    except sqlite3.OperationalError:
        popupmsg("Vous avez choisi un EOI inexistant")

    if c.fetchone()is None:
        popupmsg("le contrat chercher n'existe pas dans la base de donnee")
        print("le contrat chercher n'existe pas dans la base de donnee")
        pass

    else:

        print("passed")

        while True:

            produit = input()

            if produit != "0":

                contrat.add_element(produit)

            else:
                contrat.element = element_counter(contrat.element)
                for i in contrat.element:
                    element_string_add += i + " "
                c.execute("UPDATE contrats SET element = ? WHERE EOI = ?", (element_string_add, num_de_contrat))
                for row in c.fetchall():
                    print(row)
                conn.commit()

                break


def utiliser_dans_commande():
    global element_string
    num_decontrat = "8"
    while num_decontrat != "0":
        num_decontrat = input()
        if num_decontrat != "0":
            x = 0
            print(num_decontrat)

            contrat = Contrat_retour(num_decontrat)

        while x != 1:

            produit = input()

            print(produit)

            if produit != num_decontrat:

                contrat.add_element(produit)

            else:

                contrat.element = element_counter(contrat.element)

                for i in contrat.element:
                    element_string += i + ", "

                data_entry_for_retour(num_decontrat, element_string)
                print(element_string)
                try:
                    c.execute("DELETE FROM contrats WHERE EOI = " + num_decontrat)
                    contrat.element.clear()
                    contrat.bain.clear()
                except sqlite3.OperationalError:
                    print("le contrat que vous tenter de supprimer n'existe pas, veullier vous referer au document exel")
                x = 1



def Ajout_de_bain(num_de_contrat):
    global element_string_add
    
    print(num_de_contrat)
    contrat = Contrat(num_de_contrat)
    


    while True:

        produit = input()

        if produit != "0":

            contrat.add_bain(produit)
            print(contrat.bain)

                

        else:
            for i in contrat.bain:
                element_string_add += i + ", "
            print(element_string_add)
            return element_string_add

def Ajout_de_bain_manuelle():
    global element_string_add
    num_de_contrat = input()
    print(num_de_contrat)
    contrat = Contrat(num_de_contrat)
    try:
        c.execute("SELECT * FROM contrats WHERE EOI =" + num_de_contrat)
    except sqlite3.OperationalError:
        popupmsg("Vous avez crée un nouveau contrat" + num_de_contrat)


    while True:

        produit = input()

        if produit != "0":

            contrat.add_bain(produit)
            print(contrat.bain)

                

        else:
            for i in contrat.bain:
                element_string_add += i + ", "
            print(element_string_add)
            c.execute("UPDATE contrats SET bain = ? WHERE EOI = ?", element_string_add, num_de_contrat)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ajout d'un element", font=LargeFont)
        label.pack(pady=10, padx=10)

        button3 = ttk.Button(self, text="Retirer une commande", command=lambda: delete_contrat())
        button3.pack()

        button4 = ttk.Button(self, text="Retour de commande", command=lambda: utiliser_dans_commande())
        button4.pack()

        button = ttk.Button(self, text="Ajout d'un element dans une commande", command=Ajout_element_commande)
        button.pack()

        button5 = ttk.Button(self, text="Modification d'un retour", command= Ajout_a_un_retour)
        button5.pack()

        button2 = ttk.Button(self, text="Ajout d'un bain a un Contrat", command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ajout de bain", font=LargeFont)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Ajout d'un bain ou modification",
                             command=lambda : Ajout_de_bain_manuelle())
        button1.pack()

        button3 = ttk.Button(self, text="Retour Ajout d'un element dans une commande",
                             command=lambda: controller.show_frame(PageOne))
        button3.pack()

        button4 = ttk.Button(self, text="Inventaire",
                             command=lambda: controller.show_frame(PageThree))
        button4.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Iventaire", font=LargeFont)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Ajout a l'inventaire",
                             command=lambda: Ajout_a_linventaire())
        button1.pack()

        button2 = ttk.Button(self, text="Retrait a l'inventaire", command=lambda: retrait_a_linventaire())
        button2.pack()

        button3 = ttk.Button(self, text="Retour a Ajouter un contrat",
                             command=lambda: controller.show_frame(StartPage))
        button3.pack()


app = Display()
app.mainloop()

