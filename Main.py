import cv2
from Start import Registration
from Trainer import Trainer
from Recognition import Recognizer
from Test2 import Video
import tkinter as tk
from PIL import Image, ImageTk

# Функция обработки и показа
def show_frame():
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
            id = "unknown person"
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
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    # Capture video frames
    global lmain, cap, faceCascade, rec, font, id, names
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    cap = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read('trainer/trainer.yml')
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0

    names = ['None', 'Misha', 'Katya', 'Vlada', 'Sasha', 'Alexey']

    sliderFrame = tk.Frame(window, width=600, height=100)
    sliderFrame.grid(row=600, column=0, padx=10, pady=2)

    show_frame()

def training():
    trainer = Trainer()
    trainer.Train()
    lbl_registered.destroy()
    lbl_success = tk.Label(window, text="You`re succesfully registered!",
                           font=("Arial", 18), bg="white")
    lbl_success.place(x=220, y=250)
    window.update()


def registration():
    face_id = id_form.get()
    id_form.destroy()
    btn_form.destroy()

    lbl_register = tk.Label(window, text="Don`t move your head too much. \n We`re registering your face",
                            font=("Arial", 18), bg="white")
    lbl_register.place(x=220, y=250)
    window.update()
    # Processing

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
            cv2.imwrite('face/user.' + str(face_id) + '.' + str(count) + '.jpg', gray[y:y + h, x:x + w])
        """cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff
        if k == 50:
            break
        el"""
        if count >= 30:
            break

    lbl_register.destroy()
    global lbl_registered
    lbl_registered = tk.Label(window, text="You can relax now. \n We`re adding you into the database",
                                  font=("Arial", 18), bg="white")
    lbl_registered.place(x=220, y=250)
    window.update()
    training()

def signup():
    print("signup")
    btn_login.destroy()
    btn_signup.destroy()
    global id_form, btn_form
    id_form = tk.Entry(window)
    id_form.place(x=280, y=200)
    btn_form = tk.Button(window, text = "Continue", command=registration)
    btn_form.place(x=280, y=230)

if __name__ == '__main__':
    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title("FACE ID")
    window.resizable(height=False, width=False)
    window.geometry("800x600")
    window.config(background="#FFFFFF")

    global btn_login, btn_signup
    btn_login = tk.Button(window, text="LOGIN", command=login)
    btn_login.place(x=280, y=150)

    btn_signup = tk.Button(window, text="SIGNUP", command=signup)
    btn_signup.place(x=280, y=180)


    window.mainloop()