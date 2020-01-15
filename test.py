import barcode
from barcode.writer import ImageWriter
import os
def print_bar_codes(contrat):
    EAN = barcode.get_barcode_class("code128")
    ean = EAN(u""+contrat + "", writer = ImageWriter())
    print(ean)
    fullname = ean.save(contrat)
    os.rename("C:/Users/entrepot/Desktop/inventaire work/" + fullname, "C:/Users/entrepot/Desktop/codebarre/" + fullname)
    try : 
        os.remove("C:/Users/entrepot/Desktop/inventaire work/" + fullname)
    except FileNotFoundError:
        print(" ")
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createFolder("C:/Users/entrepot/Desktop/codebarre")

