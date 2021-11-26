from tkinter import StringVar, Button


def text_about_page():
    """Text to display in About page."""
    return "\nImage Metadata app allows to view and update metadata of the images with " \
           "their description. \nWith the help of Google Vision API, the app detects and " \
           "extracts information about \nentities in an image, across a broad group of " \
           "categories: labels, landmarks, logos, \ntext.\nIt only takes a few minutes " \
           "to process images on your computer. \n\nIf you would like to learn more " \
           "about Vision AI, go to https://cloud.google.com/vision."


def text_help_page():
    """Text to display in Help page."""
    return '\n1. To process images click the "Pick images" button on the Home screen. ' \
           '\n2. Select images from your computer you would like to process. Supported ' \
           'extensions are png, jpeg, jpg.\n3. To check the metadata to be added for ' \
           'each image, tap on the right arrow button. If everything looks okay, select ' \
           'the "Save" button to save metadata and then confirm in the dialog window.' \
           '\n4. To view metadata saved, open information about each image and check ' \
           'the "Description" section.\n\nRemember, if you change your mind at the last ' \
           'minute, you can press the Undo button\nto revert the change and metadata ' \
           'will be removed from the images.'


def create_styled_button(frame, text, command, layout):
    """Create a button with a style.
    :param frame to attach the button to
    :param text for the button
    :param command to issue
    :param layout"""
    button_text = StringVar()
    padx, pady = None, None
    if len(layout) == 3: padx = layout[2]
    if len(layout) > 3: pady = layout[3]
    row, column = layout[0], layout[1]
    button = Button(frame, textvariable=button_text, command=lambda: command())
    button.configure(set_style(button))
    button_text.set(text)
    button.grid(row=row, column=column, padx=padx, pady=pady)
    return button


def set_style(button):
    button.configure(font="Roman", bg="#22bfc5", highlightbackground="#22bfc5", height=2, width=11)