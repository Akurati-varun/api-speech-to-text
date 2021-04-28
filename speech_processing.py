import speech_recognition as sr

r = sr.Recognizer()

def speechToText(file, language="en-US"):
    audioData = sr.AudioFile(file )
    with audioData as source:
        audio = r.record(audioData)
    
    outputText = r.recognize_google(audio, language=language)
    
    return outputText