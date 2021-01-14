import speech_recognition as sr

r = sr.Recognizer()
microphone_n = "Realtek High Definition Audio(SST)"
mic_list = sr.Microphone.list_microphone_names() 
  
#the following loop aims to set the device ID of the mic that 
#we specifically want to use to avoid ambiguity. 
for i, micname in enumerate(mic_list): 
    if microphone_n == micname: 
        device_id = i 
mic = sr.Microphone(device_index=i)
with mic as source:
    print("Speak Anything :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize what you said")
