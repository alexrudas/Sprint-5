import os
from sqlite3.dbapi2 import Error
from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_mysqldb import MySQL
#from flask import g
#from pprint import pprint


from database import sql_insert_producto, sql_select_productos, sql_edit_productos, sql_delete_productos
from database import sql_select_proveedores, sql_insert_proveedores, sql_edit_proveedores, sql_delete_proveedores
from database import sql_select_usuarios, sql_insert_usuarios, sql_edit_usuarios, sql_delete_usuarios, sql_connection
from forms import Usuarios, Proveedores,Producto

App = Flask(__name__)
App.secret_key = os.urandom(24)

####### Connect to mysql ########
#App.config['MYSQL_Host'] = 'localhost'
#App.config['MYSQL_USER'] = 'root'
#App.config['MYSQL_PASSWORD'] = ''
#App.config['MYSQL_DB'] = 'dbhotai'

#mysql = MySQL(App)
#####################################




@App.route('/', methods=["GET","POST"])
def Login():
    return render_template('login.html')

@App.route('/Inicio', methods=["GET","POST"])
def Inicio():   
    return render_template('inicio.html')

    

############################################# INICO RUTA Y CRUD DE USUARIOS ###################################################
###################################################################
#### Index RUTA usuarios + obtención de datos de SQL #########

@App.route('/Usuarios', methods=['GET', 'POST']) 
def Usuario(): 
  #form=Usuarios()
  user = sql_select_usuarios()
  return render_template('usuario.html', user = user)
#########################################################


#########################################################
#  -----------Metodo de CREAR de usuarios -----------#
# en revisión
@App.route('/Insertar/Usuarios', methods=["POST"])
def Usuario_add():
    print ('insertando')
    try:
        #Datos de formulario 
        nombre = request.form['name']   #asigna variable cod con valor enviado desde formulario  en la vista html
        mail = request.form['email']
        perfil = request.form['profile']
        usuario = request.form['user']
        passw = request.form['password']

        sql_insert_usuarios(nombre, mail, perfil, usuario, passw) #llamado de la función para insertar el nuevo producto
        
        # Mensaje de creación de usuario 
        flash('Usuario añadido correctamente')
        #redirecion ruta
        return redirect(url_for('Usuario'))

    except Error as err:
        print (err)
#########################################################


###########################################################
#-------------Metodo EDITAR de usuario -------------- #

@App.route('/Usuario/update', methods=['POST'])
def editar_usuario():
    id = request.form ['id']
    nombre = request.form['name']
    mail = request.form['email']
    perfil = request.form['profile']
    usuario = request.form['user']
    passw = request.form['password']        
    sql_edit_usuarios(id,nombre, mail, perfil, usuario, passw) #llamado de la función de edición de la base de datos

    flash('Usuario actualizado correctamente')
    return redirect(url_for('Usuario'))
#######################################################


#############################################################
#------------ Metodo ELIMINAR de usuaro ------------#

@App.route('/Usuario/delete/<id>', methods=["GET", "POST"])
def delete_usuario(id=None):
    sql_delete_usuarios(id) #llamado a la función de borrado de la base de datos
    flash('Usuario eliminado correctamente')
    return redirect(url_for('Usuario'))
#########################################################
############################################# FIN MÉTODOS Y RUTA DE USUARIOS #############################################################################
# #####



############################################# INICO MÉTODOS Y RUTA DE PROVEEDORES ###################################################

###################################################################
#### Index ruta proveedores + obtención de datos de  mysql #########
####################################################################
@App.route('/Proveedores')
def Proveedores():
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT * FROM Proveedores  ')
    supplier = cursor.fetchall()
    cursor.close()
    return render_template('proveedores.html', supplier = supplier)
#########################################################


