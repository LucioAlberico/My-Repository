import imp
from flask import Flask, redirect
from flask import render_template, request, url_for, flash
from flaskext.mysql import MySQL

# para accedr al directorio
from flask import send_from_directory

# el envio de info es el request
# para q las fotos no se superpongan y cambien de nombre

from datetime import datetime
import os


app = Flask(__name__)
# info q se envia
# se usa para mantener la secion del cliente segura, esto se tendri aque cambiar a algo mas complejo
app.secret_key = "Develoteca"


mysql = MySQL()
# tiene q estar todo en mayuscula
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "basededatos_usuarios"
mysql.init_app(app)

# camino hacia un derectorio
CARPERTA = os.path.join("uploads")
app.config["CARPETA"] = CARPERTA


# sirve para mostrar la foto , se utiliza en edit
@app.route("/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config["CARPETA"], nombreFoto)


@app.route("/")
def index():
    # inserta la info
    sql = "SELECT * FROM `informe`;"
    # genera la coneccion
    conn = mysql.connect()
    # lugar donde se va a almacenar info
    cursor = conn.cursor()
    cursor.execute(sql)
    # busca toda la info y la imprime
    empleados = cursor.fetchall()
    print(empleados)
    # commi significa el final de uns transacion exitosa
    conn.commit()
    return render_template("empleados/index.html", empleados=empleados)


@app.route("/destroy/<int:id>")
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    # borra la foto de la carpeta
    cursor.execute("SELECT foto FROM informe WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config["CARPETA"], fila[0][0]))

    # hace el borrado de datos
    cursor.execute("DELETE FROM informe WHERE id=%s", (id))
    conn.commit()
    # vuelve de donde vino
    return redirect("/")


@app.route("/edit/<int:id>")
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM informe WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()
    # va a mostrar la pamtalla de edit
    return render_template("empleados/edit.html", empleados=empleados)


# conecta create con el archivo principal
@app.route("/update", methods=["POST"])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    id = request.form["txtID"]
    # en el caso q el usuario no elija cambiar la foto
    sql = "UPDATE informe SET nombre=%s, correo= %s WHERE id= %s;"

    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    # la fecha se adjunta a la foto asi no hay una incopabilidad en el guardado
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "":
        nuevoNombreFoto = tiempo + _foto.filename
        # guarda la foto en el archivo uploads
        _foto.save("uploads/" + nuevoNombreFoto)

        # remplaza la foto
        cursor.execute("SELECT foto FROM informe WHERE id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config["CARPETA"], fila[0][0]))
        cursor.execute("UPDATE informe SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()

    cursor.execute(sql, datos)

    conn.commit()
    # te retorna al archivo anterior/pagina
    return redirect("/")


# routa para la creacion de un empleado


@app.route("/create")
def create():
    return render_template("empleados/create.html")


# el guardado de los datos una vez que se crea el empleado


@app.route("/store", methods=["POST"])
def storage():
    # version con valores no fijos, no como los de arriba
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    # se diferencia y se usa file
    _foto = request.files["txtFoto"]

    # lo re direciona a create si no se rellena algun campo
    if _nombre == "" or _correo == "" or _foto == "":
        # feedback cuando no se completan los datos adecuadamente
        flash("Recuerda llenar los datos de los campos")
        # te manda a create para que los rellenes bienn
        return redirect(url_for("create"))

    # subimos la foto con el fotmato de foto
    now = datetime.now()
    # si no esta vacio tenemos el nombre de tiempo y se lo une a al nombre dado
    # se sube a carpeta uploads
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "":
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `informe` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
