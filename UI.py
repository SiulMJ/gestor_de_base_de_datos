import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector


#funcion para crear bases de datos y que salga un mensaje
def crear():
    cone = mysql.connector.connect(host="localhost", user="root", password="")
    cur = cone.cursor()
    text = texto_chido.get()
    try:
        cur.execute(f"CREATE DATABASE {text}")
        if text == 0:
            messagebox.showinfo(
            message="no creo la base de datos",
            title="crear"
        )
        else:
            messagebox.showinfo(
            message="se creo la base de datos",        
            title="crear"
            )
            refresh_listbox()
    except mysql.connector.Error as error:
        ventana3 = tk.Toplevel()
        ventana3.title("creacion de tablas")
        ventana3.config(width=300, height=200)
        label = tk.Label(ventana3, text=error)
        label.pack()
         
#fucion para borrar bases de datos y que salga un mensaje
def borrar():
    cone = mysql.connector.connect(host="localhost", user="root", password="")
    cur = cone.cursor()
    bases = lista.get(lista.curselection())
    print(bases)
    cur.execute("drop database {}".format(bases))
    if bases == 0:
        messagebox.showinfo(
        message="no se borro",
        title="borrar"
    )
    else:
        messagebox.showinfo(
        message="se borro la base de datos",        
        title="borrar"
         )
        refresh_listbox()

#funcion para que la lista muestre las bases de datos se auto actualize
def refresh_listbox():
    lista.delete(0, tk.END)#este comando resetea la lista cuando borras un elemento
    cone = mysql.connector.connect(host="localhost", user="root", password="")
    cur = cone.cursor()
    cur.execute("SHOW DATABASES")
    resultados = cur.fetchall()
    for resultado in resultados:
        lista.insert(tk.END, resultado[0])
        cone.commit()
        
def consulta():
    # Crear una ventana secundaria.
    ventana2 = tk.Toplevel()
    ventana2.title("tabla de consultas")
    ventana2.config(width=300, height=200)
    
    # Obtener el texto del cuadro de texto
    consulta = cuadrot.get("1.0","end")
    db = lista.get(lista.curselection())
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = db
    )
    try:

        cursor = conexion.cursor()
        cursor.execute(consulta)
        results = cursor.fetchall()
        conexion.commit()
        
        consultas = tk.Label(ventana2, text="su consulta es exitosa")
        consultas.pack()
        
        resultados_text = tk.Text(ventana2, height=30, width=50)

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Agregar los nombres de las columnas al widget Text
        resultados_text.insert(tk.END, ", ".join(columnas) + "\n")

        # Agregar los resultados de la consulta al widget Text
        for resultado in results:
            resultados_text.insert(tk.END, str(resultado) + "\n")

            # Mostrar el widget Text
        resultados_text.pack()
        refresh_listbox()
        refresh_table()

    except mysql.connector.Error as error:
        label = tk.Label(ventana2, text=error)
        label.pack()

def mostrar_tablas():
    global tablas
    ventana3 = tk.Toplevel()
    ventana3.title("tabla de consultas")
    ventana3.geometry("650x400")
    # Conectar a la base de datos
    mostra = lista.get(lista.curselection())
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = mostra
    )
    # Crear el cursor
    cursor = conexion.cursor()

    # Obtener los datos de las tablas
    cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_schema='{mostra}'")
    datos_tablas = cursor.fetchall()

    # Crear el Treeview y agregar las columnas
    tablas = ttk.Treeview(ventana3, columns=("table_name", "table_type"))
    tablas.heading("table_name", text="Nombre de la tabla")
    tablas.heading("table_type", text="Tipo de tabla")

    # Agregar las filas
    for fila in datos_tablas:
        tablas.insert("", "end", values=(fila[2], fila[3]))

    # Empaquetar el Treeview
    tablas.pack()

    boton_eliminar = tk.Button(ventana3, text="Eliminar tablas seleccionadas", command=eliminar_tablas)
    boton_eliminar.pack()

    # Función para modificar una tabla seleccionada

def refresh_table():
    bdx = lista.get(lista.curselection())
    lista.delete(0, tk.END)
    cone = mysql.connector.connect(host="localhost", user="root", password="", database=bdx)
    cur = cone.cursor()
    cur.execute(f"SHOW TABLES FROM {tablas}")
    resultados = cur.fetchall()
    for resultado in resultados:
        lista.insert(tk.END, resultado[0])

def eliminar_tablas():
    datosbase = lista.get(lista.curselection())
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database= datosbase
    )
    cursor = conexion.cursor()
    # Obtener las filas seleccionadas
    seleccion = tablas.selection()    # Eliminar las tablas de la base de datos
    if seleccion:
        for id in seleccion:
            tabla_seleccionada = tablas.item(id)['values'][0]
            cursor.execute(f"DROP TABLE {tabla_seleccionada}")
            # Eliminar la tabla del Treeview
            tablas.delete(id)
        # Confirmar los cambios en la base de datos
        conexion.commit()
    else:
        messagebox.showinfo("Mensaje", "Debes seleccionar al menos una tabla para eliminar")
    if seleccion <seleccion:
        messagebox.showinfo(
        message="se borro la Tabla",
        title="borrar"
    )


