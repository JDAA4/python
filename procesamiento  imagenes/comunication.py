import serial
import serial.tools.list_ports  # Permite reconocer puertos
from threading import Thread, Event  # Crear subprocesos
from tkinter import StringVar  # Recibir datos de arduino en string


# Código para la comunicación serial
class Comunicacion():
    # Método constructor
    def __init__(self, *args):
        self.datos_recibidos = StringVar()  # Variable para almacenar datos recibidos

        self.arduino = serial.Serial()  # Objeto para comunicación serial
        self.arduino.port = 'COM3'  # Cambiar al puerto COM3 donde está conectado tu Arduino
        self.arduino.timeout = 0.5  # Tiempo de espera para lectura

        self.senial = Event()  # Evento para controlar el hilo de lectura
        self.hilo = None  # Hilo de lectura

    def conexion_serial(self):
        try:
            self.arduino.open()  # Intentar abrir el puerto serial
        except Exception as e:
            print(f'Error al conectar al puerto COM3: {str(e)}')
            return
        
        if self.arduino.is_open:
            self.iniciar_hilo()  # Iniciar el hilo para leer datos
            print('Conectado al puerto COM3')

    def enviar_datos(self, data):
        try:
            if self.arduino.is_open:
                self.datos = str(data) + "\n"
                self.arduino.write(self.datos.encode())  # Enviar datos al Arduino
            else:
                print('Error: Puerto serie no abierto')
        except Exception as e:
            print('Error al enviar datos:', str(e))

    def leer_datos(self):
        try:
            while self.senial.isSet() and self.arduino.is_open:
                data = self.arduino.readline().decode("utf-8").strip()  # Leer datos del Arduino
                if len(data) > 1:
                    self.datos_recibidos.set(data)  # Actualizar la variable con los datos recibidos
        except Exception as e:
            print('Error al leer datos:', str(e))

    def iniciar_hilo(self):
        # Crear y comenzar el hilo para la lectura de datos
        self.hilo = Thread(target=self.leer_datos)
        self.hilo.setDaemon(True)  # Establecer como demonio para que se cierre con la aplicación principal
        self.senial.set()  # Activar la señal para iniciar la lectura
        self.hilo.start()  # Iniciar el hilo

    def stop_hilo(self):
        # Detener el hilo de lectura
        if self.hilo is not None:
            self.senial.clear()  # Limpiar la señal para detener el hilo
            self.hilo.join()  # Esperar a que el hilo termine
            self.hilo = None  # Reiniciar el hilo a None

    def desconectar(self):
        # Cerrar el puerto serial y detener el hilo
        if self.arduino.is_open:
            self.arduino.close()  # Cerrar el puerto serial
            print('Desconectado del puerto COM3')
        self.stop_hilo()  # Detener el hilo de lectura


# Ejemplo de uso
if __name__ == "__main__":
    # Crear objeto de comunicación
    comunicacion = Comunicacion()

    # Conectar al puerto COM3
    comunicacion.conexion_serial()

    try:
        # Ejemplo de envío de datos al Arduino
        comunicacion.enviar_datos("Hello Arduino!")

        # Ejemplo de lectura de datos recibidos del Arduino
        while True:
            print("Datos recibidos:", comunicacion.datos_recibidos.get())
    except KeyboardInterrupt:
        pass
    finally:
        # Desconectar al finalizar
        comunicacion.desconectar()
