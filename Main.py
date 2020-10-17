import cv2
from Start import Registration
from Trainer import Trainer
from Recognition import Recognizer
from Test2 import Video
import tkinter as tk
from PIL import Image, ImageTk
import os
import shutil


# Функция обработки и показа
def show_frame():
    with open('users.txt', 'r') as f:
        names = f.read().splitlines()
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        cv2image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, conf = rec.predict(cv2image[y:y + h, x:x + w])

        if (conf < 100):
            id = names[id]
            conf = "  {0}%".format(round(100 - conf))
        else:
            id = "Unknown"
            confidence = "  {0}%".format(round(100 - conf))

        cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(conf), (x + 5, y + h - 5), font, 1, (255, 255, 0), 2)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)



def login():
    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.place(x=0,y=0)
    # Capture video frames
    global lmain, cap, faceCascade, rec, font, id
    names = []
    with open('users.txt', 'r') as f:
        names = f.read().splitlines()
    lmain = tk.Label(imageFrame)
    lmain.place(x=0, y=0)
    cap = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read('trainer/trainer.yml')
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0

    show_frame()

def training():
    trainer = Trainer()
    trainer.Train()

    shutil.rmtree("face")
    os.mkdir("face")

    lbl_registered.destroy()
    lbl_success = tk.Label(window, text="You`re succesfully registered!",
                           font=("Arial", 18), bg="white")
    lbl_success.place(x=132, y=170)
    window.update()


def registration():

    face_id = id_form.get() # Name
    print("face_id=",face_id)

    lbl_name.destroy()
    id_form.destroy()
    btn_form.destroy()

    lbl_register = tk.Label(window, text="Don`t move your head too much. \n We`re registering your face",
                            font=("Arial", 18), bg="white")
    lbl_register.place(x=132, y=170)
    window.update()
    # Processing

    #-----------------------------
    lengthNames = []
    with open('users.txt', 'a') as f:
        f.write(face_id + '\n')
        f.close()
    with open('users.txt', 'r') as g:
        lengthNames = g.read().splitlines()
    #-----------------------------

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite('face/user.' + str(len(lengthNames)-1) + '.' + str(count) + '.jpg', gray[y:y + h, x:x + w])

        if count >= 30:
            break

    lbl_register.destroy()
    global lbl_registered
    lbl_registered = tk.Label(window, text="You can relax now. \n We`re adding you into the database",
                                  font=("Arial", 18), bg="white")
    lbl_registered.place(x=137, y=170)
    window.update()
    training()

def signup():
    btn_login.destroy()
    btn_signup.destroy()
    global id_form, btn_form, lbl_name

    btn_menu = tk.Button(window, text="MENU")


    lbl_name = tk.Label(window, text="Name:", font=("Arial", 10), bg='#3a5dde')
    lbl_name.place(x=210, y=170)


    id_form = tk.Entry(window, width=24)
    id_form.place(x=264, y=170)


    btn_form = tk.Button(window, image=img_reg, bd=0, command=registration)
    btn_form.place(x=210, y=200)

if __name__ == '__main__':
    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title("FACE ID")
    window.resizable(height=False, width=False)
    window.geometry("600x450")

    global btn_login, btn_signup
    names = ["Unknown"]
    img_reg = tk.PhotoImage(file="Images/reg.png")
    img_bg = tk.PhotoImage(file="Images/bg.gif")
    background_label = tk.Label(window, image=img_bg)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    img_login = tk.PhotoImage(file="Images/login.png")
    btn_login = tk.Button(window, image=img_login, bd=0, command=login)
    btn_login.place(x=210, y=150)

    img_signup = tk.PhotoImage(file="Images/signup.png")
    btn_signup = tk.Button(window, image=img_signup, bd=0, command=signup)
    btn_signup.place(x=210, y=200)

    
    window.mainloop()
