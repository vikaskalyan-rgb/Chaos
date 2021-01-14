from tkinter import *
import time
import speech_recognition as sr 
 
mic_name = "Realtek High Definition Audio(SST)"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer() 
device_id=1 


dur = 2000


def set_blind_F():
	blind = False
def set_blind_t():
	blind = True



def check_blind():
    top = Toplevel()
    top.title('WELCOME')
    Message(top, text="Can You Read text?If so click/say yes. Else click/say no", padx=20, pady=20).pack()
    b1 = Button(top, text="YES", command = "set_blind_f").pack()
    b2 = Button(top, text="NO", command = "set_blind_t").pack()
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source: 
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source) 
        try: 
            text = r.recognize_google(audio)
            if text == "yes":
                blind = False
            elif text == "no":
            	blind = True 
        except sr.UnknownValueError:
            print("error")
        except sr.RequestError as e:
            print("error1") 
    top.after(dur, top.destroy)


def set_hand_f():
	hand = True
def set_hand_t():
	hand = False



def check_hand():
    top = Toplevel()
    top.title('WELCOME')
    Message(top, text="Can You type text?If so click/say yes. Else click/say no", padx=20, pady=20).pack()
    b1 = Button(top, text="YES", command = "set_blind_f").pack()
    b2 = Button(top, text="NO", command = "set_blind_t").pack()
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source: 
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source) 
        try: 
            text = r.recognize_google(audio)
            if text == "yes":
                hand = True
            elif text == "no":
            	hand = False
        except sr.UnknownValueError:
            print("error")
        except sr.RequestError as e:
            print("error1") 
    top.after(dur, top.destroy)


root = Tk()
root.title("cha-OS")
root.geometry("500x500")
title = Label(root, text="chaOS", height=72, font=("Courier",50))
title.pack()
time.sleep(3)
check_blind()
time.sleep(3)
check_hand()



root.mainloop()