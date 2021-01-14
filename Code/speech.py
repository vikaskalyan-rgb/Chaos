import speech_recognition as sr 
import pyautogui as pag
import os
def findKeyWords(text,keywords):
	print(text)
	operations = []
	for i in text:
		if i.lower() in keywords:
			operations.append(i)
	return operations

def voiceOperation(operations):
	print(operations)
	for i in range(len(operations)):
		if operations[i].lower() == "select":
			pag.click()
		elif operations[i].lower() == 'options':
			pag.click(button="right")	
		elif operations[i].lower() == 'scroll' and operations[i+1].lower() == "up":
			pag.scroll(10)
		elif operations[i].lower() == 'scroll' and operations[i+1].lower() == "down":
			pag.scroll(-10)
		elif operations[i].lower() == "shutdown":
			os.system("shutdown /s /t 1")
		elif operations[i].lower() == "restart":
			os.system("shutdown /r /t 1")
		elif operations[i].lower() == "screenshot":
			im2 = pag.screenshot('my_screenshot.png')
		elif operations[i].lower() == "move" and operations[i+1].lower() == "mouse" and operations[i+2] == "right":
			pag.moveRel(30, 0)
		elif operations[i].lower() == "move" and operations[i+1].lower() == "mouse" and operations[i+2] == "left":
			pag.moveRel(-30, 0)


mic_name = "Realtek High Definition Audio(SST)"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer() 
device_id=1 
keywords = ["move","mouse","scroll","options","select","shutdown","restart","search","screenshot","open","close","left","right"]

mic_list = sr.Microphone.list_microphone_names()

for i, microphone_name in enumerate(mic_list): 
    if microphone_name == mic_name: 
        device_id = i 

with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
						chunk_size = chunk_size) as source: 
	r.adjust_for_ambient_noise(source)
	audio = r.listen(source) 
	try: 
		text = r.recognize_google(audio)
		print(text) 
		op = findKeyWords(text.split(),keywords)
		voiceOperation(op)
	except sr.UnknownValueError: 
		print("Google Speech Recognition could not understand audio") 
	
	except sr.RequestError as e: 
		print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
