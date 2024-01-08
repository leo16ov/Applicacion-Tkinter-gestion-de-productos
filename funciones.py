from tkinter import *
from tkinter import ttk
import mysql.connector, re

fuente_grande= ('Heveltica', 14)
fuente_mediana= ('Heveltica', 12)
fuente_pequeña= ('Heveltica', 9)

#Funcion para abrir la conexion a la base de datos:
def connectionDB():
    mi_db = mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'pyandjs17',
                                    database = 'gestion_de_ventas')
    db_cursor = mi_db.cursor()
    return mi_db, db_cursor #Devuelve la conexion y el cursor de la bdd.

#Funcion que para crear una ventana. (titulo de la ventana, tamaño de la ventana)
def createWindow(title, geometry):
    window = Toplevel()
    window.title(title)
    window.geometry(geometry)
    window.resizable(False, False)
    window.configure(bg= 'white')
    return window

def createCombo(window, width, valueInit, query):
    Combobox = ttk.Combobox(window, width= width)
    
    mi_db, db_cursor = connectionDB()
    db_cursor.execute(query)

    values = [valueInit]
    for tuple in db_cursor:
        for datos in tuple:
            values.append(datos)
    
    db_cursor.close()
    mi_db.close()
    Combobox['values'] = values
    Combobox.current(0)
    return Combobox

#Funcion para crear un tabla.(nombre de ventana en la que aparecera, numero de columnas, nombre de columnas, tamaños de columnas, consulta.)
def createTable(window, numColumns, namesColumns, sizeColumns, query):
    tabla = ttk.Treeview(window, columns=tuple(range(numColumns)), show='headings')
    for i in range(numColumns):
        tabla.heading(i, text=namesColumns[i], anchor="center")
        tabla.column(i, width=sizeColumns[i], anchor="center")

    mi_db, db_cursor = connectionDB()
    db_cursor.execute(query)
    
    for datos in db_cursor:
        tabla.insert('', END, values=datos)
    
    db_cursor.close()
    mi_db.close()
    return tabla

def createSimpleCombo(window, width, values):
    Combobox = ttk.Combobox(window, width= width)
    Combobox['values'] = values
    Combobox.current(0)
    return Combobox

def updateCombo(combo, valueInit,query):
    values = [valueInit]
    mi_db, db_cursor = connectionDB()
    db_cursor.execute(query)
    for i in db_cursor:
        values.append(i)
    combo['values'] = values
    combo.current(0)
    db_cursor.close()
    mi_db.close()

def eliminar_widget(widget):
    if widget.winfo_exists():
        widget.destroy()

def contiene_solo_numeros(cadena):
    patron = r'^\d+$'

    if re.match(patron, cadena):
        return True
    else:
        return False

def addCampus(window, text, width, font):
    label = Label(window, text= text, font= font, bg= 'white')
    entry = Entry(window, width= width)
    
    return label, entry

def deleteEntrys6(campo1, campo2, campo3, campo4, campo5, campo6):
    campo1.delete(0, END)
    campo2.delete(0, END)
    campo3.delete(0, END)
    campo4.delete(0, END)
    campo5.delete(0, END)
    campo6.delete(0, END)
    
def ocultar_widget(widget, ventanaAOcultar, ventanaAMostrar):
    widget.pack_forget()
    ventanaAOcultar.withdraw()
    ventanaAMostrar()

def mostrar_widget(widget, tiempo, ventanaAOcultar, ventanaAMostrar):
    widget.pack(pady= 200)
    widget.after(tiempo, lambda: ocultar_widget(widget, ventanaAOcultar, ventanaAMostrar))

def es_decimal(cadena):
    try:
        decimal = float(cadena)
        if cadena.replace('.', '', 1).isdigit():
            return True
        else:
            return False
    except ValueError:
        return False
    
def texto(window, text):
    texto_extenso = Text(window, wrap= WORD, width=40, height=10)
    texto_largo = text
    
    texto_extenso.insert(END, texto_largo)

    return texto_extenso