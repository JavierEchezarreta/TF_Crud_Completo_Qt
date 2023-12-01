from PySide6.QtWidgets import *
from conectar_db import *

class VentanaModificar(QMainWindow):

    def __init__(self, nombre, apellido, dni):
        super().__init__()

        self.setWindowTitle("Modificación de alumnos")
        self.setGeometry(800, 300, 300, 200)

        self.label_nombre = QLabel("Nombre:", self)
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setText(nombre)

        self.label_apellido = QLabel("Apellido:", self)
        self.input_apellido = QLineEdit(self)
        self.input_apellido.setText(apellido)

        self.label_dni = QLabel("Edad:", self)
        self.input_dni = QLineEdit(self)
        self.input_dni.setText(str(dni))

        self.boton_guardar = QPushButton("Guardar", self)
        self.boton_guardar.clicked.connect(self.guardar_datos)

        layout = QVBoxLayout()
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.label_apellido)
        layout.addWidget(self.input_apellido)
        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.boton_guardar)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Conecta la base de datos mysql
        self.conexion = conectar_db()
        # Ejecuta consulta MySql
        cursor = self.conexion.cursor()
        consulta = "USE trabajo_final"
        cursor.execute(consulta)
        consulta = "SELECT * FROM alumnos WHERE nombre = %s AND apellido = %s"
        valores = (nombre, apellido)
        cursor.execute(consulta, valores)
        id = cursor.fetchone()
        self.id = id[0]

    def guardar_datos(self):
        try:
            # Obtener los valores de los campos de entrada
            nombre = self.input_nombre.text()
            apellido = self.input_apellido.text()
            dni = self.input_dni.text()
            # Valida que los campos nombre y alumno sólo contengan letras
            if nombre.isalpha() and apellido.isalpha():
                 nombre = self.input_nombre.text()
                 apellido = self.input_apellido.text()
            else:
                 self.notificacion_error()
                 return

            # Actualizar los datos del alumno en la tabla "alumnos"
            cursor = self.conexion.cursor()
            consulta = "UPDATE alumnos SET nombre = %s, apellido = %s, dni = %s WHERE id = %s"
            valores = (nombre, apellido, dni, self.id)
            cursor.execute(consulta, valores)
            self.conexion.commit()

            # Noticacion Exitosa
            self.notificacion_exitosa()
        
            # Cerrar la conexión y cerrar la ventana actual
            cursor.close()
            self.conexion.close()
            self.close()

        except:
            self.notificacion_error()

    def notificacion_exitosa(self):
            #mensaje de alerta de notificacion exitosa
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setWindowTitle("Advertencia")
            mensaje.setText("Datos modificados correctamente.")
            mensaje.addButton(QMessageBox.Ok)
            mensaje.exec()

    def notificacion_error(self):
            #mensaje de alerta de notificacion exitosa
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setWindowTitle("Advertencia")
            mensaje.setText("Ocurrió un error, intente nuevamente.")
            mensaje.addButton(QMessageBox.Ok)
            mensaje.exec()