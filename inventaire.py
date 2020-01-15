
from tkinter import *
from settings import *
from operationclasses import *

root = Tk()
root.geometry("400x300")

num_lines = sum(1 for line in open (myfile))
line_skip_counter = num_lines

class Window (Frame) :
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("Inventaire")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)

        self.master.config(menu=menu)
        file = Menu(menu)

        file.add_command(label="Exit", command=self.client_exit)

        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)


        button = Button(self, text="nouvelle commande", command=Ajout_de_commande)

        button2 = Button(self, text="Ajout de bain", command=Ajout_de_bain)

        button3 = Button(self, text = "Ajout a une commande", command = ajout_a_une_commande_existante)

        button3.place(x=120, y= 0)

        button2.place(x=0, y=50)

        button.place(x=0, y=0)


    def client_exit(self):
        exit()

def Ajout_de_commande():

    num_decontrat = input()

    contrat = Contrat(num_decontrat)


    while True:

        produit = input()

        if produit != "0":

            contrat.add_element(produit)

        else :

            with open("inventaire.txt", "a+") as f:

                f.writelines("\n")

                f.write("contrat : ") + f.write(contrat.EOI)

                for i in contrat.element:
                    f.writelines("\n")
                    f.writelines(i)


            contrat_element_bain.append([contrat.EOI, contrat.element])
            print(contrat_element_bain)
            break

def ajout_a_une_commande_existante ():

    commande = input()
    with open(myfile, "a") as f:

        line_search(commande)



def line_search(string) :

    with open(myfile, "r") as f:

        lines = f.readlines()

        for i, line in enumerate(lines):

            if line.startswith(string):

                return i + 1

        else :

            appendcontrat(string)

def appendcontrat(contrat) :

    with open(myfile, "a") as f:
        lines = f.readlines()
        for i, l in enumerate(lines):

            pass

    return 1 + i

    with open(myfile, "a") as f:

        line[i + 1] = "contrat : " + contrat



def Ajout_de_bain() :

    num_decontrat = input()

    contrat = Contrat(num_decontrat)

    while True:

        bain = input()

        if bain != "0":

            contrat.add_bain(bain)

        else:
    
            liste_bain.append(contrat.bain)

            with open(myfile, "a+") as f:

                line_search("contrat : " + num_decontrat)

                for i in contrat.bain:
                    f.writelines("\n")
                    f.writelines(i)

            print(contrat.EOI)
    
            print(contrat.bain)
    
            break


app = Window(root)

root.mainloop()


