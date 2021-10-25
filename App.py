import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import g
from pprint import pprint

from database import sql_insert_producto, sql_select_productos, sql_edit_productos, sql_delete_productos
from database import sql_select_proveedores, sql_insert_proveedores, sql_edit_proveedores, sql_delete_proveedores
from database import sql_select_usuarios, sql_insert_usuarios, sql_edit_usuarios, sql_delete_usuarios
from forms import Proveedores,Producto


App = Flask(__name__)
####### Connect to mysql ########
App.config['MYSQL_Host'] = 'localhost'
App.config['MYSQL_USER'] = 'root'
App.config['MYSQL_PASSWORD'] = ''
App.config['MYSQL_DB'] = 'dbhotai'

mysql = MySQL(App)
#####################################


App.secret_key = os.urandom(24)

#@App.route('/productos1') 
#def productos1(): 
  #form = Producto()
  #productos = sql_select_productos()
  #return render_template('productos1.html', productos = productos)

# @App.route('/nuevo', methods=['GET', 'POST'])
# def nuevo():
#    if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
# 	    form = Proveedores() #Crea un nuevo formulario de tipo Proveedores
# 	    return render_template('nuevo.html', form = form) #redirecciona vista nuevo.html enviando la variable form
#    if  request.method == "POST": #Si la ruta es accedida a través del método POST entonces
#         id_proveedores = request.form["id_proveedores"] #asigna variable cod con valor enviado desde formulario  en la vista html
#         nombre = request.form["nombre"] #asigna variable nom con valor enviado desde formulario en la vista html
#         categoria = request.form["categoria"] #asigna vble cant con valor enviado desde formulario en la vista html
#         ciudad = request.form["ciudad"] #asigna vble cant con valor enviado desde formulario en la vista html
#         direccion = request.form["direccion"] #asigna vble cant con valor enviado desde formulario en la vista html
#         telefono = request.form["telefono"] #asigna vble cant con valor enviado desde formulario en la vista html       sql_insert_proveedores(cod, nom, cant, precio) #llamado de la función para insertar el nuevo producto
#         sql_insert_proveedores(id_proveedores, nombre, categoria, ciudad, direccion, telefono) #llamado de la función para insertar el nuevo producto
#         return 'OK'

@App.route('/', methods=["GET","POST"])
def Home():
    return render_template('home.html')

@App.route('/Inicio', methods=["GET","POST"])
def Inicio():
    g.nombre = request.form.get("nombre")
    return render_template('inicio.html', nombre=g.nombre)

###################################################################
#### Index ruta usuarios + obtención de datos de  mysql #########
####################################################################
@App.route('/Usuarios')
def Usuario():
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT * FROM usuarios  ')
    user = cursor.fetchall()
    cursor.close()
    return render_template('usuario.html', user = user)
#########################################################


#########################################################
#  -----------Metodo de creación de usuarios -----------#
#########################################################
@App.route('/Usuarios', methods=["POST"])
def Usuario_add():
    #Datos de formulario 
    nombre = request.form['name']
    mail = request.form['email']
    perfil = request.form['profile']
    usuario = request.form['user']
    passw = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios(nombre, mail, perfil, usuario, passw) VALUES (%s, %s, %s, %s, %s)", (nombre, mail, perfil, usuario, passw))

    mysql.connection.commit()
    cursor.close()
    # Mensaje de creación de usuario 
    flash('Usuario añadido correctamente')
    #redirecion ruta
    return redirect(url_for('Usuario'))
#########################################################


#############################################################
#------------ Metodo de eliminiación de usuaro ------------#
############################################################
@App.route('/Usuario/delete/<string:id>', methods=["GET", "POST"])
def delete_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('Usuario'))
###########################################################


###########################################################
#-------------Metodo actualizar de usuario -------------- #
###########################################################
@App.route('/Usuario/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['name']
        mail = request.form['email']
        perfil = request.form['profile']
        usuario = request.form['user']
        passw = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE usuarios SET nombre = %s, mail = %s, perfil = %s, usuario = %s, passw = %s WHERE id = %s """, (nombre, mail, perfil, usuario, passw, id))
        flash('Usuario actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('Usuario'))
#######################################################



@App.route('/Productos', methods=["GET", "POST"])
def Productos():
    return render_template('productos.html')

@App.route('/Proveedores', methods=["GET", "POST"])
def Proveedores():
    return render_template('proveedores.html')

@App.errorhandler(404)
def not_found(error):
        return "La página no existe"

if __name__ == '__main__':
    App.run(debug = True)
