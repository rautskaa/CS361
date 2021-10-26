from tkinter import Label, Text, END, Image
import PIL
from PIL import ImageTk, Image

class Images:

    def show_logo(self, frame):
        logo = PIL.Image.open("logo.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, padx=250)

    def resize_image(self, image):
        width, height = int(image.size[0]), int(image.size[1])
        if width > height:
            height = int(300 / width * height)
            width = 300
        elif height > width:
            width = int(250 / height * width)
            height = 250
        else:
            width, height = 250, 250
        image = image.resize((width, height))
        return image

    def show_image(self, frame, image):
        image = Image.open(image)
        image = self.resize_image(image)
        image = ImageTk.PhotoImage(image=image)
        img_label = Label(frame, image=image, bg="white")
        img_label.image = image
        img_label.grid(row=4, column=0, padx=170)
        return img_label

    def display_text_box(self, frame):
        text_box = Text(frame, height=5, width=25, padx=15, pady=15, bg="#22bfc5")
        text_box.tag_configure("center", justify="center")
        text_box.grid(column=0, row=6)
        return text_box

    def remove_metadata(self, undo, text):
        print("hello from remove")
        undo.set("Undone")
        text.delete('1.0', END)
        text.insert('1.0', "All metadata is now removed")