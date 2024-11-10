import sys
import serial
import serial.tools.list_ports
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QLabel
import pyqtgraph as pg
import numpy as np


class SerialMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.serial_port = None
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

        self.pot_curve = self.plot_widget.plot(pen='g', name="Potentiometer")
        self.button_curve = self.plot_widget.plot(pen='r', name="Button")

        self.setLayout(self.layout)
        self.show()

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_selector.clear()
        for port in ports:
            self.port_selector.addItem(port.device)

    def start_acquisition(self):
        port_name = self.port_selector.currentText()
        try:
            self.serial_port = serial.Serial(port_name, 9600)
            self.timer.start(100)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except serial.SerialException as e:
            self.data_label.setText(f"Error al abrir el puerto serial: {e}")

    def stop_acquisition(self):
        self.timer.stop()
        if self.serial_port:
            self.serial_port.close()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def toggle_led(self):
        if self.serial_port:
            self.led_state = not self.led_state
            self.serial_port.write(b'1' if self.led_state else b'0')

    def update_data(self):
        if self.serial_port and self.serial_port.in_waiting > 0:
            line = self.serial_port.readline().decode('utf-8').strip()
            if line.startswith("POT:"):
                data = line.split(',')
                pot_value = int(data[0].split(':')[1])
                button_state = int(data[1].split(':')[1])
                self.data_label.setText(
                    f"Potenciometro: {pot_value}, Botón: {button_state}")

                # Actualizar las listas de datos
                self.pot_data.append(pot_value)
                self.button_data.append(button_state)

                # Mantener las listas de datos a un tamaño fijo
                if len(self.pot_data) > 100:
                    self.pot_data.pop(0)
                if len(self.button_data) > 100:
                    self.button_data.pop(0)

                # Actualizar las gráficas
                self.pot_curve.setData(self.pot_data)
                self.button_curve.setData(self.button_data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SerialMonitor()
    sys.exit(app.exec_())
