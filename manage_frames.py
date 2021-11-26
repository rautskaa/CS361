from functools import partial
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
from helper_functions import text_about_page, text_help_page, create_styled_button, set_style
from process_images import ImagesProcessing
from metadata_functions import save_metadata, remove_metadata


class Frames:

    def __init__(self, f_home, f_about, f_help, f_save):
        self.f1 = f_home
        self.f2 = f_about
        self.f3 = f_help
        self.f4 = f_save
        self.index_to_show = StringVar()
        self.image_index = [0]
        self.metadata_dict = {}
        self.shown_image = []
        self.configure_frames()
        self.img = ImagesProcessing(f_home)

    def configure_frames(self):
        """Add frames to a grid and configure columns and rows."""
        for frame in (self.f1, self.f2, self.f3, self.f4):
            frame.grid(row=0, column=0, sticky='news')
        self.f1.grid_propagate(False)
        self.f1.grid_rowconfigure(0, weight=0)
        self.f1.grid_columnconfigure(0, weight=0)

    def raise_frame(self, frame):
        """Lifting a frame to display.
        :param frame"""
        frame.tkraise()

    def start(self):
        """Beginning of the program. Build logo, all buttons, About and Help pages."""
        self.img.show_logo(None, True)
        self.create_pick_images_button()
        self.create_additional_buttons()
        # Create About page
        self.create_page(self.f2, "About Image Metadata App \n", text_about_page())
        # Create Help page
        self.create_page(self.f3, "User Guide \n", text_help_page())
        self.create_picker_instructions()

    def create_page(self, frame, page_name, text):
        """Create a page with the text displayed.
        :param frame
        :param page_name
        :param text"""
        self.img.show_logo(frame, False)
        self.create_home_button(None, frame, [3, 0, 100], False)
        self.show_text(frame, text, page_name)

    def create_picker_instructions(self):
        """Add instructions for image picker button."""
        font_app = font.Font(family='Arial', size=14)
        instructions = Label(self.f1, text="Select images on your computer", font=font_app)
        instructions.grid(row=1, column=0, padx=170)

    def create_navigation_icon(self, left, images, text_box):
        """Create and configure navigation icons
        :param left should be True if icon is left; False when right
        :param images images to show
        :param text_box text box to attach to.
        :return created icon"""
        image_data = []
        image_data.extend((self.index_to_show, self.image_index, self.shown_image))
        if left:
            icon = self.img.show_icon("arrow-left.png", W)
            icon.configure(
                command=lambda: self.img.next_prev_images(images, text_box, image_data, False))
        else:
            icon = self.img.show_icon("arrow-right.png", E)
            icon.configure(
                command=lambda: self.img.next_prev_images(images, text_box, image_data, True))
        return icon

    def create_home_button(self, elements, frame, layout, main_page):
        """Creates go home button
        :param elements to destroy
        :param frame to attach the button to
        :param layout of the button
        :param main_page True if it's main page
        :return created button"""
        row, column, padx, name = layout[0], layout[1], None, StringVar()
        home_command = partial(self.raise_frame, self.f1)
        # Unable to use create_styled_button(), the button should be created prior to destroying it
        arg1, arg2, arg3, com = elements, self.image_index, self.metadata_dict, self.destroy_elements
        if main_page:
            button = Button(frame, textvariable=name, command=lambda: com(arg1, arg2, arg3, button))
            button.configure(set_style(button))
            button.grid(row=row, column=column, padx=padx)
            name.set("Go Home")
        else:
            button = create_styled_button(frame, "Go Home", home_command, layout)
        return button

    def create_save_button(self, elements, home_button, images):
        """Creates save button
        :param elements to destroy
        :param home_button
        :param images"""
        button = Button(self.f1, text='Save', command=lambda: self.raise_frame(self.f4))
        button.grid(row=0, column=2, sticky=W)
        save_command = partial(self.confirm_saving, elements, home_button, images)
        layout = []
        layout.extend((2, 0, 100, None))
        create_styled_button(self.f1, "Save Metadata", save_command, layout)

    def create_undo_button(self, text, images):
        """Creates undo button on Save page
        :param text to display
        :param images"""
        undo = StringVar()
        undo_command = partial(remove_metadata, undo, text, images)
        layout = []
        layout.extend((1, 0, None, None))
        create_styled_button(self.f4, "Undo", undo_command, layout)

    def create_pick_images_button(self):
        """Add image picker button."""
        layout = []
        layout.extend((2, 0, 170, None))
        create_styled_button(self.f1, "Pick Images", self.show_images, layout)

    def create_additional_buttons(self):
        """Create buttons on the pages - About and Help"""
        about_button = Button(self.f1, text='About', command=lambda: self.raise_frame(self.f2))
        about_button.grid(row=10, column=0, pady=450, sticky=W)
        help_button = Button(self.f1, text='Help', command=lambda: self.raise_frame(self.f3))
        help_button.grid(row=10, column=0, pady=450, sticky=E)

    def create_gui_main_page(self, image, images):
        """Create GUI elements on the page for displaying images
        :param image the first image to show
        :param images all selected images."""
        # Create image menu, text box, icons and buttons
        image_menu = Label(self.f1, textvariable=self.index_to_show)
        image_menu.grid(row=5, column=0)
        # Create a text box and set an image description
        text_box = self.show_text_box()
        self.img.update_text_box(text_box, image)
        # Create and configure icons
        left_arrow_icon = self.create_navigation_icon(True, images, text_box)
        right_arrow_icon = self.create_navigation_icon(False, images, text_box)
        # Create main elements, home and save buttons
        elements = [text_box, image_menu, left_arrow_icon, right_arrow_icon, self.shown_image]
        home_button = self.create_home_button(elements, self.f1, [3, 0, 100], True)
        self.create_save_button(elements, home_button, images)

    def create_gui_save_page(self, images, elements):
        """Adds logo, text and undo button to save page
        :param elements for home page
        :param images"""
        self.create_home_button(elements, self.f4, [2, 0], True)
        self.img.show_logo(self.f4, False)
        text = self.show_text(self.f4, "", "All Metadata in images is now saved")
        self.create_undo_button(text, images)

    def show_home_page(self, image_index, shown_image, metadata):
        """Destroy elements on the page
        :param image_index
        :param shown_image
        :param metadata to clear"""
        # Show the main frame
        self.raise_frame(self.f1)
        # Remove all image data, icons and metadata to display main frame
        self.clear_data(image_index, shown_image, metadata)
        # Display Home page
        self.start()

    def show_text_box(self):
        """Show text box"""
        text_box = Text(self.f1, height=8, width=40, padx=10, pady=20, bg="#22bfc5")
        text_box.tag_configure("center", justify="center")
        text_box.grid(column=0, row=6)
        text_box.tag_add("center", 1.0, "end")
        return text_box

    def show_text(self, frame, text_to_show, title_to_show):
        """Show text
        :param frame
        :param text_to_show
        :param title_to_show"""
        text = Text(frame, height=15, width=70, bg="#22bfc5", padx=10, pady=10)
        text.tag_configure('big', font=('Arial', 14), justify='center')
        text.tag_configure('color', font=('Arial', 12))
        text.insert(END, title_to_show, 'big')
        text.insert(END, text_to_show, 'color')
        text.grid(row=7, column=0, padx=10, pady=10)
        return text

    def show_images(self):
        """Opens image picker and lets user select images with png and jpeg format.
        Adds GUI after images were selected: image menu, buttons, image display,
        text box with metadata and icons"""
        filetypes = (("png", "*.png"), ("jpeg", "*.jpg"), ("jpeg", "*.jpeg"))
        images = askopenfilenames(parent=self.f1, title="Select an Image", filetypes=filetypes)
        self.reset_images()
        image = images[0]
        self.img.set_index_to_show(images, self.image_index, self.index_to_show)
        current_image = self.img.show_image(image)
        self.shown_image.append(current_image)
        self.create_gui_main_page(image, images)

    def reset_images(self):
        """Resets images index and displayed images."""
        for image_index in self.image_index:
            self.image_index.pop()
        self.image_index.append(0)
        if self.shown_image:
            self.shown_image[-1].grid_forget()
            self.shown_image.pop()

    def confirm_saving(self, elements, home_button, images):
        """Confirmation window to save metadata
        :param elements to destroy
        :param home_button
        :param images"""
        warning_text = 'Are you sure you want to save metadata for the selected images?'
        dialog = messagebox.askquestion('Save Metadata', warning_text, icon='warning')
        if dialog == 'yes':
            self.raise_frame(self.f4)
            save_metadata(images)
            self.destroy_element(home_button)
        else:
            messagebox.showinfo('Return', 'You will now return to the Home screen')
            self.destroy_elements(elements, self.image_index, self.metadata_dict, home_button)
            self.start()
        self.create_gui_save_page(images, elements)

    def destroy_elements(self, elements, image_index, metadata, home_button):
        """Destroy elements on the page
        :param elements to destroy
        :param home_button
        :param image_index
        :param metadata to clear"""
        text_box, image_menu, shown_image = elements[0], elements[1], elements[4]
        icon_label, icon_label1 = elements[2], elements[3]
        text_box.destroy()
        image_menu.destroy()
        for image in shown_image:
            image.destroy()
        icon_label.destroy()
        home_button.destroy()
        icon_label1.destroy()
        self.show_home_page(image_index, shown_image, metadata)

    def destroy_element(self, element):
        """Destroy element on the page
        :param element to destroy"""
        element.destroy()

    def clear_data(self, image_index, shown_image, metadata):
        """Clear images data and metadata.
        :param image_index
        :param shown_image
        :param metadata"""
        image_index.clear()
        shown_image.clear()
        metadata.clear()
