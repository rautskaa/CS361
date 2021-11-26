import os
from tkinter import END

import requests


def save_metadata(images):
    """Save metadata for each image.
    :param images"""
    for image in images:
        image_name = os.path.basename(image)
        print("Sending a call to the service to save metadata for image " + image_name)
        requests.get('http://127.0.0.1:5000/image_process_with_save?url=photos/' + image_name)


def remove_metadata(undo, text, images):
    """Remove metadata if user chooses to. Sets button from Undo to Undone.
    :param undo
    :param text
    :param images"""
    undo.set("Undone")
    text.delete('1.0', END)
    text.insert(END, "All metadata is now removed", 'big')
    text.tag_configure('big', font=('Arial', 14), justify='center')
    for image in images:
        image_name = os.path.basename(image)
        print("Sending a call to the service to remove metadata for image " + image_name)
        print(os.path.basename(image))
        requests.get('http://127.0.0.1:5000/image_del_METADATA?url=photos/' + image_name)
