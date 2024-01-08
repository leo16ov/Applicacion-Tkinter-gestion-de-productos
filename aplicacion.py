from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from funciones import * 
import mysql.connector

fuente_gigante= ('Heveltica', 20)
fuente_grande= ('Heveltica', 14)
fuente_mediana= ('Heveltica', 12)
fuente_pequeña= ('Heveltica', 9)
camposUsuario = '(nombre, apellido, nombre_usuario, email, password, telefono)'

root = Tk()
root.resizable(False, False)
root.geometry('700x450')
root.title('Gestion de ventas')
root.configure(bg= 'white')


#------VENTANA DE USUARIO--------

def mostrar_detalles(nombre_producto):
    ventana_detalles = createWindow('Producto','750x650')
    
    mi_db, db_cursor = connectionDB()
    query = "SELECT nombre, precio_venta, categoria, cantidad_en_stock, descripcion FROM Productos WHERE nombre = %s;"
    db_cursor.execute(query, (nombre_producto,))
    resultado = db_cursor.fetchone()

    if resultado:
        nombre, precio, categoria, cantidad, descripcion = resultado
        Label(ventana_detalles, text="", font= fuente_gigante, bg= 'white').pack(pady= 40)
        Label(ventana_detalles, text=f"{nombre}", font= fuente_gigante, bg= 'white').pack(pady= 20)
        Label(ventana_detalles, text=f"${precio}", font= fuente_gigante, bg= 'white').pack()
        Label(ventana_detalles, text=f"-Categoría: {categoria}", font= fuente_mediana, bg= 'white').place(relx= 0.07, rely= 0.6)
        Label(ventana_detalles, text=f"-Stock: {cantidad}", font= fuente_mediana, bg= 'white').place(relx= 0.07, rely= 0.65)
        Label(ventana_detalles, text=f"-Descripción: {descripcion}", font= fuente_mediana, bg= 'white').place(relx= 0.07, rely= 0.7)
    else:
        Label(ventana_detalles, text="Producto no encontrado").pack()

def abrirVentanaUsuario():
    ventanaDeUsuario = createWindow('Usuario', '900x600')
    mi_db, db_cursor = connectionDB()
    query1 = "select nombre, precio_venta from Productos;"
    
    db_cursor.execute(query1)
    
    text = Label(ventanaDeUsuario, text= 'Productos', font= fuente_grande, bg= 'white')
    text.pack(pady= 50)

    productos = []
    for tupleDatos in db_cursor:
        producto = {'nombre': tupleDatos[0],
                    'precio': tupleDatos[1],
                    }
        productos.append(producto)
    x = 0.1
    y = 0.2
    count = 1
    for producto in productos:
        nombre = Label(ventanaDeUsuario, text=producto['nombre'], font=fuente_mediana)
        precio = Label(ventanaDeUsuario, text=str(producto['precio']), font=fuente_mediana)
        
        nombre.place(relx=x, rely=y)
        precio.place(relx=x + 0.04, rely=y + 0.05)
        
        boton = Button(ventanaDeUsuario, text="Ver", command=lambda nombre=producto['nombre']: mostrar_detalles(nombre))
        boton.place(relx=x+ 0.035, rely=y + 0.1)
        
        x += 0.2
        count += 1
        
        if count == 5:
            y += 0.2
            x = 0.1
     
def accionBtnVentanaAdministrador():
    ventana = createWindow('Administradores', '400x400')
    texto = Label(ventana, text= 'Hola administradores')
    texto.place(relx= 0.3, rely=0.2)

