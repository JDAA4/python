import sys
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QLabel
import pyqtgraph as pg
import bluetooth

class SerialMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bluetooth_socket = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.pot_data = []
        self.button_data = []

    def initUI(self):
        self.setWindowTitle('GUI')
        self.layout = QVBoxLayout()
        self.port_selector = QComboBox()
        self.refresh_ports()
        self.layout.addWidget(self.port_selector)

        self.start_button = QPushButton('Inicio')
        self.start_button.clicked.connect(self.start_acquisition)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Apagado')
        self.stop_button.clicked.connect(self.stop_acquisition)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.led_button = QPushButton('Encender LED')
        self.led_button.clicked.connect(self.toggle_led)
        self.led_state = False
        self.layout.addWidget(self.led_button)

        self.data_label = QLabel('Esperando datos...')
        self.layout.addWidget(self.data_label)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.pot_curve = self.plot_widget.plot(pen='g', name="Potenciometro")
        self.button_curve = self.plot_widget.plot(pen='r', name="Botón")

        self.setLayout(self.layout)
        self.show()

    def refresh_ports(self):
        # No es necesario en caso de Bluetooth, se deja por compatibilidad
        pass

    def start_acquisition(self):
        addr = self.port_selector.currentText()
        try:
            self.bluetooth_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.bluetooth_socket.connect((addr, 1))
            self.timer.start(100)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except bluetooth.BluetoothError as e:
            self.data_label.setText(f"Error al conectar por Bluetooth: {e}")

    def stop_acquisition(self):
        self.timer.stop()
        if self.bluetooth_socket:
            self.bluetooth_socket.close()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def toggle_led(self):
        if self.bluetooth_socket:
            self.led_state = not self.led_state
            self.bluetooth_socket.send(b'1' if self.led_state else b'0')

    def update_data(self):
        if self.bluetooth_socket:
            try:
                data = self.bluetooth_socket.recv(1024).decode().strip()
                if data.startswith("POT:"):
                    values = data.split(',')
                    pot_value = int(values[0].split(':')[1])
                    button_state = int(values[1].split(':')[1])
                    self.data_label.setText(
                        f"Potenciometro: {pot_value}, Botón: {button_state}")
                    self.pot_data.append(pot_value)
                    self.button_data.append(button_state)
                    if len(self.pot_data) > 100:
                        self.pot_data.pop(0)
                    if len(self.button_data) > 100:
                        self.button_data.pop(0)
                    self.pot_curve.setData(self.pot_data)
                    self.button_curve.setData(self.button_data)
            except bluetooth.BluetoothError as e:
                self.data_label.setText(f"Error en la comunicación Bluetooth: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SerialMonitor()
    sys.exit(app.exec_())