def crear_tablas():
    ventana4 = tk.Toplevel()
    ventana4.title("tabla de consultas")
    ventana4.geometry("800x200")
    # Define los valores para el combobox
    tipos = ["VARCHAR", "INT", "FLOAT", "DATE","DATETIME","FLOAT","SMALLINT","BLOB"]
    Key = [" ", "PRIMARY KEY"]
    motores = ["InnoDB","MyISAM"]
    var_list = []

    # Define las variables booleanas para los checkboxes

    # Agrega las entradas a la ventana
    rows = 0
    num_filas_entry = tk.Entry(ventana4)
    num_filas_entry.grid(row=0, column=1, padx=5, pady=5, sticky="snew")
    tk.Label(ventana4, text="Número de filas").grid(row=0, column=0, padx=5, pady=5, sticky="snew")
    nombre_tabla = tk.Entry(ventana4)
    nombre_tabla.grid(row=0, column=3, padx=5, pady=5, sticky="snew")
    tk.Label(ventana4, text="nombre de la tabla:").grid(row=0, column=2, padx=5, pady=5, sticky="snew")
    moto= ttk.Combobox(ventana4, values=motores, state="readonly")
    moto.grid(row=1, column=1, padx=5, pady=5, sticky="snew")
    tk.Label(ventana4, text="Ingrese motor:").grid(row=1, column=0, padx=5, pady=5, sticky="snew")

    def agregar_filas():
        
        # Obtén el número de filas que el usuario quiere agregar
        num_filas = int(num_filas_entry.get())

        if num_filas >= 24:
            messagebox.showerror("Error", "el numero de filas es demasiado grande")
        else:        
            # Crear etiquetas para cada campo en la fila 1
            campos = ["Nombre", "Tipo", "Longitud", "Null", "Indice", "I_A"]
            for c, campo in enumerate(campos):
                tk.Label(ventana4, text=campo).grid(row=2, column=c, padx=5, pady=5, sticky="snew")

            # Agregar los campos de entrada y selección en la fila 2 en adelante
            for r in range(rows, rows + num_filas):
                var = tk.BooleanVar()
                var2 = tk.BooleanVar()
                nom = tk.StringVar()
                tipo = tk.StringVar()
                tamano = tk.StringVar()
                combobox = tk.StringVar()
                var_list.append((nom, tipo, tamano, combobox,var, var2))  # Agregar la variable booleana a la lista
                tk.Entry(ventana4,textvariable=nom).grid(row=r+3, column=0, padx=5, pady=5, sticky="snew")
                ttk.Combobox(ventana4, textvariable=tipo , values=tipos, state="readonly").grid(row=r+3, column=1, padx=5, pady=5, sticky="snew")
                tk.Entry(ventana4,textvariable=tamano).grid(row=r+3, column=2, padx=5, pady=5, sticky="snew")
                ttk.Checkbutton(ventana4, variable=var2).grid(row=r+3, column=5, padx=5, pady=6, sticky="snew")
                ttk.Combobox(ventana4, textvariable=combobox , values=Key, state="readonly").grid(row=r+3, column=4, padx=5, pady=5, sticky="snew")
                ttk.Checkbutton(ventana4, variable=var).grid(row=r+3, column=3, padx=5, pady=6, sticky="snew")

    #recoge los registros de los campos
    def imprimir():
        datab = lista.get(lista.curselection())
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database = datab
        )
        cur = conexion.cursor()
        tabla = []
        nombret = str(nombre_tabla.get())
        motor = str(moto.get())
        for nom, tipo, tamano, combobox, var, var2 in var_list:
            longitud = tamano.get() if tamano.get() else ""
            null = ""
            if combobox.get() == "PRIMARY KEY":
                null= "PRIMARY KEY"
                if tipo.get() != "INT":
                    messagebox.showerror("Error", "El tipo de la llave primaria debe ser INT")
            if var.get():
                null = "NULL"
            else:
                null = "NOT NULL"

            auto = "AUTO_INCREMENT" if var2.get() else " "
            tabla.append(nom.get() + " " + tipo.get() + ("(" + longitud + ")" if longitud else "") + " " + null + " " + combobox.get() + " " +auto)

        resultado_str = ",".join(tabla)
        query = f"CREATE TABLE {nombret} ({resultado_str}) ENGINE={motor};"
        cur.execute(query)

        if query == " ":
            messagebox.showerror(title="Error", message="la consulta esta basi por ende no se puede crear la base de datos")
        else:
            messagebox.showinfo(message="se ha creado la tabla",title="crear tablas")
            conexion.commit()  

    agregar_filas_button = tk.Button(ventana4, text="Agregar filas", command=agregar_filas)
    agregar_filas_button.grid(row=0, column=4, padx=5, pady=5, sticky="snew")
    btton = tk.Button(ventana4, text="Agregar tabla", command=imprimir)
    btton.grid(row=0, column=5, padx=5, pady=5, sticky="snew")




#estas es la parte de las vistas o toda la parte del diseño 
#crear la ventana
ventana = tk.Tk()
ventana.title("Gestor de base de datos Mondragon")
ventana.geometry("650x400")
#lista despligable
lista = tk.Listbox(ventana)
lista.pack()
refresh_listbox()
#texto de la ceracion de la base de datos
texto_chido = ttk.Entry()
texto_chido.place(x=50, y=80)
button = tk.Button(text="crear databas", command=crear)
bor = tk.Button(text="borrar", command=borrar)
bor.place(x=160, y=120)
button.place(x=50, y=120)
#mostrar tablas de base de datos
boton_modificar = tk.Button(ventana, text="Mostrar tablas", command=mostrar_tablas)
boton_modificar.place(x=450, y=30)
#objetos de la consulta
cuadrot = tk.Text()
cuadrot.place(x=50, y=160,height=100,width=200)
boton_consulta = tk.Button( text="hacer consulta", command=consulta)
boton_consulta.place(x=50, y=270)
# boton para crear tablas
btt = tk.Button( text="crear tablas", command=crear_tablas)
btt.place(x=450, y=70)
#iconos del sistema
icono_chico = tk.PhotoImage(file="C:\\mondrago\\imagen\\icon-v1.png")
ventana.iconphoto(True, icono_chico)
ventana.mainloop()