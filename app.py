from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configurar la conexión a la base de datos
mydb = mysql.connector.connect(
    user='root', 
    password='',
    host='localhost',
    database='inventario')

# Rutas de la aplicación
@app.route('/')
def index():
    # Obtener todos los productos de la base de datos
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM producto")
    productos = mycursor.fetchall()
    print(productos)
    return render_template('index.html', productos=productos)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        # Obtener los datos del formulario de creación de producto
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        # Crear el producto en la base de datos
        mycursor = mydb.cursor()
        sql = "INSERT INTO producto (nombre, descripcion, precio) VALUES (%s, %s, %s)"
        val = (nombre, descripcion, precio)
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirigir al usuario a la página principal
        return redirect('/')
    else:
        # Mostrar el formulario de creación de producto
        return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        # Obtener los datos del formulario de edición de producto
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        # Actualizar el producto en la base de datos
        mycursor = mydb.cursor()
        sql = "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s"
        val = (nombre, descripcion, precio, id)
        mycursor.execute(sql, val)
        mydb.commit()

        # Redirigir al usuario a la página principal
        return redirect('/')
    else:
        # Obtener el producto a editar de la base de datos
        mycursor = mydb.cursor()
        sql = "SELECT * FROM producto WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        producto = mycursor.fetchone()

        # Mostrar el formulario de edición de producto
        return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Eliminar el producto de la base de datos
    mycursor = mydb.cursor()
    sql = "DELETE FROM producto WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()

    # Redirigir al usuario a la página principal
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