"""----------VENTANA DE REGISTRO----------"""
def abrirVentanaRegister():
    root.withdraw()
    ventanaRegister= createWindow('Registrarse', '500x500')
    txtRegister = Label(ventanaRegister, text= 'Registrese', font= fuente_mediana, bg= 'white')
    txtRegister.place(relx= 0.4, rely= 0.05)

    nombreLab, nombreEnt = addCampus(ventanaRegister, 'Nombre', 22, fuente_pequeña)
    nombreLab.place(relx=0.31, rely= 0.15)
    nombreEnt.place(relx=0.31, rely= 0.19)

    apellidoLab, apellidoEnt = addCampus(ventanaRegister, 'Apellido', 22, fuente_pequeña)
    apellidoLab.place(relx=0.31, rely=0.25)
    apellidoEnt.place(relx=0.31, rely=0.29)

    nombreUsuarioLab, nombreUsuarioEnt = addCampus(ventanaRegister, 'Nombre usuario', 22, fuente_pequeña)
    nombreUsuarioLab.place(relx=0.31, rely= 0.35)
    nombreUsuarioEnt.place(relx=0.31, rely= 0.39)

    emailLab, emailEnt = addCampus(ventanaRegister, 'Email', 22, fuente_pequeña)
    emailLab.place(relx= 0.31, rely= 0.45)
    emailEnt.place(relx= 0.31, rely= 0.49)

    contrasenaLab, contrasenaEnt = addCampus(ventanaRegister, 'Contraseña', 22, fuente_pequeña)
    contrasenaLab.place(relx= 0.31, rely= 0.55)
    contrasenaEnt.place(relx= 0.31, rely= 0.59)

    telefonoLab, telefonoEnt = addCampus(ventanaRegister, 'Telefono', 22, fuente_pequeña)
    telefonoLab.place(relx= 0.31, rely= 0.65)
    telefonoEnt.place(relx= 0.31, rely= 0.69)

    def accionBtnAceptarDatosRegistro():
        nombre = nombreEnt.get()
        apellido = apellidoEnt.get()
        userNombre = nombreUsuarioEnt.get()
        email = emailEnt.get()
        contrasena = contrasenaEnt.get()
        telefono = telefonoEnt.get()
    
        mi_db, db_cursor = connectionDB()

        if nombre != '' and apellido != '' and len(userNombre) >=8 and len(contrasena) >=8 and '@gmail.com' in email[len(email)-10:len(email)] and contiene_solo_numeros(telefono):
            try:
                sql = 'insert into Usuarios(nombre, apellido, nombre_usuario, email, password, telefono) values(%s, %s, %s, %s, %s, %s)'
                values = (nombre, apellido, userNombre, email, contrasena, telefono)
                db_cursor.execute(sql, values)
                mi_db.commit()
                deleteEntrys6(nombreEnt, apellidoEnt, nombreUsuarioEnt, emailEnt, contrasenaEnt, telefonoEnt)
                messagebox.showinfo("Exito", "Se ha creado la cuenta con exito.", parent= ventanaRegister)
                
                ventanaRegister.withdraw()
                ventanaBienvenidaUsuario = createWindow('Usuario', '650x570')
                db_cursor.execute(f"select nombre_usuario, nombre, apellido from Usuarios where email = '{email}' and password = '{contrasena}';")
                
                datosUsuario = []
                for datos in db_cursor:
                    datosUsuario.append(datos)
                
                db_cursor.close()
                mi_db.close()

                saludoUsuario = Label(ventanaBienvenidaUsuario, text= f'Bienvenido {datosUsuario[0][1]} {datosUsuario[0][2]}', font= fuente_grande)
                saludoUsuario.configure(bg= 'white')

                mostrar_widget(saludoUsuario, 2000, ventanaBienvenidaUsuario, abrirVentanaUsuario)
    

            except mysql.connector.errors.IntegrityError:
                messagebox.showerror("Error", "El nombre de usuario ingresado ya esta siendo usado. Intentelo de nuevo", parent= ventanaRegister)
        
        elif '@gmail.com' not in email[len(email)-10:len(email)]:
            messagebox.showerror("Error", "Email no valido. Intentelo de nuevo", parent= ventanaRegister)
        elif len(contrasena) < 8:
            messagebox.showerror("Error", "La contraseña es muy corta. Intentelo de nuevo")
        elif len(userNombre) < 8:
            messagebox.showerror("Error", "El nombre de Usuario es muy corto. Intentelo de nuevo")

        elif contiene_solo_numeros(telefono) == False:
            messagebox.showerror("Error", "El telefono debe solo contener numeros. Intentelo de nuevo", parent= ventanaRegister)
        
    btnAceptarLogin = Button(ventanaRegister, text= 'Aceptar', command= accionBtnAceptarDatosRegistro, bg= '#00CC00')
    btnAceptarLogin.place(relx= 0.6, rely= 0.77)

    def VolverDeRegisterAInicio():
        root.deiconify()
        ventanaRegister.withdraw()

    btnVolver = Button(ventanaRegister, text= 'Volver', command= VolverDeRegisterAInicio)
    btnVolver.place(relx= 0.23, rely= 0.77)

