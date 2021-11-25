import json
import os
from tkinter import Label, Image, Button, END
import PIL
from PIL import ImageTk, Image
import requests


class ImagesProcessing:

    def __init__(self, frame):
        self.frame = frame

    def show_logo(self, frame, main_page):
        """Shows logo."""
        logo = PIL.Image.open("logo.png")
        logo = ImageTk.PhotoImage(logo)
        # If it's a main page, attach it to a main frame
        if main_page:
            res_frame = self.frame
        # If it's About or Help page, attach it to a corresponding frame
        else:
            res_frame = frame
        logo_label = Label(res_frame, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, padx=250)

    def show_icon(self, image, sticky):
        """Shows icon
        :param image
        :param sticky
        :return label icon"""
        icon = Image.open(image)
        icon = icon.resize((20, 20))
        icon = ImageTk.PhotoImage(icon)
        icon_label = Button(self.frame, image=icon, width=25, height=25)
        icon_label.image = icon
        icon_label.grid(column=0, row=5, sticky=sticky, padx=240)
        return icon_label

    def resize_image(self, image):
        """Resizes image
        :param image to resize
        :return resized image"""
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

    def show_image(self, image):
        """Show image
         :param image
         :return label of image"""
        image = Image.open(image)
        image = self.resize_image(image)
        image = ImageTk.PhotoImage(image=image)
        img_label = Label(self.frame, image=image, bg="white")
        img_label.image = image
        img_label.grid(row=4, column=0, padx=170)
        return img_label

    def next_images(self, images, index_to_show, image_index, shown_image, text_box):
        """Shows next image in the set of selected images.
          :param images
          :param index_to_show
          :param image_index
          :param shown_image
          :param text_box"""
        # If there are images left, show the image
        if image_index[-1] < len(images) - 1:
            updated_index = image_index[-1] + 1
            image = self.update_image_to_view(images, updated_index, index_to_show, image_index, shown_image)
            # clear all data and update the text box with the metadata description for next image
            self.update_text_box(text_box, image)

    def previous_images(self, images, index_to_show, image_index, shown_image, text_box):
        """Shows previous image in the set of selected images.
          :param images
          :param index_to_show
          :param image_index
          :param shown_image
          :param text_box"""
        if image_index[-1] >= 1:
            updated_index = image_index[-1] - 1
            image = self.update_image_to_view(images, updated_index, index_to_show, image_index, shown_image)
            # clear all data and update the text box with the metadata description for previous image
            self.update_text_box(text_box, image)

    def set_index_to_show(self, images, image_index, index_to_show):
        """Updates index of displayed images.
          :param images
          :param image_index
          :param index_to_show"""
        index_to_show.set("Image " + str(image_index[-1] + 1) + " out of " + str(len(images)))

    def update_image_to_view(self, images, updated_index, index_to_show, image_index, shown_image):
        """Updates image to show.
           :param images
           :param updated_index
           :param index_to_show
           :param image_index
           :param shown_image
           :return new image"""
        image_index.pop()
        image_index.append(updated_index)
        if shown_image:
            shown_image[-1].grid_forget()
            shown_image.pop()
        new_image = images[image_index[-1]]
        current_image = self.show_image(new_image)
        shown_image.append(current_image)
        self.set_index_to_show(images, image_index, index_to_show)
        return new_image

    def update_text_box(self, text_box, image):
        """Updates image description in text box.
           :param text_box
           :param image_description
        """
        image_name = os.path.basename(image)
        print("Sending a call to the service to get metadata for image " + image_name)
        # Make a call to the Image Metadata Service to get a metadata with image description.
        image_description = requests.get('http://127.0.0.1:5000/image_process_only?url=photos/' + image_name).content
        data = json.loads(image_description)
        final_string = ', '.join(data["labels"])
        text_box.delete(1.0, END)
        text_box.insert(1.0, final_string)
        text_box.tag_add("center", 1.0, "end")
