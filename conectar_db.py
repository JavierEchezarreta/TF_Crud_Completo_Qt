import mysql.connector

# Configuración de la conexión a la base de datos

def conectar_db():
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password='')
    return conexion