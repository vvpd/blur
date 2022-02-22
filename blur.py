import sys, os
from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from playsound import playsound

IMAGE_NAME = "test.png"
DURATION_MS = 1000
INCREASE = 0.1
WAIT_BEFORE_START = 10000

os.environ["DISPLAY"] = ":0.0"

tk = Tk()
tk.title = "BLUR"
# tk.resizable(0,0)
tk.overrideredirect(1)
w, h = tk.winfo_screenwidth(), tk.winfo_screenheight()
tk.geometry("%dx%d+0+0" % (w, h))
tk.attributes('-fullscreen', True)
tk.wm_attributes("-topmost", 1)
tk.config(cursor="none")

canvas = Canvas(tk, width=w, height=h, bd=0, highlightthickness=0)
canvas.pack()
canvas.configure(background='black')

class FadingImage:
    def __init__(self, canvas, img):
        imgWidth, imgHeight = img.size
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        self.pilImage = img.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas
        self.id = canvas.create_image(w/2,h/2,image=self.image)
        self.amount = INCREASE

    def start(self):
        self.canvas.after(WAIT_BEFORE_START, self.draw)

    def draw(self):
        print('update')
        self.amount += INCREASE
        self.pilImage = self.pilImage.filter(ImageFilter.GaussianBlur(self.amount))
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.id = canvas.create_image(w/2,h/2,image=self.image)
        playsound('click.mp3')
        self.canvas.after(DURATION_MS, self.draw)  #(time_delay, method_to_execute)


load = Image.open(IMAGE_NAME)
img = FadingImage(canvas, load)
img.start()
tk.mainloop()