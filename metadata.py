from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilenames
from PIL import ImageTk, Image
from tkinter import messagebox
from images import Images


def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("Image Metadata app")
index_to_show = StringVar()
image_index = [0]
metadata = {} # store all metadata for all images in list
shown_image = []
button_is_pressed = False
img = Images()

def clear_data():
    image_index.clear()
    shown_image.clear()
    metadata.clear()

f1 = LabelFrame(root, width=650, height=700) #Home page
f1.grid_propagate(False)
f1.grid_rowconfigure(0, weight=0)
f1.grid_columnconfigure(0, weight=0)

f2 = LabelFrame(root) #About page
f3 = LabelFrame(root) #Help page
f4 = LabelFrame(root) #Save page

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

def begin():
    img.show_logo(f1)
    appHighlightFont = font.Font(family='Pegasus', size=14)
    instructions = Label(f1, text="Select images on your computer", font=appHighlightFont)
    instructions.grid(row=1, column=0, padx=170)
    pick_image = StringVar()
    pick_image_button = Button(f1, textvariable=pick_image,
                               command=lambda: image_picker(), font="Roman",
                               bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
    pick_image.set("Pick Images")
    pick_image_button.grid(row=2, column=0, padx=170)

begin()

def next_images(images, index_to_show):
    if image_index[-1] < len(images) - 1:
        updated_index = image_index [-1] + 1
        image_index.pop()
        image_index.append(updated_index)
        if shown_image:
            shown_image[-1].grid_forget()
            shown_image.pop()
        new_image = images[image_index[-1]]
        current_image = img.show_image(f1, new_image)
        shown_image.append(current_image)
        index_to_show.set("Image " + str(image_index[-1] + 1) + " out of " + str(len(images)))

def previous_images(images, index_to_show):
    if image_index[-1] >= 1:
        updated_index = image_index [-1] - 1
        image_index.pop()
        image_index.append(updated_index)
        if shown_image:
            shown_image[-1].grid_forget()
            shown_image.pop()
        new_image = images[image_index[-1]]
        current_image = img.show_image(f1, new_image)
        shown_image.append(current_image)
        index_to_show.set("Image " + str(image_index[-1] + 1) + " out of " + str(len(images)))

def image_picker():
    images = askopenfilenames(parent=f1, title="Select an Image",
                              filetypes=(("png", "*.png"), ("jpeg", "*.jpg"), ("jpeg", "*.jpeg")))
    print(images)
    for i in image_index:
        image_index.pop()
    image_index.append(0)
    if shown_image:
        shown_image[-1].grid_forget()
        shown_image.pop()
    # read_image =

    image = images[0]
    index_to_show.set("Image " + str(image_index[-1] + 1) + " out of " + str(len(images)))

    # # # make a call to the service and return dictionary of lists, file name: list of strings
    # index = 0
    # for image in images:
    #     metadata[image] = index + 1
    #     index += 1
    # for k, v in metadata.items():
    #     print(k, v)

    current_image = img.show_image(f1, image)
    shown_image.append(current_image)

    image_menu = Label(f1, textvariable=index_to_show)
    image_menu.grid(row=5, column=0)

    icon1 = Image.open("arrow-left.png")
    icon1 = icon1.resize((20, 20))
    icon1 = ImageTk.PhotoImage(icon1)
    icon_label1 = Button(f1, image=icon1, width=25, height=25)
    icon_label1.image = icon1
    icon_label1.grid(column=0, row=5, sticky=W, padx=240)

    icon2 = Image.open("arrow-right.png")
    icon2 = icon2.resize((20, 20))
    icon2 = ImageTk.PhotoImage(icon2)
    icon_label = Button(f1, image=icon2, width=25, height=25)
    icon_label.image = icon2
    icon_label.grid(column=0, row=5, sticky=E, padx=240)
    icon_label.configure(command=lambda: next_images(images, index_to_show))
    icon_label1.configure(command=lambda: previous_images(images, index_to_show))

    text_box = img.display_text_box(f1)
    data_to_show = "flower"  # metadata
    text_box.insert(1.0, data_to_show)
    text_box.tag_add("center", 1.0, "end")

    go_home_main_page = StringVar()
    go_home_main_page_button = Button(f1, textvariable=go_home_main_page,
                                      command=lambda: destroy_images(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_main_page_button),
                                      font="Roman",
                                      bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
    go_home_main_page_button.grid(row=3, column=0, padx=100)
    go_home_main_page.set("Go home")

    Button(f1, text='Save', command=lambda: raise_frame(f4)).grid(row=0, column=2, sticky=W)
    save = StringVar()
    save_button = Button(f1, textvariable=save,
                               command=lambda: confirm_saving(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_main_page_button), font="Roman",
                               bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
    save.set("Save Metadata")
    save_button.grid(row=2, column=0, padx=100)

def confirm_saving(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_main_page_button):
    dialog = messagebox.askquestion('Save Metadata', 'Are you sure you want to save metadata for the selected images?',
                                       icon='warning')
    if dialog == 'yes':
        raise_frame(f4)
        print("Okay, Saving metadata now")
    else:
        messagebox.showinfo('Return', 'You will now return to the Home screen')
        destroy_images(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_main_page_button)
        begin()

    go_home_undo = StringVar()
    go_home_button = Button(f4, textvariable=go_home_undo,
                         command=lambda: destroy_images(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_main_page_button), font="Roman",
                         bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)
    go_home_button.grid(row=2, column=1)
    go_home_undo.set("Go home")

    text = Text(f4, height=8, bg="#22bfc5")
    text.grid(row=0, column=1)
    text.insert('1.0', 'All Metadata in images is now saved')

    undo = StringVar()
    undo_button = Button(f4, textvariable=undo,
                               command=lambda: img.remove_metadata(undo, text), font="Roman",
                               bg="#22bfc5", highlightbackground='#22bfc5', height=2, width=11)\

    undo_button.grid(row=1, column=1)
    undo.set("Undo")

def destroy_images(text_box, image_menu, icon_label, icon_label1, shown_image, go_home_button):
    print("Destroying everything")
    text_box.destroy()
    image_menu.destroy()
    for image in shown_image:
        print("image", image)
        image.destroy()
    icon_label.destroy()
    go_home_button.destroy()
    icon_label1.destroy()
    raise_frame(f1)
    clear_data()
    begin()

raise_frame(f1)
root.mainloop()