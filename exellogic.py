import xlwings as xw
import sqlite3
import pandas as pd
import barcode
import openpyxl as openpx

conn = sqlite3.connect('contrat.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Used_contrats(EOI TEXT, date TEXT, element TEXT, bain TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS inventaire(item TEXT, date TEXT)')

def post_to_exel():
    print(xw.Book("type d'items.xlsm").sheets)
    try:
        wb.sheets.add("Contrats")
    except ValueError:
        c.execute("SELECT * FROM contrats")
        data = c.fetchall()
        sht = xw.sheets["Contrats"]
        df = pd.DataFrame(data)
        sht.range("A1").value = df
        sht.range("B1").value = "EOI"
        sht.range("C1").value = "Date"
        sht.range("D1").value = "Element"
        sht.range("E1").value = "Bain"

        c.execute("SELECT * FROM Used_contrats")
        data = c.fetchall()
        sht = xw.sheets["Contrats"]
        df = pd.DataFrame(data)
        sht.range("F1").value = df
        sht.range("G1").value = "EOI"
        sht.range("H1").value = "Date"
        sht.range("I1").value = "Element"
        sht.range("J1").value = "Bain"
        sht.range("F1").value = "Supplies Used"

        c.execute("SELECT * FROM inventaire")
        data = c.fetchall()
        sht = xw.sheets["Ajout"]
        df = pd.DataFrame(data)
        sht.range("A1").value = df
        sht.range("B1").value = "Item"
        sht.range("C1").value = "Date"


try:
    wb = xw.Book("type d'items.xlsm")
    post_to_exel()

except FileNotFoundError as e:
    print(e)
    print("le ficher exel n'est plus associer au programme")


def Ajout_a_linventaire():
    wb = openpx.load_workbook(r"C:\Users\entrepot\Desktop\inventaire work\type d'items.xlsm")
    currentsheet = wb.active
    pass


Ajout_a_linventaire()
