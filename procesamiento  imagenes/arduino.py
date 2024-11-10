import serial
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import sys
import pyqtgraph as pg

arduino = serial.Serial(port='COM3', baudrate=9600)

class QLabelBuddy(QDialog):
    def __init__(self):
        super().__init__()
        self.temp_data = []
        self.plot_widget = pg.PlotWidget()
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizarTemperatura)
        self.timer.start(3000)  # Actualizar temperatura cada 3 segundos

    def initUI(self):
        self.setWindowTitle('UART')
        self.setFixedWidth(450)
        self.setFixedHeight(400)

        font = QFont("Arial", 12)

        nameLabel = QLabel('Salida: ', self)
        self.nameLineEdit = QLineEdit(self)
        nameLabel.setBuddy(self.nameLineEdit)
        nameLabel.setFont(font)
        self.nameLineEdit.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border: 2px solid lightgray;
            border-radius: 5px;
            padding: 7px 5px
        }
        """)

        tempLabel = QLabel('Temperatura:', self)
        self.tempLineEdit = QLineEdit()
        self.tempLineEdit.setReadOnly(True)
        tempLabel.setBuddy(self.tempLineEdit)
        tempLabel.setFont(font)
        self.tempLineEdit.setStyleSheet("""
        QLineEdit {
            background-color: transparent;
            border: none;
        }
        """)

        btnOK = QPushButton('&OK')
        btnOK.clicked.connect(self.enviarTextoArduino)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLineEdit, 0, 1, 1, 2)
        mainLayout.addWidget(tempLabel, 1, 0)
        mainLayout.addWidget(self.tempLineEdit, 1, 1, 1, 2)
        mainLayout.addWidget(btnOK, 2, 1)
        mainLayout.addWidget(self.plot_widget, 3, 0, 1, 3)

    def enviarTexto(self, texto):
        arduino.write(bytes(texto + '\n', 'utf-8'))

    def enviarTextoArduino(self):
        texto = self.nameLineEdit.text()
        self.enviarTexto(texto)

    def leerTemperatura(self):
        arduino.write(b'T')
        temp = arduino.readline().decode().strip()
        self.temp_data.append(float(temp))
        return temp

    def actualizarTemperatura(self):
        temp = self.leerTemperatura()
        self.tempLineEdit.setText(temp)
        self.plot_widget.plot(self.temp_data, pen='r', symbol='o', symbolPen='b', symbolSize=5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QLabelBuddy()
    main.show()
    sys.exit(app.exec_())



