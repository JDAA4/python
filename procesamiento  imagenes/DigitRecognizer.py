import numpy as np
from PIL import Image, ImageDraw 
from tkinter import Canvas, Button, Label

class DigitRecognizer:
    def __init__(self, master, network):
        self.master = master
        self.master.title("Prediccion de digitos")

        self.network = network

        self.canvas = Canvas(master, width=280, height=280, bg="white")
        self.canvas.grid(row=0, columnspan=2)

        self.label = Label(master, text="Dubuja un digito")
        self.label.grid(row=1, columnspan=2)

        self.predict_button = Button(master, text="Predecir", command=self.predict_digit)
        self.predict_button.grid(row=2, column=0)

        self.clear_button = Button(master, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=2, column=1)

        self.image = Image.new("L", (280, 280), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.draw_digit)

    def draw_digit(self, event):
        x, y = event.x, event.y
        r = 8
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image.paste(255, box=(0, 0, 280, 280))
        self.draw = ImageDraw.Draw(self.image)

    def predict_digit(self):
        scaled_image = self.image.resize((28, 28))
        image_array = np.array(scaled_image).reshape((784, 1)) / 255.0
        prediction = self.network.feedforward(image_array)
        digit_prediction = np.argmax(prediction)
        self.label.config(text=f"Prediccion: {digit_prediction}")