#########################################################
#  -----------Metodo de creación de proveedores -----------#
#########################################################
@App.route('/Proveedores', methods=["POST"])
def Proveedores_add():
    #Datos de formulario 
    nombre = request.form['name']
    categoria = request.form['category']
    ciudad = request.form['city']
    direccion = request.form['address']
    telefono = request.form['phone']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO proveedores(nombre, categoria, ciudad, direccion, telefono) VALUES (%s, %s, %s, %s, %s)", (nombre, categoria, ciudad, direccion, telefono))

    mysql.connection.commit()
    cursor.close()
    # Mensaje de creación de proveedor
    flash('Proveedor añadido correctamente')
    #redirecion ruta
    return redirect(url_for('Proveedores'))
#########################################################


###########################################################
#-------------Metodo Actualizar (Editar)de Proveedor -------------- #
###########################################################
@App.route('/Proveedores/update/<id>', methods=['POST'])
def update_proveedort(id):
    if request.method == 'POST':
        #Datos de formulario 
        nombre = request.form['name']
        categoria = request.form['category']
        ciudad = request.form['city']
        direccion = request.form['address']
        telefono = request.form['phone']

        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE proveedores SET nombre = %s, categoria = %s, ciudad = %s, direccion = %s, telefono = %s WHERE id_proveedores = %s """, (nombre, categoria, ciudad, direccion, telefono,id))

        flash('Proveedor actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('Proveedores'))
#######################################################

#############################################################
#------------ Metodo de eliminiación de proveedores ------------#
############################################################
@App.route('/Proveedores/delete/<string:id>', methods=["GET", "POST"])
def delete_proveedores(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id_proveedores = {0}'.format(id))
    mysql.connection.commit()
    flash('Proveedor eliminado correctamente')
    return redirect(url_for('Proveedores'))
###########################################################

############################################# FIN MÉTODOS Y RUTA DE PROVEEDORES ###################################################




############################################# INICO MÉTODOS Y RUTA DE PRODUCTOS ###################################################

###################################################################
#### Index ruta productos + obtención de datos de  mysql #########
####################################################################
@App.route('/Productos')
def Productos():
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT * FROM productos')
    products = cursor.fetchall()
    cursor.close()
    return render_template('productos.html', products = products)
#########################################################


#########################################################
#  -----------Metodo de creación de productos ----------#
#########################################################
@App.route('/Productos', methods=["POST"])
def Productos_add():
    #Datos de formulario
    nombre = request.form['name']
    marca = request.form['brand']
    descripcion = request.form['description']
    categoria = request.form['category']
    cantidad = request.form['quantity']
    costo = request.form['cost']
    id_proveedores = request.form['id_supplier']
    print(nombre, marca, descripcion, categoria, cantidad, costo,id_proveedores)
   
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO productos(nombre, marca, descripcion, categoria, cantidad, costo,id_proveedores) VALUES (%s, %s, %s, %s, %s, %s, %s )", (nombre, marca, descripcion, categoria, cantidad, costo, id_proveedores))

    mysql.connection.commit()
    cursor.close()
    # Mensaje de creación de proveedor
    flash('Producto añadido correctamente')
    #redirecion ruta
    return redirect(url_for('Productos'))
#########################################################


###########################################################
#-------------Metodo Actualizar (Editar)de Productos ------- #
###########################################################
@App.route('/Productos/update/<id>', methods=['POST'])
def update_produto(id):
    if request.method == 'POST':
        nombre = request.form['name']
        marca = request.form['brand']
        descripcion = request.form['description']
        categoria = request.form['category']
        cantidad = request.form['quantity']
        costo = request.form['cost']
      


        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE productos SET nombre = %s, marca = %s, descripcion = %s, categoria = %s, cantidad = %s, costo = %s WHERE id_producto = %s """, (nombre, marca, descripcion, categoria, cantidad, costo, id))

        flash('Producto actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('Productos'))
#######################################################

#############################################################
#------------ Metodo de eliminiación de PRODUCTOS ------------#
############################################################
@App.route('/Productos/delete/<string:id>', methods=["GET", "POST"])
def delete_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('Productos'))
###########################################################







@App.errorhandler(404)
def not_found(error):
        return "La página no existe"

if __name__ == '__main__':
    App.run(debug = True)
