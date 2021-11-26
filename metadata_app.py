from tkinter import *
from manage_frames import Frames
from process_images import ImagesProcessing

root = Tk()
root.title("Image Metadata App")

# Create frames for each page
f_home = LabelFrame(root, width=650, height=700)
f_about = LabelFrame(root)
f_help = LabelFrame(root)
f_save = LabelFrame(root)

img = ImagesProcessing(f_home)
app = Frames(f_home, f_about, f_help, f_save)

app.start()
app.raise_frame(f_home)
root.mainloop()
