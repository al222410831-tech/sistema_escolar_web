from flask import Flask, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "123"

# conexión local (luego será Atlas)
client = MongoClient("mongodb://localhost:27017/")
db = client["proyecto2"]

usuarios = db["usuarios"]
materias = db["materias"]
calificaciones = db["calificaciones"]
reportes = db["reportes"]

# INICIO
@app.route("/")
def inicio():
    return """
    <h1>Sistema Escolar</h1>

    <a href='/registro'>Registro</a><br>
    <a href='/login'>Login</a>
    """

# REGISTRO
@app.route("/registro", methods=["GET","POST"])
def registro():

    if request.method == "POST":

        matricula = request.form["matricula"]
        nombre = request.form["nombre"]
        password = request.form["password"]
        rol = request.form["rol"]

        usuarios.insert_one({
            "matricula": matricula,
            "nombre": nombre,
            "password": password,
            "rol": rol
        })

        return "Usuario registrado"

    return """
    <h2>Registro</h2>

    <form method='post'>

    Matricula:
    <input name='matricula'><br>

    Nombre:
    <input name='nombre'><br>

    Password:
    <input name='password'><br>

    Rol:
    <select name='rol'>
        <option value='alumno'>Alumno</option>
        <option value='maestro'>Maestro</option>
    </select>

    <button>Registrar</button>

    </form>
    """

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        matricula = request.form["matricula"]
        password = request.form["password"]

        user = usuarios.find_one({"matricula": matricula})

        if user and user["password"] == password:

            session["matricula"] = matricula
            session["rol"] = user["rol"]

            return redirect("/menu")

        return "Error login"

    return """
    <h2>Login</h2>

    <form method='post'>

    Matricula:
    <input name='matricula'><br>

    Password:
    <input name='password'><br>

    <button>Entrar</button>

    </form>
    """

# MENU
@app.route("/menu")
def menu():

    if "rol" not in session:
        return redirect("/")

    if session["rol"] == "alumno":

        return """
        <h1>Menu Alumno</h1>

        <a href='/ver_calificaciones'>Ver Calificaciones</a><br>
        <a href='/ver_reportes'>Ver Reportes</a>
        """

    else:

        return """
        <h1>Menu Maestro</h1>

        <a href='/poner_calificacion'>Poner Calificacion</a><br>
        <a href='/poner_reporte'>Poner Reporte</a>
        """

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)