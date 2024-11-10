from matplotlib.pyplot import show as Show
from matplotlib.pyplot import subplots as Subplots
from matplotlib.pyplot import tight_layout as TightLayout
from matplotlib.pyplot import axes as Axes
from matplotlib.widgets import Button
from time import time as Time
from serial import Serial
import threading

"""CONSTANTS"""

PORT = "COM3"
BAUD_RATE = 9600

TIME_POINTS_BTW_DATA = 10

"""TEMPERATURE & HUMIDITY GRAPH CLASS"""

class THGraph():
  def __init__(self):
    self.humidity = 0
    self.max_humidity = 70
    self.min_humidity = 30

    self.temperature = 0
    self.max_temperature = 33
    self.min_temperature = 20

    self.__time_data = []
    self.__temp_data = []
    self.__hum_data = []

    self.__setup_graph()
    self.__setup_min_max_buttons()

  def update_graphs(self, temp, max_temp, min_temp, hum, max_hum, min_hum):
    current_time = Time()

    self.temperature = temp
    self.max_temperature = max_temp
    self.min_temperature = min_temp
    self.humidity = hum
    self.max_humidity = max_hum
    self.min_humidity = min_hum

    self.__time_data.append(current_time)
    self.__temp_data.append(self.temperature)
    self.__hum_data.append(self.humidity)

    self.__ax_temp.set_title(f"Temperature (°C), Max: {self.max_temperature}°C, Min: {self.min_temperature}°C")

    self.__temp_line.set_data(self.__time_data, self.__temp_data)
    self.__temp_max_line.set_data(self.__time_data, [self.max_temperature] * len(self.__time_data))
    self.__temp_min_line.set_data(self.__time_data, [self.min_temperature] * len(self.__time_data))
    self.__ax_temp.relim()
    self.__ax_temp.autoscale_view(True, True, True)

    self.__hum_line.set_data(self.__time_data, self.__hum_data)
    self.__hum_max_line.set_data(self.__time_data, [self.max_humidity] * len(self.__time_data))
    self.__hum_min_line.set_data(self.__time_data, [self.min_humidity] * len(self.__time_data))
    self.__ax_hum.relim()
    self.__ax_hum.autoscale_view(True, True, True)

    self.__check_alerts(current_time)

    self.__fig.canvas.draw_idle()

  
  def __check_alerts(self, current_time):
    # Remove existing annotations
    for artist in self.__ax_temp.texts:
      artist.remove()
    for artist in self.__ax_hum.texts:
      artist.remove()

    # Check for temperature alerts
    if self.temperature >= self.max_temperature:
        self.__ax_temp.text(current_time, self.temperature + 2, 
                             f'High Temp Alert: {self.temperature}°C', 
                             color='red', fontsize=10, fontweight='bold')
    elif self.temperature <= self.min_temperature:
        self.__ax_temp.text(current_time, self.temperature - 2, 
                             f'Low Temp Alert: {self.temperature}°C', 
                             color='blue', fontsize=10, fontweight='bold')

    # Check for humidity alerts
    if self.humidity >= self.max_humidity:
        self.__ax_hum.text(current_time, self.humidity + 2, 
                            f'High Humidity Alert: {self.humidity}%', 
                            color='red', fontsize=10, fontweight='bold')
    elif self.humidity <= self.min_humidity:
        self.__ax_hum.text(current_time, self.humidity - 2, 
                            f'Low Humidity Alert: {self.humidity}%', 
                            color='blue', fontsize=10, fontweight='bold')

  def __setup_graph(self):
    # Create a figure with two subplots
    self.__fig, (self.__ax_temp, self.__ax_hum) = Subplots(nrows=2, ncols=1, figsize=(8, 10))

    # Temperature subplot
    self.__ax_temp.set_xlabel('Time')
    self.__ax_temp.set_ylabel('Temperature (°C)')
    self.__temp_max_line, = self.__ax_temp.plot([], [], 'r--', label='Max Temperature')
    self.__temp_min_line, = self.__ax_temp.plot([], [], 'g--', label='Min Temperature')
    self.__temp_line, = self.__ax_temp.plot([], [], lw=2, label='Temperature')
    self.__ax_temp.legend()
    self.__ax_temp.set_title(f"Temperature Monitor, Max: {self.max_temperature}°C, Min: {self.min_temperature}°C")
    self.__ax_temp.grid(True)

    # Humidity subplot
    self.__ax_hum.set_xlabel('Time')
    self.__ax_hum.set_ylabel('Humidity (%)')
    self.__hum_max_line, = self.__ax_hum.plot([], [], 'r--', label='Max Humidity')
    self.__hum_min_line, = self.__ax_hum.plot([], [], 'g--', label='Min Humidity')
    self.__hum_line, = self.__ax_hum.plot([], [], lw=2, label='Humidity')
    self.__ax_hum.legend()
    self.__ax_hum.set_title('Humidity Monitor')
    self.__ax_hum.grid(True)


    self.__fig.tight_layout()

  def __setup_min_max_buttons(self):
    self.temp_max_btn = Button(Axes([0.01, 0.48, 0.08, 0.05]), 'Add Max', color='#EAEAEA', hovercolor='0.975')
    self.temp_min_btn = Button(Axes([0.1, 0.48, 0.08, 0.05]), 'Add Min', color='#EAEAEA', hovercolor='0.975')

    self.hum_max_btn = Button(Axes([0.1, 0.05, 0.1, 0.075]), 'rest Max', color='#EAEAEA', hovercolor='0.975')
    self.hum_min_btn = Button(Axes([0.2, 0.05, 0.1, 0.075]), 'rest Min', color='#EAEAEA', hovercolor='0.975')



  def run(self):
    Show()

