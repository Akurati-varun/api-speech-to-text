import speech_recognition as sr

r = sr.Recognizer()

def speechToText(file):
    audioData = sr.AudioFile(file )
    with audioData as source:
        audio = r.record(audioData)
    
    outputText = r.recognize_google(audio)
    
    return outputText