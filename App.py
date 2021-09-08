from flask import Flask, render_template, request, redirect, url_for, flash
#render para q reconozca las plantillas y el request para methpd, url_for para redirigir, flash muestra alerts
from flask_mysqldb import MySQL #para poder usar la bd

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #lo pongo xq necesita una clave para guardar la sesion, la q sea
#MYSQL connection
app.config['MYSQL_HOST'] = 'localhost' #configuramos la conexion mysql
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

@app.route("/")#Ruta de acceso
def index():
    cursor = mysql.connection.cursor() #da acceso al cursor de la bd para operar
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall() #obtiene los resultados #retorna una tupla
    return render_template('index.html', contacts = data) #retorna esa vista y le pasa la tupla con los datos

@app.route("/add_contact", methods=['POST'])#Ruta de acceso y metodo desde el form
def add_contact():
    if request.method == 'POST': #identifica si llega al metodo a traves del post del formulario
        fullname = request.form['fullname'] #lo recoge del input del formulario
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor() #da acceso al cursor de la bd para operar
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit() #confirma la operacion
        flash('Contact added successfully') #lo mostramos como un alert q recibe la vista
        return redirect(url_for('index'))#nombre del metodo al q redirecciona

@app.route("/edit/<string:id>")#Ruta de acceso q recibe el parametro id del formulario
def edit_contact(id): #Recibira el id 
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s',(id)) #%s xq es un string
    data = cursor.fetchall()#recuperamos el contacto
    print(data)#imprime tupla con listas((3, 'fffff', 'eeeee', 'fffff'),)
    print(data[0])#imprime la 1ª lista de la tupla (3, 'fffff', 'eeeee', 'fffff')
    return render_template('edit-contact.html', contact = data[0]) #le pasamos esa lista

@app.route("/delete/<string:id>")#Ruta q recibe el parametro id del formulario
def delete_contact(id): #lo recibe en la funcion desde la ruta
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id)) #formatea el id como un string
    mysql.connection.commit()
    flash('Contact deleted successfully') #lo pasa a la vista q recibe un get_flashed_messages()
    return redirect(url_for('index'))

@app.route("/update/<id>", methods=['POST'])#Recibe el parametro id del formulario, puedes especificar string
def update_contact(id):
    if request.method == 'POST': #identifica si llega al metodo a traves del post del formulario
        fullname = request.form['fullname'] #lo recoge del input del formulario
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor() #da acceso al cursor de la bd para operar
        cursor.execute("""UPDATE contacts SET fullname =%s, phone =%s, email =%s 
        WHERE id =%s""", (fullname, phone, email, id))#triple comilla para varias lineas
        mysql.connection.commit() #confirma la operacion
        flash('Contact updated successfully') #lo mostramos como un alert q recibe la vista
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug =True)#le podemos indicar el puerto, debug es para q se reinicie con los cambios
