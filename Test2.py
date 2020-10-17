import cv2
import tkinter as tk
from PIL import Image, ImageTk

class Video():
    def __init__(self, window):
        self.window = window


    def get(self):
        imageFrame = tk.Frame(self.window, width=600, height=500)
        imageFrame.grid(row=0, column=0, padx=10, pady=2)

        # Capture video frames
        global cap, lmain
        lmain = tk.Label(imageFrame)
        lmain.grid(row=0, column=0)
        cap = cv2.VideoCapture(0)

        self.show_frame()

        sliderFrame = tk.Frame(self.window, width=600, height=100)
        sliderFrame.grid(row=600, column=0, padx=10, pady=2)

    def show_frame(self):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, self.show_frame)

if __name__ == '__main__':

    window = tk.Tk()  # Makes main window
    window.wm_title("FACE ID")
    window.resizable(height=False, width=False)
    window.geometry("800x600")
    window.config(background="#FFFFFF")
    regis = Video(window)
    regis.get()
    window.mainloop()