if __name__ == "__main__":
  temp_hum_graph = THGraph()

  try:
    serial = Serial(PORT, BAUD_RATE)
  except Exception as e:
    print(f"Error: {e}")
    exit()

  def min_max_data(value, min_value, max_value):
    # percentage = ((value - min_value) / (max_value - min_value))
    percentage = ((max_value - value) / (max_value - min_value)) 

    if percentage < 0:
      percentage = 0
    elif percentage > 1:
      percentage = 1

    return percentage * 10
  
  def add_max_temp(event):
    temp_hum_graph.max_temperature += 1
    if temp_hum_graph.max_temperature > 60:
      temp_hum_graph.max_temperature = 60
    
    print(f"Max Temp: {temp_hum_graph.max_temperature}")

  def add_min_temp(event):
    temp_hum_graph.min_temperature += 1
    if temp_hum_graph.min_temperature > 40:
      temp_hum_graph.min_temperature = 40
    
    print(f"Min Temp: {temp_hum_graph.min_temperature}")

  def add_max_hum(event):
    temp_hum_graph.max_temperature -= 1
    if temp_hum_graph.max_temperature < 0:
      temp_hum_graph.max_temperature = 70
    
    print(f"Max Hum: {temp_hum_graph.max_temperature}")

  def add_min_hum(event):
    temp_hum_graph.min_temperature -= 1
    if temp_hum_graph.min_temperature < 0:
      temp_hum_graph.min_temperature = 30
    
    print(f"Min Hum: {temp_hum_graph.min_temperature}")

  def get_output():
    while serial.is_open:
      data = serial.readline().decode().strip()
      data = data.split("/")

      # try:
      if len(data) == 2:
        temp, hum = data

        closest_temp = min_max_data(float(temp), float(temp_hum_graph.min_temperature), float(temp_hum_graph.max_temperature))
        brightness = str(int(closest_temp))

        serial.write(brightness.encode())
        print(f"Data Sent: {brightness}")
        
        temp_hum_graph.update_graphs(float(temp), float(temp_hum_graph.max_temperature), float(temp_hum_graph.min_temperature), 
                                     float(hum), float(temp_hum_graph.max_humidity), float(temp_hum_graph.min_humidity))
      # except Exception as e:
      else:
        print(f"Error. Data: {data}")

  input_thread = threading.Thread(target=get_output)
  input_thread.daemon = True
  input_thread.start()

  temp_hum_graph.temp_max_btn.on_clicked(add_max_temp)
  temp_hum_graph.temp_min_btn.on_clicked(add_min_temp)
  temp_hum_graph.hum_max_btn.on_clicked(add_max_hum)
  temp_hum_graph.hum_min_btn.on_clicked(add_min_hum)

  temp_hum_graph.run()
