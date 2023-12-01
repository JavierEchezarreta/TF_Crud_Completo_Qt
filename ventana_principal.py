from ventana_registrar import *
from ventana_modificar import *


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.filarow = ''

    def initUI(self):
        self.setWindowTitle("Gestión de Alumnos")
        self.setGeometry(800, 300, 335, 400)
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)

        # Configuración de la conexión a la base de datos
        self.conexion = conectar_db()

        # Crear un cursor
        cursor = self.conexion.cursor()

        # Crear una la base de datos si no existe
        consulta = "CREATE DATABASE IF NOT EXISTS trabajo_final"
        # Ejecuta la consulta
        cursor.execute(consulta)
        # Pone en uso la base de datos
        consulta = "use trabajo_final"
        # Ejecuta la consulta
        cursor.execute(consulta)
        # Crea la tabla alumnos si no existe
        consulta = "CREATE TABLE IF NOT EXISTS alumnos (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(50) NOT NULL, apellido VARCHAR(50) NOT NULL, dni VARCHAR(8) NOT NULL, CONSTRAINT longitud_campo CHECK (LENGTH(dni) >= 7 AND LENGTH(dni) <= 8));"
        # Ejecuta la consulta
        cursor.execute(consulta)
        
        # Selecciona los datos de la tabla alumnos
        consulta = "SELECT nombre, apellido, dni FROM alumnos" 
        cursor.execute(consulta)
        
        # Recupera todos los registros
        self.registros = cursor.fetchall()

        # Crea una tabla para mostrar los registros
        self.tabla_registros = QTableWidget(self)
        self.tabla_registros.setColumnCount(3)  # Columnas para Nombre, Apellido y Edad
        self.tabla_registros.setHorizontalHeaderLabels(["Nombre", "Apellido", "DNI",])

        # Método para agregar los registros en la ventana principal
        self.agregar_registros(self.registros,self.tabla_registros)

        # Agrega la tabla al diseño
        self.layout.addWidget(self.tabla_registros)


        # Botones
        self.boton_registrar = QPushButton("Registrar")
        self.boton_registrar.clicked.connect(self.registrar_alumno)
        self.layout.addWidget(self.boton_registrar)

        self.boton_modificar = QPushButton("Modificar")
        self.boton_modificar.clicked.connect(self.modificar_alumno)
        self.layout.addWidget(self.boton_modificar)

        self.boton_eliminar = QPushButton("Eliminar")
        self.boton_eliminar.clicked.connect(self.eliminar_alumno)
        self.layout.addWidget(self.boton_eliminar)

        # Funcionalidad de busqueda
        self.busqueda = QLabel()
        self.busqueda.setText('Buscar alumno por nombre')
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText('Ingresa el nombre')
        self.campo_busqueda.textChanged.connect(self.filtrar_alumnos)
        self.etiqueta_resultados = QLabel()
        self.layout.addWidget(self.busqueda)
        self.layout.addWidget(self.campo_busqueda)

        # Establece el diseño de la ventana principal de la aplicación. 
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Captura el dato de en que fila de la lista hace click el usuario
        self.tabla_registros.cellClicked.connect(self.obtener_datos_click)

    def obtener_datos_click(self, fila, columna):
        self.filarow = fila


    def agregar_registros(self, registros, tabla_registros):
         # Agregar filas con los registros
        tabla_registros.setRowCount(len(registros))
        for nombre, registro in enumerate(registros):
            for apellido, dato in enumerate(registro):
                dni = QTableWidgetItem(str(dato))
                tabla_registros.setItem(nombre, apellido, dni)

    def registrar_alumno(self):
        self.ventana_registrar = VentanaRegistrar()
        self.ventana_registrar.show()
        self.ventana_registrar.boton_registrar.clicked.connect(self.actualizar_registro)

    def modificar_alumno(self):
        id = self.filarow
        fila = self.registros[id]
        nombre = fila[0]
        apellido = fila[1]
        dni = fila[2]
        self.ventana_modificar = VentanaModificar(nombre, apellido, dni)
        self.ventana_modificar.show()
        self.ventana_modificar.boton_guardar.clicked.connect(self.actualizar_registro)

    def actualizar_registro(self):
        self.tabla_registros.setRowCount(0)
        conexion = conectar_db()
        cursor = conexion.cursor()
        consulta = "use trabajo_final"
        cursor.execute(consulta)
        consulta = "SELECT nombre, apellido, dni FROM alumnos" 
        cursor.execute(consulta)
        self.registros = cursor.fetchall()
        self.agregar_registros(self.registros, self.tabla_registros)

    def filtrar_alumnos(self, texto):
        # Filtra los alumnos según el input del campo de búsqueda
        for i in range(self.tabla_registros.rowCount()): 
            nombre = self.tabla_registros.item(i, 0).text()
            apellido = self.tabla_registros.item(i, 1).text()
            dni = self.tabla_registros.item(i, 2).text()
            if texto.lower() in apellido.lower() or texto.lower() in dni.lower() or texto.lower() in nombre.lower():
                self.tabla_registros.setRowHidden(i, False)  
            else:
                self.tabla_registros.setRowHidden(i, True) 


    def eliminar_alumno(self):
        # Se capturan los datos necesarios para la eliminacion 
        id = self.filarow
        fila = self.registros[id]
        nombre = str(fila[0])
        apellido = str(fila[1])
        valores = (nombre, apellido)
        # Se emite la consulta sql para la eliminacion
        cursor = self.conexion.cursor()
        consulta = "USE trabajo_final"
        cursor.execute(consulta)       
        consulta = "DELETE FROM alumnos WHERE nombre = %s AND apellido = %s"
        cursor.execute(consulta, valores)
        self.conexion.commit()
        cursor.close()
        self.actualizar_registro()
        # Mensaje de alerta de eliminacion exitosa
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Warning)
        mensaje.setWindowTitle("Advertencia")
        mensaje.setText("Alumno eliminado correctamente.")
        mensaje.addButton(QMessageBox.Ok)
        mensaje.exec()