"""----------VENTANA DE INICIO DE SESION-----------"""
def abrirVentanaLogin():
    root.withdraw()
    ventanaLogin = createWindow('Iniciar Sesión', '500x500')
    txtLogin = Label(ventanaLogin, text='Iniciar Sesión', font=fuente_mediana, bg='white')
    txtLogin.place(relx=0.4, rely=0.05)

    emailLab, emailEnt = addCampus(ventanaLogin, 'Email', 22, fuente_pequeña)
    emailLab.place(relx=0.31, rely=0.15)
    emailEnt.place(relx=0.31, rely=0.19)

    contrasenaLab, contrasenaEnt = addCampus(ventanaLogin, 'Contraseña', 22, fuente_pequeña)
    contrasenaLab.place(relx=0.31, rely=0.25)
    contrasenaEnt.place(relx=0.31, rely=0.29)

    def accionBtnIniciarSesion():
        email = emailEnt.get()
        contrasena = contrasenaEnt.get()
        
        mi_db, db_cursor = connectionDB()

        if contrasena != '' and '@gmail.com' in email[len(email)-10:len(email)]:

            db_cursor.execute(f"select nombre_usuario, nombre, apellido, idAdministrador from Administradores where email = '{email}' and password = '{contrasena}';")
            
            datosAdministrador = []
            for datosAdmin in db_cursor:
                datosAdministrador.append(datosAdmin)
            
            if datosAdministrador:
                emailEnt.delete(0, END)
                contrasenaEnt.delete(0, END)
                ventanaLogin.withdraw()
                ventanaBienvenidaAdministrador = createWindow('Administrador', '650x570')
                saludoAdministrador = Label(ventanaBienvenidaAdministrador, text=f'Bienvenido {datosAdministrador[0][1]} {datosAdministrador[0][2]}', font=fuente_grande)
                saludoAdministrador.configure(bg='white')

                def menu(ventana):
                    def regresarAVentanaAnterior(ventanaAocultar):
                        ventanaAocultar.withdraw()
                        ventana.deiconify()

                    #-----PROVEEDORES-----

                    def abrir_ver_proveedores():
                        ventanaVerProveedores = createWindow('Ver Proveedores', '700x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaVerProveedores, text='←', font=fuente_grande, command=lambda: regresarAVentanaAnterior(ventanaVerProveedores))
                        btnVolver.place(relx=0.03, rely=0.03)
                        query = f'select apellido from Proveedores;'
                        comboProveedor = createCombo(ventanaVerProveedores, 16, 'Seleccione ID', query)
                        comboProveedor.place(relx= 0.1, rely= 0.2)

                        lblProv = Label(ventanaVerProveedores, text= 'Proveedor', font= fuente_pequeña, bg= 'white')
                        lblProv.place(relx= 0.1, rely= 0.165)

                        def accionVerProveedor():
                            if comboProveedor.get() != 'Seleccione ID':
                                columnsNames = ('ID', 'Nombre', 'Apellido', 'Telefono')
                                tamanoColumns = [60, 110, 110, 120]
                                query = f'select * from Proveedores where apellido = "{comboProveedor.get()}";'
                                tablaProveedor = createTable(ventanaVerProveedores, 4, columnsNames, tamanoColumns, query)
                                tablaProveedor.place(relx= 0.1, rely= 0.35)

                        btnVerProv = Button(ventanaVerProveedores, text= 'Ver', command= accionVerProveedor)
                        btnVerProv.place(relx= 0.4, rely= 0.2)

                    def abrir_agregar_proveedores():
                        ventanaAgregarProveedores = createWindow('Agregar Proveedores', '700x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaAgregarProveedores, text='←', font=fuente_grande, command=lambda: regresarAVentanaAnterior(ventanaAgregarProveedores))
                        btnVolver.place(relx=0.03, rely=0.03)
                        text = Label(ventanaAgregarProveedores, text='Complete los datos del proveedor', font=fuente_mediana, bg='white')
                        text.place(relx=0.3, rely=0.1)
                        nombreLab, nombreEnt = addCampus(ventanaAgregarProveedores, 'Nombre', 20, fuente_pequeña)
                        nombreLab.place(relx= 0.37, rely= 0.2)
                        nombreEnt.place(relx= 0.37, rely= 0.235)
                        
                        apellidoLab, apellidoEnt = addCampus(ventanaAgregarProveedores, 'Apellido', 20, fuente_pequeña)
                        apellidoLab.place(relx= 0.37, rely= 0.3)
                        apellidoEnt.place(relx= 0.37, rely= 0.335)

                        telefonolab, telefonoEnt = addCampus(ventanaAgregarProveedores, 'Telefono', 20, fuente_pequeña)
                        telefonolab.place(relx=0.37, rely=0.4)
                        telefonoEnt.place(relx=0.37, rely=0.435)

                        def accionBtnAceptar():
                            nombre = nombreEnt.get()
                            apellido = apellidoEnt.get()
                            telefono = telefonoEnt.get()

                            if nombre!= '' and apellido != '' and telefono.isdigit() and len(telefono) == 10:
                                mi_db, db_cursor = connectionDB()
                                values = (nombre, apellido, telefono)
                                sql = 'insert into Proveedores(nombre, apellido, telefono) values(%s,%s,%s);'
                                
                                try:
                                    db_cursor.execute(sql, values)
                                    mi_db.commit()
                                    db_cursor.close()
                                    mi_db.close()

                                    nombreEnt.delete(0, END)
                                    apellidoEnt.delete(0, END)
                                    telefonoEnt.delete(0, END)
                                    messagebox.showinfo("Exito", "Se ha guardado la informacion del Proveedor con exito.")
                                
                                except mysql.connector.errors.DatabaseError:
                                    messagebox.showerror("Error", 'Parece ser que el telefono que desea ingresar ya esta siendo usado. Puede intentar con otro.')
                                    
                            elif nombre == '':
                                messagebox.showerror("Error", 'El nombre no puede estar vacio. Intentelo de nuevo')
                            elif apellido == '':
                                messagebox.showerror("Error", 'El apellido no puede estar vacio. Intentelo de nuevo')
                            elif len(telefono) != 10 or not telefono.isdigit():
                                messagebox.showerror("Error", 'El telefono debe estar compuesto por 10 numeros. Intentelo de nuevo')

                        btnAceptar = Button(ventanaAgregarProveedores, text= 'Aceptar', command= accionBtnAceptar, bg= '#00CC00')
                        btnAceptar.place(relx= 0.6, rely= 0.55)

                    def abrir_actualizar_proveedores():
                        ventanaActualizarProveedores = createWindow('Actualizar Proveedores', '800x650')
                        ventana.withdraw()
                        btnVolver = Button(ventanaActualizarProveedores, text='←', font=fuente_grande, command=lambda: regresarAVentanaAnterior(ventanaActualizarProveedores))
                        btnVolver.place(relx=0.03, rely=0.03)
                        query = 'select IdProveedor from  Proveedores;'
                        comboProveedores = createCombo(ventanaActualizarProveedores, 16, 'Seleccione ID', query)
                        comboProveedores.place(relx= 0.1, rely= 0.2)
                        lblProv = Label(ventanaActualizarProveedores, text= 'Proveedores', font= fuente_pequeña, bg= 'white')
                        lblProv.place(relx= 0.1, rely= 0.165)

                        def accionConsultarProveedor():
                            if comboProveedores.get() != 'Seleccione ID':
                                query = f'select * from Proveedores where IdProveedor = {comboProveedores.get()};'
                                columnsNames = ('ID', 'Nombre', 'Apellido', 'Telefono')
                                columnsTamanos = [50, 110, 110, 100]
                                tablaProveedores = createTable(ventanaActualizarProveedores, 4, columnsNames, columnsTamanos, query)
                                tablaProveedores.configure(height= 3)
                                tablaProveedores.place(relx= 0.1, rely= 0.3)

                        btnConsultar = Button(ventanaActualizarProveedores, text= 'Consultar', command= accionConsultarProveedor)
                        btnConsultar.place(relx= 0.33, rely= 0.2)
                        values = ['Seleccione campo', 'nombre', 'apellido', 'telefono']
                        comboCampos = createSimpleCombo(ventanaActualizarProveedores, 16, values)
                        comboCampos.place(relx= 0.1, rely= 0.5)
                        def accionSiguiente():
                            if comboCampos.get() != 'Seleccione campo':
                                lblValorNuevo = Label(ventanaActualizarProveedores, text= f'{comboCampos.get()[0].upper()+comboCampos.get()[1:len(comboCampos.get())]}', font= fuente_pequeña, bg= 'white')
                                lblValorNuevo.place(relx= 0.6, rely= 0.465)
                                entValorNuevo = Entry(ventanaActualizarProveedores)
                                entValorNuevo.place(relx= 0.6, rely= 0.5)

                                def accionActualizar():
                                    if comboCampos.get() != 'Selecione campo' and comboProveedores.get() != 'Seleccione ID':
                                        if comboCampos.get() == 'telefono' :
                                            if len(entValorNuevo.get())!= 10 or not contiene_solo_numeros(entValorNuevo.get()):
                                                messagebox.showerror("Error", 'El Telofono debe estar compuesto por 10 numeros.')
                                            elif len(entValorNuevo.get())== 10 and contiene_solo_numeros(entValorNuevo.get()) and comboProveedores.get() != 'Seleccione ID':
                                                try:
                                                    mi_db, db_cursor = connectionDB()
                                                    db_cursor.execute(f'update Proveedores set {comboCampos.get()} = "{entValorNuevo.get()}" where IdProveedor = {comboProveedores.get()};')
                                                    mi_db.commit()
                                                    db_cursor.close()
                                                    mi_db.close()
                                                except:
                                                    messagebox.showerror("Error", 'Ocurrio un error inesperado. Intentelo de nuevo.')
                                        else:
                                            try:
                                                mi_db, db_cursor = connectionDB()
                                                db_cursor.execute(f'update Proveedores set {comboCampos.get()} = "{entValorNuevo.get()}" where IdProveedor = {comboProveedores.get()};')
                                                mi_db.commit()
                                                db_cursor.close()
                                                mi_db.close()
                                            except:
                                                messagebox.showerror("Error", 'Ocurrio un error inesperado. Intentelo de nuevo.')

                                btnActualizar = Button(ventanaActualizarProveedores, text= 'Actualizar', command= accionActualizar, bg= 'yellow')
                                btnActualizar.place(relx= 0.83, rely= 0.5)
                        btnSiguiente = Button(ventanaActualizarProveedores, text= 'Siguiente', command= accionSiguiente)
                        btnSiguiente.place(relx= 0.33, rely= 0.5)

                    def abrir_eliminar_proveedores():
                        ventanaEliminarProveedores = createWindow('Eliminar Proveedores', '700x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaEliminarProveedores, text='←', font=fuente_grande, command=lambda: regresarAVentanaAnterior(ventanaEliminarProveedores))
                        btnVolver.place(relx=0.03, rely=0.03)

                        comboProveedor = createCombo(ventanaEliminarProveedores, 14, 'Seleccione ID', 'select IdProveedor from Proveedores;')
                        comboProveedor.place(relx= 0.1, rely= 0.185)
                        lblProv = Label(ventanaEliminarProveedores, text='Proveedor', font= fuente_pequeña, bg= 'white')
                        lblProv.place(relx= 0.1, rely= 0.15)
                        def accionConsultarProveedor():
                            if comboProveedor.get() != 'Seleccione ID':
                                query = f'select * from Proveedores where IdProveedor = {comboProveedor.get()};'
                                columnsNames = ('ID', 'Nombre', 'Apellido', 'Telefono')
                                columnsTamanos = [60, 110, 110, 130]
                                tablaProveedores = createTable(ventanaEliminarProveedores, 4, columnsNames, columnsTamanos, query)
                                tablaProveedores.configure(height= 3)
                                tablaProveedores.place(relx= 0.1, rely= 0.4)

                        def accionEliminarProveedor():
                            if comboProveedor.get() != 'Seleccione ID':
                                try:
                                    mi_db, db_cursor = connectionDB()
                                    db_cursor.execute(f'delete from Proveedores where IdProveedor = {comboProveedor.get()};')
                                    mi_db.commit()
                                    updateCombo(comboProveedor, 'Seleccione ID', 'select IdProveedor from Proveedores;')
                                except mysql.connector.errors.DatabaseError:
                                        messagebox.showerror("Error", 'El Proveedor que desea eliminar esta anotado en los productos, por lo que primero debera eliminar al proveedor de todos lo productos en los que esté.')
        
                        btnConsultarProv = Button(ventanaEliminarProveedores, text= 'Consultar', command= accionConsultarProveedor)
                        btnConsultarProv.place(relx= 0.33, rely= 0.185)
                        btnEliminarProveedor = Button(ventanaEliminarProveedores, text= 'Eliminar', command= accionEliminarProveedor, bg= 'red')
                        btnEliminarProveedor.place(relx= 0.33, rely= 0.25)

                    #-----PRODUCTOS------
                    def producto_buscarPorfiltro():
                        ventanaVerProductos = createWindow('Ver por filtro', '900x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaVerProductos, text= '←', font=fuente_grande, command= lambda:regresarAVentanaAnterior(ventanaVerProductos))
                        btnVolver.place(relx= 0.03, rely= 0.03)

                        comboMetodo = createSimpleCombo(ventanaVerProductos, 16, ['Seleccione metodo', 'nombre', 'precio_venta', 'precio_proveedor', 'categoria', 'cantidad_en_stock', 'Proveedor', 'Administrador'])
                        comboMetodo.place(relx= 0.05, rely= 0.2)
                        
                        entryValue = Entry(ventanaVerProductos)
                        entryValue.place(relx= 0.33, rely= 0.2)
                        lblValue = Label(ventanaVerProductos, text= 'Busque', font= fuente_pequeña, bg= 'white')
                        lblValue.place(relx= 0.33, rely= 0.165)

                        def accionVer():
                            if comboMetodo.get() !=  'Seleccione metodo':
                                nameColumns = ('Codigo', 'Nombre', 'Precio venta', 'Categoria', 'Stock', 'Precio prov.', 'Proveedor', 'Adminisnitrador')
                                tamColumns = [60, 130, 100, 130, 60, 100, 130, 130]
                                if contiene_solo_numeros(entryValue.get()):
                                    query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.categoria, 
                                    pd.cantidad_en_stock, pd.precio_proveedor, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , 
                                    CONCAT(ad.nombre, ' ', ad.apellido)as Administrador from Productos pd, Proveedores pv, Administradores ad 
                                    where pv.IdProveedor = pd.IdProveedor and ad.IdAdministrador = pd.IdAdministrador and {comboMetodo.get()} = {entryValue.get()};
                                    """
                                else:
                                    if comboMetodo.get() == 'Proveedor':
                                        query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.categoria, 
                                        pd.cantidad_en_stock, pd.precio_proveedor, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , 
                                        CONCAT(ad.nombre, ' ', ad.apellido)as Administrador from Productos pd, Proveedores pv, Administradores ad 
                                        where pv.IdProveedor = pd.IdProveedor and ad.IdAdministrador = pd.IdAdministrador and pv.apellido = "{entryValue.get()}";
                                        """
                                    elif comboMetodo.get() == 'Administrador':
                                        query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.categoria, 
                                        pd.cantidad_en_stock, pd.precio_proveedor, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , 
                                        CONCAT(ad.nombre, ' ', ad.apellido)as Administrador from Productos pd, Proveedores pv, Administradores ad 
                                        where pv.IdProveedor = pd.IdProveedor and ad.IdAdministrador = pd.IdAdministrador and ad.apellido  = "{entryValue.get()}";
                                        """
                                    else:     
                                        query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.categoria, 
                                        pd.cantidad_en_stock, pd.precio_proveedor, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , 
                                        CONCAT(ad.nombre, ' ', ad.apellido)as Administrador from Productos pd, Proveedores pv, Administradores ad 
                                        where pv.IdProveedor = pd.IdProveedor and ad.IdAdministrador = pd.IdAdministrador and pd.{comboMetodo.get()} = "{entryValue.get()}";
                                        """
                                tablaProductos = createTable(ventanaVerProductos, 8, nameColumns, tamColumns, query)
                                tablaProductos.place(relx= 0.05, rely= 0.35)

                        btnVer = Button(ventanaVerProductos, text= 'Ver', command= accionVer)
                        btnVer.place(relx= 0.55, rely= 0.2)

                    def abrir_agregar_productos():
                        ventanaAgregarProductos = createWindow('Agregar Productos', '700x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaAgregarProductos, text= '←', font= fuente_grande, command= lambda:regresarAVentanaAnterior(ventanaAgregarProductos))
                        btnVolver.place(relx= 0.03, rely= 0.03)
                        text = Label(ventanaAgregarProductos, text= 'Complete los datos del producto', font= fuente_mediana, bg= 'white')
                        text.place(relx=0.3, rely=0.1)
                        codigoProductoLab, codigoProductoEnt = addCampus(ventanaAgregarProductos, 'Codigo producto', 20, fuente_pequeña)
                        codigoProductoLab.place(relx= 0.37, rely= 0.2)
                        codigoProductoEnt.place(relx= 0.37, rely= 0.235)
                        
                        nombreLab, nombreEnt = addCampus(ventanaAgregarProductos, 'Nombre', 20, fuente_pequeña)
                        nombreLab.place(relx= 0.37, rely= 0.3)
                        nombreEnt.place(relx= 0.37, rely= 0.335)

                        precioVentaLab, precioVentaEnt = addCampus(ventanaAgregarProductos, 'Precio de Venta', 20, fuente_pequeña)
                        precioVentaLab.place(relx=0.37, rely=0.4)
                        precioVentaEnt.place(relx=0.37, rely=0.435)

                        precioProveedorLab, precioProveedorEnt = addCampus(ventanaAgregarProductos, 'Precio de Proveedor', 20, fuente_pequeña)
                        precioProveedorLab.place(relx=0.37, rely=0.5)
                        precioProveedorEnt.place(relx=0.37, rely=0.535)

                        stockLab, stockEnt = addCampus(ventanaAgregarProductos, 'Cantidad en Stock', 20, fuente_pequeña)
                        stockLab.place(relx=0.37, rely=0.6)
                        stockEnt.place(relx=0.37, rely=0.635)

                        categoriaLab, categoriaEnt = addCampus(ventanaAgregarProductos, 'Categoría', 20, fuente_pequeña)
                        categoriaLab.place(relx=0.37, rely=0.7)
                        categoriaEnt.place(relx=0.37, rely=0.735)

                        def accionBtnSiguiente():
                            codigoProducto = codigoProductoEnt.get()
                            nombre = nombreEnt.get()
                            precioVenta = precioVentaEnt.get()
                            precioProveedor = precioProveedorEnt.get()
                            categoria = categoriaEnt.get()
                            cantidadStock = stockEnt.get()
                            if codigoProducto.isdigit() and nombre != '' and categoria != ''and es_decimal(precioVenta) and es_decimal(precioProveedor) and es_decimal(cantidadStock):
                                ventanaAgregarProductos.withdraw()
                                ventanaSiguiente = createWindow('Agregar Productos', '700x550')
                                text = Label(ventanaSiguiente, text= 'Complete los datos del producto', font= fuente_mediana, bg= 'white')
                                text.place(relx=0.3, rely=0.1)
                                descripcionLab = Label(ventanaSiguiente, text='Descripcion', font= fuente_pequeña, bg= 'white')
                                descripcionEnt = Text(ventanaSiguiente, height= 8, width= 55)
                                descripcionLab.place(relx= 0.17, rely= 0.53)
                                descripcionEnt.place(relx= 0.17, rely= 0.565)
                                
                                sql = 'select IdProveedor from Proveedores;'
                                txtIdProv = Label(ventanaSiguiente, text= 'Proveedor', font= fuente_pequeña, bg= 'white')
                                txtIdProv.place(relx= 0.17, rely= 0.2)
                                comboIdProveedores = createCombo(ventanaSiguiente, 14, 'Seleccione ID', sql)
                                comboIdProveedores.place(relx= 0.17, rely= 0.235)
                                def accionConsultarProveedor():
                                    if comboIdProveedores.get().isdigit():
                                        query = f'select * from Proveedores where IdProveedor = {comboIdProveedores.get()};'
                                        columns = ('ID','Nombre', 'Apellido', 'Telefono')
                                        tamano = [40, 80, 80, 120]
                                        tablaProveedor = createTable(ventanaSiguiente, 4, columns, tamano, query)
                                        tablaProveedor.configure(height= 3)
                                        tablaProveedor.place(relx= 0.17, rely= 0.335)

                                btnConsultarProveedor = Button(ventanaSiguiente, text= 'Consultar', command= accionConsultarProveedor)
                                btnConsultarProveedor.place(relx= 0.4, rely= 0.235)

                                def accionBtnAceptar():
                                    descripcion = descripcionEnt.get("1.0", "end-1c")
                                    if comboIdProveedores.get().isdigit():
                                        try:
                                            mi_db, db_cursor = connectionDB()
                                            query = 'insert into Productos(Codigo_Producto, nombre, precio_venta, precio_proveedor, categoria, cantidad_en_stock, descripcion, idProveedor, idAdministrador) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                                            values = (codigoProducto, nombre, precioVenta, precioProveedor, categoria, cantidadStock, descripcion, comboIdProveedores.get(), datosAdministrador[0][3])
                                            db_cursor.execute(query, values)
                                            mi_db.commit()
                                            db_cursor.close()
                                            mi_db.close()
                                            codigoProductoEnt.delete(0, END)
                                            nombreEnt.delete(0, END)
                                            precioVentaEnt.delete(0, END)
                                            precioProveedorEnt.delete(0, END)
                                            categoriaEnt.delete(0, END)
                                            stockEnt.delete(0, END)
                                            if descripcion != '':
                                                descripcionEnt.delete(0.0, END)
        
                                            messagebox.showinfo('Exito', 'Se ha guardado todo con exito.')
                                            ventanaSiguiente.withdraw()
                                            ventanaAgregarProductos.deiconify()
                                        except mysql.connector.errors.IntegrityError:
                                            messagebox.showerror("Error", 'Ha ocurrido un error con respecto a guardar datos con un "Codigo de producto" que ya esta en uso.')
                                def accionBtnAtras():
                                    ventanaSiguiente.withdraw()
                                    ventanaAgregarProductos.deiconify()
                            
                                btnVolverAtras = Button(ventanaSiguiente, text= 'Atras', command= accionBtnAtras)
                                btnVolverAtras.place(relx= 0.17, rely= 0.85)
                                btnAceptar = Button(ventanaSiguiente, text= 'Aceptar', bg='#00CC00', command= accionBtnAceptar)
                                btnAceptar.place(relx= 0.7, rely= 0.85)
                            elif nombre == '' or categoria == '':
                                messagebox.showerror('Faltan completar campos', 'Debe completar todos los campos para poder seguir. Intetelo de nuevo')
                            elif not codigoProducto.isdigit():
                                messagebox.showerror('Error', 'El "Codigo producto" debe ser un numero.')
                            elif not cantidadStock.isdigit():
                                messagebox.showerror('Error', 'La "Cantidad en Stock" debe ser un numero.')
                            elif not es_decimal(precioProveedor):
                                messagebox.showerror('Error', 'El "Precio de Proveedor" debe ser un numero decimal.')
                            elif not es_decimal(precioVenta):
                                messagebox.showerror('Error', 'El "Precio de Venta" debe ser un numero decimal.')

                        btnSiguiente = Button(ventanaAgregarProductos, text='Siguiente', command= accionBtnSiguiente, bg='#00CC00')
                        btnSiguiente.place(relx= 0.55, rely= 0.8)
                        #------""""MEE QUEEEDEEE ACAAAA""""------
                    
                    def abrir_actualizar_productos():
                        ventanaActualizarProductos = createWindow('Actualizar Productos', '1000x700')
                        ventana.withdraw()
                        btnVolver = Button(ventanaActualizarProductos, text='←', font=fuente_grande, command= lambda:regresarAVentanaAnterior(ventanaActualizarProductos))
                        btnVolver.place(relx= 0.03, rely= 0.03)
                        sql = 'select Codigo_producto from Productos;'
                        comboProducto = createCombo(ventanaActualizarProductos, 16, 'Seleccione codigo', sql)
                        comboProducto.place(relx= 0.1, rely= 0.14)
                        lblProducto = Label(ventanaActualizarProductos, text= 'Producto', font= fuente_pequeña, bg= 'white')
                        lblProducto.place(relx= 0.1, rely= 0.11)
                        def accionConsultarProducto():
                            if comboProducto.get().isdigit():
                                columns = ('Codigo', 'Nombre', 'Precio venta', 'Precio prov.', 'Categoria', 'Stock', 'Proveedor')
                                tamano = [60, 150, 120, 110, 110, 60, 110]
                                query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.precio_proveedor, pd.categoria,
                                        pd.cantidad_en_stock, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor
                                        from Productos pd, Proveedores pv where pv.IdProveedor = pd.IdProveedor and pd.Codigo_producto = {comboProducto.get()};"""
                                tablaProducto = createTable(ventanaActualizarProductos, 7, columns, tamano, query)
                                tablaProducto.configure(height= 4)
                                tablaProducto.place(relx= 0.1, rely= 0.25)

                        btnConsultar = Button(ventanaActualizarProductos, text= 'Consultar', command= accionConsultarProducto)
                        btnConsultar.place(relx= 0.28, rely= 0.14)
                        values = ['Codigo_producto', 'nombre', 'precio_venta', 'precio_proveedor', 'categoria', 'cantidad_en_stock', 'Proveedor']
                        comboDato = createSimpleCombo(ventanaActualizarProductos, 16, values)
                        comboDato.place(relx= 0.1, rely= 0.5)
                        lblDato = Label(ventanaActualizarProductos, text= 'Dato', bg='white', font= fuente_pequeña)
                        lblDato.place(relx= 0.1, rely= 0.47)
                                    
                        def accionSiguiente():
                            # Verificar si comboProveedor existe y eliminarlo si es el caso
                            if 'comboProveedor' in locals() or 'comboProveedor' in globals():
                                eliminar_widget(comboProveedor)
                            # Verificar si entValorNuevo existe y eliminarlo si es el caso
                            if 'entValorNuevo' in locals() or 'entValorNuevo' in globals():
                                eliminar_widget(entValorNuevo)

                            if comboDato.get() == 'Proveedor' and comboProducto.get().isdigit():
                                lblProv = Label(ventanaActualizarProductos, text='Nuevo dato', font=fuente_pequeña, bg='white')
                                lblProv.place(relx=0.5, rely=0.47)
                                comboProveedor = createCombo(ventanaActualizarProductos, 16, 'Seleccione ID', 'select IdProveedor from Proveedores;')
                                comboProveedor.place(relx=0.5, rely=0.5)

                                def accionActualizarProducto():
                                    if comboProducto.get().isdigit() and comboProveedor.get().isdigit():
                                        mi_db, db_cursor = connectionDB()
                                        if comboDato.get() == 'Proveedor':
                                            db_cursor.execute(f'update Productos set IdProveedor = {comboProveedor.get()} where Codigo_producto = {comboProducto.get()}')
                                            mi_db.commit()
                                            db_cursor.close()
                                            mi_db.close()

                                    elif not comboProducto.get().isdigit():
                                        messagebox.showerror('Ups', "Se ha olvidado de seleccionar el Codigo del Producto.")

                                btnActualizar = Button(ventanaActualizarProductos, text='Actualizar', command=accionActualizarProducto, bg='yellow')
                                btnActualizar.place(relx=0.68, rely=0.5)

                            elif comboDato.get() != 'Proveedor' and comboDato.get() in values:

                                lbl2 = Label(ventanaActualizarProductos, text='Nuevo dato', font=fuente_pequeña, bg='white')
                                lbl2.place(relx=0.5, rely=0.47)
                                entValorNuevo = Entry(ventanaActualizarProductos, width= 17)
                                entValorNuevo.place(relx=0.5, rely=0.5)

                                def accionActualizarProducto():
                                    if comboProducto.get().isdigit() and entValorNuevo.get() != '':
                                        mi_db, db_cursor = connectionDB()
                                        if comboDato.get() != 'Proveedor':
                                            try:
                                                db_cursor.execute(f'update Productos set {comboDato.get()} = "{entValorNuevo.get()}" where Codigo_producto = {comboProducto.get()};')
                                                mi_db.commit()
                                                db_cursor.close()
                                                mi_db.close()
                                                if comboDato.get() == 'Codigo_producto':
                                                    comboProducto.delete(0, END)
                                                    updateCombo(comboProducto, 'Seleccione codigo', 'select Codigo_producto from Productos;')
                                            except mysql.connector.errors.DatabaseError:
                                                messagebox.showerror("Error", 'Valor no valido para el dato a actualizar. Intentelo de nuevo')
                                    elif entValorNuevo.get() == '':
                                        messagebox.showerror("Error", 'El valor nuevo no puede estar vacio.')
                                    elif not comboProducto.get().isdigit():
                                        messagebox.showerror('Ups', "Se ha olvidado de seleccionar el Codigo del Producto.")

                                btnActualizar = Button(ventanaActualizarProductos, text='Actualizar', command=accionActualizarProducto, bg='yellow')
                                btnActualizar.place(relx=0.68, rely=0.5)

                        btnSiguiente = Button(ventanaActualizarProductos, text='Siguiente', command=accionSiguiente)
                        btnSiguiente.place(relx=0.28, rely=0.5)

                    def abrir_eliminar_productos():
                        ventanaEliminarProductos = createWindow('Eliminar Productos', '880x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaEliminarProductos, text= '←', font=fuente_grande, command= lambda:regresarAVentanaAnterior(ventanaEliminarProductos))
                        btnVolver.place(relx= 0.03, rely= 0.03)
                        query = 'select Codigo_producto from Productos;'
                        comboProducto = createCombo(ventanaEliminarProductos, 16, 'Seleccione codigo', query)
                        comboProducto.place(relx= 0.18, rely= 0.235)
                        lblProducto = Label(ventanaEliminarProductos, text= 'Producto', font= fuente_pequeña, bg= 'white')
                        lblProducto.place(relx= 0.18, rely= 0.2)

                        def accionConsultarProducto():
                            if comboProducto.get().isdigit():
                                columns = ('Codigo', 'Nombre', 'Precio venta', 'Precio prov.', 'Categoria', 'Stock', 'Proveedor', 'ID Admin')
                                tamano = [60, 150, 120, 110, 110, 60, 110, 100]
                                query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.precio_proveedor, pd.categoria,
                                        pd.cantidad_en_stock, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , IdAdministrador 
                                        from Productos pd, Proveedores pv where pv.IdProveedor = pd.IdProveedor and pd.Codigo_producto = {comboProducto.get()};  
                                        """
                                tablaProducto = createTable(ventanaEliminarProductos, 8, columns, tamano, query)
                                tablaProducto.configure(height= 6)
                                tablaProducto.place(relx= 0.03, rely= 0.5)

                        btnConsultar = Button(ventanaEliminarProductos, text= 'Consultar', command= accionConsultarProducto)
                        btnConsultar.place(relx= 0.4, rely= 0.235)

                        def accionEliminarProducto():
                            if comboProducto.get().isdigit():
                                mi_db, db_cursor = connectionDB()
                                sql = f'delete from Productos where Codigo_producto = {comboProducto.get()};'
                                comboProducto.delete(0, END)
                                db_cursor.execute(sql)
                                mi_db.commit()
                                db_cursor.close()
                                mi_db.close()
                                
                                sql = 'select Codigo_producto from Productos;'
                                updateCombo(comboProducto, 'Seleccione codigo', sql)

                        btnEliminar = Button(ventanaEliminarProductos, text= 'Eliminar', command= accionEliminarProducto, bg= 'red')
                        btnEliminar.place(relx= 0.4, rely= 0.3)
                    
                    def producto_buscarPorCodigo():
                        ventanaVerProductos = createWindow('Ver por codigo', '900x550')
                        ventana.withdraw()
                        btnVolver = Button(ventanaVerProductos, text= '←', font=fuente_grande, command= lambda:regresarAVentanaAnterior(ventanaVerProductos))
                        btnVolver.place(relx= 0.03, rely= 0.03)
                        query = f'select Codigo_producto from Productos;'
                        comboProductos = createCombo(ventanaVerProductos, 16, 'Seleccione codigo', query)
                        comboProductos.place(relx= 0.05, rely= 0.2)

                        lblProducto = Label(ventanaVerProductos, text= 'Producto', bg= 'white', font= fuente_pequeña)
                        lblProducto.place(relx= 0.05, rely= 0.165)

                        def accionVer():
                            if comboProductos.get() !=  'Seleccione codigo':
                                nameColumns = ('Codigo', 'Nombre', 'Precio venta', 'Categoria', 'Stock', 'Precio prov.', 'Proveedor', 'Adminisnitrador')
                                tamColumns = [60, 140, 100, 100, 60, 100, 130, 130]
                            
                                query = f"""select pd.Codigo_producto, pd.nombre, pd.precio_venta, pd.categoria, 
                                pd.cantidad_en_stock, pd.precio_proveedor, CONCAT(pv.nombre, ' ', pv.apellido)as Proveedor , 
                                CONCAT(ad.nombre, ' ', ad.apellido)as Administrador from Productos pd, Proveedores pv, Administradores ad 
                                where pv.IdProveedor = pd.IdProveedor and ad.IdAdministrador = pd.IdAdministrador and pd.Codigo_producto = "{comboProductos.get()}";
                                """
                                tablaProductos = createTable(ventanaVerProductos, 8, nameColumns, tamColumns, query)
                                tablaProductos.place(relx= 0.05, rely= 0.35)

                        btnVer = Button(ventanaVerProductos, text= 'Ver', command= accionVer)
                        btnVer.place(relx= 0.3, rely= 0.2)

                    barra_menu = Menu(ventana)

                    # Crea un menú desplegable "Archivo" con opciones
                    menu_archivo = Menu(barra_menu, tearoff=0)
                    menu_archivo.add_separator()
                    menu_archivo.add_command(label="Salir", command=ventana.quit)

                    # Agrega el menú "Archivo" a la barra de menú
                    barra_menu.add_cascade(label="Inicio", menu=menu_archivo)

                    # Crea un menú desplegable "Productos" con opciones
                    menu_productos = Menu(barra_menu, tearoff=0)

                    submenu_ver_productos = Menu(menu_productos, tearoff=0)
                    submenu_ver_productos.add_command(label="Ver por codigo", command= producto_buscarPorCodigo)
                    submenu_ver_productos.add_command(label="Ver por filtro", command= producto_buscarPorfiltro)

                    menu_productos.add_cascade(label="Ver productos", menu=submenu_ver_productos)
                    menu_productos.add_command(label="Añadir productos", command=abrir_agregar_productos)
                    menu_productos.add_command(label="Actualizar productos", command=abrir_actualizar_productos)
                    menu_productos.add_command(label="Eliminar productos", command=abrir_eliminar_productos)

                    # Agrega el menú "Productos" a la barra de menú

                    # Agrega el menú "Productos" a la barra de menú
                    barra_menu.add_cascade(label="Productos", menu=menu_productos)

                    menu_proveedores = Menu(barra_menu, tearoff=0)

                    menu_proveedores.add_command(label="Ver proveedores", command=abrir_ver_proveedores)
                    menu_proveedores.add_command(label="Añadir proveedores", command=abrir_agregar_proveedores)
                    menu_proveedores.add_command(label="Actualizar proveedores", command=abrir_actualizar_proveedores)
                    menu_proveedores.add_command(label="Quitar proveedores", command=abrir_eliminar_proveedores)

                    barra_menu.add_cascade(label="Proveedores", menu= menu_proveedores)

                    # Configura la barra de menú en la ventana
                    ventana.config(menu=barra_menu)

                def abrirVentanaAdministrador():
                    ventanaAdministrador = createWindow('Administrador', '650x570')
                    textPrincipal = Label(ventanaAdministrador, text='Administrador', font= fuente_grande, bg= 'white')
                    textPrincipal.place(relx=0.4, rely= 0.1)
                    menu(ventanaAdministrador)

                mostrar_widget(saludoAdministrador, 2000, ventanaBienvenidaAdministrador, abrirVentanaAdministrador)

            else:
                db_cursor.execute(f"select nombre_usuario, nombre, apellido from Usuarios where email = '{email}' and password = '{contrasena}';")    
                datosUsuario = []
                for datosUser in db_cursor:
                    datosUsuario.append(datosUser)

                db_cursor.close()
                mi_db.close()
            
                if datosUsuario:
                    emailEnt.delete(0, END)
                    contrasenaEnt.delete(0, END)
                    ventanaLogin.withdraw()
                    ventanaBienvenidaUsuario = createWindow('Usuario', '650x570')
                    saludoUsuario = Label(ventanaBienvenidaUsuario, text=f'Bienvenido {datosUsuario[0][1]} {datosUsuario[0][2]}', font=fuente_grande)
                    saludoUsuario.configure(bg='white')

                    mostrar_widget(saludoUsuario, 2000, ventanaBienvenidaUsuario, abrirVentanaUsuario)
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas. Intenta de nuevo", parent=ventanaLogin)
        
        elif '@gmail.com' not in email[len(email)-10:len(email)]:
            messagebox.showerror("Error", "Email no valido. Intentelo de nuevo", parent= ventanaLogin)

    btnAceptarLogin = Button(ventanaLogin, text='Iniciar Sesión', command=accionBtnIniciarSesion, bg='#00CC00')
    btnAceptarLogin.place(relx=0.6, rely=0.4)

    def VolverDeLoginAInicio():
        root.deiconify()
        ventanaLogin.withdraw()

    btnVolver = Button(ventanaLogin, text='Volver', command=VolverDeLoginAInicio)
    btnVolver.place(relx=0.23, rely=0.4)


btnAbrirVentanaLogin = Button(root, text= 'Iniciar sesion', command= abrirVentanaLogin)
btnAbrirVentanaLogin.place(relx= 0.65, rely= 0.03, width= 110)
btnAbrirVentanaLogin.configure(bg= '#2CDD6F', fg= 'white')

btnAbrirVentanaRegister = Button(root, text= 'Registrarse', command= abrirVentanaRegister)
btnAbrirVentanaRegister.place(relx= 0.83, rely= 0.03, width=110)
btnAbrirVentanaRegister.configure(bg= '#228DFF', fg= 'white')

textoPrincipal = Label(root, text='Plataforma de administracion, gestion y exhibicion de productos.', font= fuente_grande, bg= 'white')
textoPrincipal.place(relx=0.07, rely=0.4)

root.mainloop()
