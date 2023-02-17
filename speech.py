import speech_recognition as sr
import time



def audio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print(len(source.list_microphone_names()))
      print(source.list_microphone_names())
      print("Say something!")
      #r.adjust_for_ambient_noise(source)
      audio = r.listen(source)

      #print(audio)
      data = r.recognize_google(audio)
      print(data)
    return data     
     
