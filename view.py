import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox

import branch_and_bound
import glouton
import heuristique
import parsing
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from random import randint

colors = []


def hexa_from_int(integer):
    if not colors:
        for i in range(len(bases)):
            colors.append('#%06X' % randint(0x777777, 0xFFFFFF))
    return colors[integer]


def get_path_file(var: tk.StringVar):
    e1.config(state=tk.NORMAL)
    e2.config(state=tk.NORMAL)
    old = var.get()
    try:
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        if filename == ():
            return

        var.set(os.path.relpath(filename))
        if path_list_bases.get() != "" and path_folder_bases.get() != "":
            all_bases.clear()
            all_bases.extend(parsing.all_bases(path_list_bases.get(), path_folder_bases.get()))
            display_cost()

        if path_list_entreprises.get() != "":
            entreprises.clear()
            entreprises.extend(parsing.liste(path_list_entreprises.get()))
            e2.delete("1.0", "end")
            e2.insert("0.1", "\n".join(entreprises))

        if path_list_bases.get() != "" and path_folder_bases.get() == "":
            bases.clear()
            bases.extend(parsing.liste(path_list_bases.get()))
            e1.delete("1.0", "end")
            e1.insert("0.1", "\n".join(bases))

    except Exception as e:
        print(e)
        var.set(old)
        messagebox.showerror("Fichier incorrecte", "Vous avez saisie un fichier qui est dans un format incomptatible")

    finally:

        e1.config(state=tk.DISABLED)
        e2.config(state=tk.DISABLED)


def get_path_folder(var: tk.StringVar):
    e1.config(state=tk.NORMAL)
    e2.config(state=tk.NORMAL)
    old = var.get()
    try:
        filename = filedialog.askdirectory(initialdir=".",
                                           title="Select a Directory")
        if filename == ():
            return

        var.set(os.path.relpath(filename))
        print(path_list_bases.get() != "" and path_folder_bases.get() != "")
        if path_list_bases.get() != "" and path_folder_bases.get() != "":
            all_bases.clear()
            all_bases.extend(parsing.all_bases(path_list_bases.get(), path_folder_bases.get()))
            display_cost()
    except Exception as e:
        print(e)
        var.set(old)
        messagebox.showerror("Dossier incorrecte", "Votre dossier contient des fichiers d'un format incompatible")
    finally:
        e1.config(state=tk.DISABLED)
        e2.config(state=tk.DISABLED)


def display_cost():
    all_bases_map = list(map(lambda x: x.name + " " + str(x.cost), all_bases))
    e1.delete("1.0", "end")
    e1.insert("0.1", "\n".join(all_bases_map))


def method():
    start = 0
    end = 0
    i = 0
    bl, c, i = None, None, None
    if m.get() == "glouton":
        start = time.time()
        bl, c, i = glouton.glouton(all_bases, entreprises, getattr(heuristique, h.get()))
        end = time.time() - start

    elif m.get() == "branch_and_bound":
        start = time.time()
        bl, c, i = branch_and_bound.branch_and_bound(all_bases, entreprises, getattr(heuristique, h.get()))
        end = time.time() - start

    if bl is None:
        messagebox.showinfo("Pas de solution", "Vérifier que vos fichiers sont correctes")
        return

    resultat_bases.clear()
    resultat_bases.extend(bl)
    cout_resultat.set(f"Coût: {c}")

    perf.set(f"Temp={end},iterations={i}")

    highlighter()


def highlighter():
    for tag in e1.tag_names():
        e1.tag_delete(tag)
    for tag in e2.tag_names():
        e2.tag_delete(tag)
    for base in resultat_bases:
        line = bases.index(base.name)
        e1.tag_add("select_bases" + str(line), str(line + 1) + ".0", str(line + 1) + "." + str(len(base.name)))
        e1.tag_config("select_bases" + str(line), background=hexa_from_int(line))

        for index, entreprise in enumerate(entreprises):

            if entreprise in base.liste:
                e2.tag_add("select_bases" + str(line), str(index + 1) + ".0",
                           str(index + 1) + "." + str(len(entreprise)))

        e2.tag_config("select_bases" + str(line), background=hexa_from_int(line))

gui = tk.Tk()
gui.title("Optimisation Combinatoire")
gui.geometry("{}x{}".format(gui.winfo_screenwidth(), gui.winfo_screenheight()))
path_list_bases = tk.StringVar()
path_list_entreprises = tk.StringVar()
path_folder_bases = tk.StringVar()
cout_resultat = tk.StringVar()
perf = tk.StringVar()

resultat_bases = []

path_list_bases.set("Data/Scénarios/Liste Bases/Liste Bases1.txt")
path_list_entreprises.set("Data/Scénarios/Liste Entreprises/Liste Ent1.txt")
path_folder_bases.set("Data/Bases")

all_bases = parsing.all_bases(path_list_bases.get(), path_folder_bases.get())
entreprises = parsing.liste(path_list_entreprises.get())
bases = parsing.liste(path_list_bases.get())

b1 = tk.Button(gui, text="Chemin du fichier de la listes des bases", command=lambda: get_path_file(path_list_bases))
b2 = tk.Button(gui, text="Chemin du fichier de la listes des entreprises",
               command=lambda: get_path_file(path_list_entreprises))
b3 = tk.Button(gui, text="Chemin du dossier des bases", command=lambda: get_path_folder(path_folder_bases))

l1 = tk.Label(gui, textvariable=path_list_bases)
l2 = tk.Label(gui, textvariable=path_list_entreprises)
l3 = tk.Label(gui, textvariable=path_folder_bases)

e1 = tkscrolled.ScrolledText(gui, height=1)
e2 = tkscrolled.ScrolledText(gui, height=1)

s = ttk.Separator(orient="horizontal")

ht = tk.Label(text="Choisir une heuristique")
h = ttk.Combobox(gui, values=dir(heuristique)[10:-1])
h.current(0)

mt = tk.Label(text="Choisir une methode")
m = ttk.Combobox(gui, values=["glouton", "branch_and_bound"])
m.current(0)

v = tk.Button(text="Calculer", command=method)

s1 = ttk.Separator(orient="horizontal")

r = tk.Label(textvariable=cout_resultat, font=("Arial", 75))

p = tk.Label(textvariable=perf, font=("Arial", 25), fg="#B7950B")

l1.grid(row=1, column=0)
l2.grid(row=1, column=1)
l3.grid(row=1, column=2)

b1.grid(row=0, column=0, pady=15)
b2.grid(row=0, column=1, pady=15)
b3.grid(row=0, column=2, pady=15)

e1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
e1.delete("1.0", "end")
e1.insert("0.1", "\n".join(bases))

e2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
e2.delete("1.0", "end")
e2.insert("0.1", "\n".join(entreprises))
display_cost()
e1.config(state=tk.DISABLED)
e2.config(state=tk.DISABLED)

v.grid(row=4, column=2, rowspan=2)

ht.grid(row=4, column=0, )
h.grid(row=5, column=0, ipadx=20, ipady=5)

mt.grid(row=4, column=1, )
m.grid(row=5, column=1, ipadx=20, ipady=5)

s1.grid(row=6, column=0, columnspan=3, sticky="ew")

r.grid(row=7, column=0, columnspan=3)
p.grid(row=8, column=0, columnspan=3)

gui.columnconfigure(0, weight=1)
gui.columnconfigure(1, weight=1)
gui.columnconfigure(2, weight=1)
gui.rowconfigure(2, weight=1)

gui.mainloop()
