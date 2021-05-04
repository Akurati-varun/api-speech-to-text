import speech_recognition as sr
from googletrans import Translator, LANGUAGES


def speechToText(file, language="en-US"):
    r = sr.Recognizer()
    
    audioData = sr.AudioFile(file)
    with audioData as source:
        audio = r.record(audioData)
    
    outputText = r.recognize_google(audio, language=language)
    
    return outputText
    
def translateText(text, src='auto', dest='en'):
    tr = Translator()
    if src in LANGUAGES:
        result = tr.translate(text, src=src, dest=dest)
    else:
        raise Exception(f"translateText: '{src}' language not supported")
        
    return result.text