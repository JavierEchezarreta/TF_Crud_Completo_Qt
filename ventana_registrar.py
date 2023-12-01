from PySide6.QtWidgets import *
from conectar_db import *

class VentanaRegistrar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Registro de Alumnos")
        self.setGeometry(800, 300, 300, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Etiquetas y campos de entrada
        self.label_nombre = QLabel("Nombre:")
        self.entry_nombre = QLineEdit()

        self.label_apellido = QLabel("Apellido:")
        self.entry_apellido = QLineEdit()

        self.label_dni = QLabel("DNI:")
        self.entry_dni = QLineEdit()

        layout.addWidget(self.label_nombre)
        layout.addWidget(self.entry_nombre)
        layout.addWidget(self.label_apellido)
        layout.addWidget(self.entry_apellido)
        layout.addWidget(self.label_dni)
        layout.addWidget(self.entry_dni)

        # Botones
        self.boton_registrar = QPushButton("Registrar")
        self.boton_registrar.clicked.connect(self.registrar_alumno)

        self.boton_volver = QPushButton("Cerrar")
        self.boton_volver.clicked.connect(self.close)


        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.boton_registrar)
        botones_layout.addWidget(self.boton_volver)

        layout.addLayout(botones_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def registrar_alumno(self):
        try:
            nombre = self.entry_nombre.text()
            apellido = self.entry_apellido.text()
            dni = self.entry_dni.text()
            # Valida que los campos nombre y alumno sólo contengan letras
            if nombre.isalpha() and apellido.isalpha():
                 nombre = self.entry_nombre.text()
                 apellido = self.entry_apellido.text()
            else:
                 self.notificacion_error()
                 return
            
            conexion = conectar_db()
            cursor = conexion.cursor()
            consulta = "USE trabajo_final"
            cursor.execute(consulta)
            consulta = "INSERT INTO alumnos (nombre, apellido, dni) VALUES (%s, %s, %s)"
            valores = (nombre, apellido, dni)


            # Ejecutar la consulta
            cursor.execute(consulta, valores)

            # Confirmar la transacción
            conexion.commit()

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            #limpia los campos luego del registro
            self.entry_nombre.clear()
            self.entry_dni.clear()
            self.entry_apellido.clear()

            #notifica el correcto ingreso de datos
            self.notificacion_exitosa()

        except:
            self.notificacion_error()


    def notificacion_exitosa(self):
            #mensaje de alerta de notificacion exitosa
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setWindowTitle("Advertencia")
            mensaje.setText("Datos registrados correctamente.")
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