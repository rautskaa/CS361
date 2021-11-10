import os
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox

import requests

from process_images import ImagesProcessing


class Frames:

    def __init__(self, f1, f2, f3, f4):
        self.f1 = f1  # Home page
        self.f2 = f2  # About page
        self.f3 = f3  # Help page
        self.f4 = f4  # Save page
        self.index_to_show = StringVar()
        self.image_index = [0]
        self.metadata = {}  # metadata for all images
        self.shown_image = []
        self.configure_frames()
        self.img = ImagesProcessing(f1)

    def configure_frames(self):
        """Add frames to a grid and configure columns and rows."""
        for frame in (self.f1, self.f2, self.f3, self.f4):
            frame.grid(row=0, column=0, sticky='news')
        self.f1.grid_propagate(False)
        self.f1.grid_rowconfigure(0, weight=0)
        self.f1.grid_columnconfigure(0, weight=0)

    def start(self):
        """Beginning of the program. Build logo, all buttons, About and Help pages."""
        self.img.show_logo()
        self.create_buttons()
        self.pick_images_button()
        self.about_page()
        self.help_page()
        self.image_picker_instructions()

    def raise_frame(self, frame):
        """Lifting a frame to display.
        :param frame
        """
        frame.tkraise()

    def about_page(self):
        """Create About page with text displayed."""
        text_to_show = 'About\n Image Metadata app allows you to update metadata of the images with their description. The app uses machine learning to understand your images. With the help of Google Vision API, we can detect and extract information about entities in an image, across a broad group of categories. \n It only takes a few minutes to process images on your computer! \n If you would like to learn more about Vision AI, go to https://cloud.google.com/vision/'
        self.show_text(self.f2, 0, 1, text_to_show)

    def help_page(self):
        """Create Help page with text displayed."""
        text_to_show = 'User Guide\n 1. To process the images first click "Pick images" button on the Home screen. \n 2. Select images from your computer you would like to process. You can pick as many files as you want with the extension png, jpeg, jpg.\n 3. Tap on Save button and if everything looks okay, confirm in the dialog window.\n\n Remember, if you change your mind at the last minute, you can press Undo button to revert the change and metadata will be removed from the images.'
        self.show_text(self.f3, 0, 1, text_to_show)

    def image_picker_instructions(self):
        """Add instructions for image picker button."""
        font_app = font.Font(family='Pegasus', size=14)
        instructions = Label(self.f1, text="Select images on your computer", font=font_app)
        instructions.grid(row=1, column=0, padx=170)

    def clear_data(self, image_index, shown_image, metadata):
        """Clear images data and metadata.
        :param image_index
        :param shown_image
        :param metadata"""
        image_index.clear()
        shown_image.clear()
        metadata.clear()

    def pick_images(self):
        """Opens image picker and lets user select images with png and jpeg format.
        Creates GUI after images were selected: image menu, buttons, image display, text box with metadata and icons"""
        images = askopenfilenames(parent=self.f1, title="Select an Image",
                                  filetypes=(("png", "*.png"), ("jpeg", "*.jpg"), ("jpeg", "*.jpeg")))
        print(images)
        for image_index in self.image_index:
            self.image_index.pop()
        self.image_index.append(0)
        if self.shown_image:
            self.shown_image[-1].grid_forget()
            self.shown_image.pop()
        image = images[0]
        self.img.set_index_to_show(images, self.image_index, self.index_to_show)

        current_image = self.img.show_image(image)
        self.shown_image.append(current_image)

        # Create image menu
        image_menu = Label(self.f1, textvariable=self.index_to_show)
        image_menu.grid(row=5, column=0)

        # Create a text box and set an image description
        text_box = self.show_text_box()
        self.img.update_text_box(text_box, image)

        # Create and configure icons
        left_arrow_icon = self.img.show_icon("arrow-left.png", W)
        right_arrow_icon = self.img.show_icon("arrow-right.png", E)
        left_arrow_icon.configure(
            command=lambda: self.img.previous_images(images, self.index_to_show, self.image_index, self.shown_image, text_box))
        right_arrow_icon.configure(
            command=lambda: self.img.next_images(images, self.index_to_show, self.image_index, self.shown_image, text_box))

        # Create go home and save buttons
        elements = [text_box, image_menu, left_arrow_icon, right_arrow_icon, self.shown_image]
        home_button = self.go_home_button(elements, self.f1, [3, 0, 100])
        self.save_button(elements, home_button, images)

    def go_home_button(self, elements, frame, layout):
        """Creates go home button
        :param elements to destroy
        :param frame to attach the button to
        :param layout of the button.
        :return created button"""
        row = layout[0]
        column = layout[1]
        padx = None
        if len(layout) > 2:
            padx = layout[2]
        go_home_main_page = StringVar()
        go_home_main_page_button = Button(frame, textvariable=go_home_main_page,
                                          command=lambda: self.destroy_elements(elements,
                                                                                go_home_main_page_button,
                                                                                self.image_index, self.metadata),
                                          font="Roman",
                                          bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
        go_home_main_page_button.grid(row=row, column=column, padx=padx)
        go_home_main_page.set("Go home")
        return go_home_main_page_button

    def save_button(self, elements, go_home_main_page_button, images):
        """Creates save button
        :param elements to destroy
        :param go_home_main_page_button
        :param images"""
        Button(self.f1, text='Save', command=lambda: self.raise_frame(self.f4)).grid(row=0, column=2, sticky=W)
        save = StringVar()
        save_button = Button(self.f1, textvariable=save,
                             command=lambda: self.confirm_saving(elements, go_home_main_page_button, images), font="Roman",
                             bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
        save.set("Save Metadata")
        save_button.grid(row=2, column=0, padx=100)

    def undo_button(self, text, images):
        """Creates undo button on Save page
        :param text to display
        :param images"""
        undo = StringVar()
        undo_button = Button(self.f4, textvariable=undo,
                             command=lambda: self.remove_metadata(undo, text, images), font="Roman",
                             bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
        undo_button.grid(row=1, column=1)
        undo.set("Undo")

    def pick_images_button(self):
        """Add image picker button."""
        pick_image = StringVar()
        pick_image_button = Button(self.f1, textvariable=pick_image,
                                   command=lambda: self.pick_images(), font="Roman",
                                   bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
        pick_image.set("Pick Images")
        pick_image_button.grid(row=2, column=0, padx=170)

    def confirm_saving(self, elements, go_home_main_page_button, images):
        """Confirmation window to save metadata
        :param elements to destroy
        :param go_home_main_page_button
        :param images"""
        dialog = messagebox.askquestion('Save Metadata',
                                        'Are you sure you want to save metadata for the selected images?',
                                        icon='warning')
        if dialog == 'yes':
            self.raise_frame(self.f4)
            print("Okay, Saving metadata...")
            self.destroy_element(go_home_main_page_button)
        else:
            messagebox.showinfo('Return', 'You will now return to the Home screen')
            self.destroy_elements(elements, go_home_main_page_button, self.image_index, self.metadata)
            self.start()

        new_go_home_button = self.go_home_button(elements, self.f4, [2, 1])
        # Add text and undo button
        text = self.show_text(self.f4, 0, 1, 'All Metadata in images is now saved')
        self.undo_button(text, images)

    def destroy_elements(self, elements, go_home_button, image_index, metadata):
        """Destroy elements on the page
        :param elements to destroy
        :param go_home_button
        :param image_index
        :param metadata to clear"""
        text_box = elements[0]
        image_menu = elements[1]
        icon_label = elements[2]
        icon_label1 = elements[3]
        shown_image = elements[4]
        print("Destroying everything")
        text_box.destroy()
        image_menu.destroy()
        for image in shown_image:
            image.destroy()
        icon_label.destroy()
        go_home_button.destroy()
        icon_label1.destroy()
        # Show the main frame
        self.raise_frame(self.f1)
        # Clear image data and metadata
        self.clear_data(image_index, shown_image, metadata)
        # Display Home page
        self.start()

    def create_button(self, frame, text, command, row, column, pady=None, sticky=None):
        """Create a button
         :param frame to attach the button to
         :param text for the button
         :param command to issue
         :param row
         :param column
         :param pady
         :param sticky"""
        Button(frame, text=text, command=lambda: command).grid(row=row, column=column, pady=pady, sticky=sticky)

    def destroy_element(self, element):
        """Destroy element on the page
        :param elements to destroy"""
        element.destroy()

    def create_buttons(self):
        """Create buttons on the pages"""
        Button(self.f1, text='About', command=lambda: self.raise_frame(self.f2)).grid(row=10, column=0, pady=450,
                                                                                      sticky=W)
        Button(self.f1, text='Help', command=lambda: self.raise_frame(self.f3)).grid(row=10, column=0, pady=450,
                                                                                     sticky=E)
        Button(self.f2, text='Go Home', command=lambda: self.raise_frame(self.f1)).grid(row=5, column=1)
        Button(self.f3, text='Go Home', command=lambda: self.raise_frame(self.f1)).grid(row=5, column=1)

    def show_text_box(self):
        """Show text box"""
        text_box = Text(self.f1, height=5, width=25, padx=15, pady=15, bg="#22bfc5")
        text_box.tag_configure("center", justify="center")
        text_box.grid(column=0, row=6)
        text_box.tag_add("center", 1.0, "end")
        return text_box

    def show_text(self, frame, row, column, text_to_show):
        """Show text
        :param frame
        :param row
        :param column
        :param text_to_show"""
        text = Text(frame, height=8, bg="#22bfc5")
        text.grid(row=row, column=column)
        text.tag_add("center", "1.0", "end")
        text.insert('1.0', text_to_show)
        return text

    def remove_metadata(self, undo, text, images):
        """Remove metadata if user chooses to. Sets button from Undo to Undone
        :param undo
        :param text
        :param images"""
        undo.set("Undone")
        text.delete('1.0', END)
        text.insert('1.0', "All metadata is now removed")
        for image in images:
            image_name = os.path.basename(image)
            print(os.path.basename(image))
            requests.get('http://127.0.0.1:5000/image_del_METADATA?url=photos/' + image_name)
