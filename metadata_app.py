from tkinter import *
from manage_frames import Frames
from process_images import ImagesProcessing

root = Tk()
root.title("Image Metadata App")

# Create frames for each page
f1 = LabelFrame(root, width=650, height=700)
f2 = LabelFrame(root)
f3 = LabelFrame(root)
f4 = LabelFrame(root)

img = ImagesProcessing(f1)
fr = Frames(f1, f2, f3, f4)

fr.start()
fr.raise_frame(f1)
root.mainloop()
