from flask import Flask, request, jsonify  
import speech_recognition as sr

app = Flask( __name__ )
r = sr.Recognizer()

def SpeechToText(file):
    audioData = sr.AudioFile(file )
    with audioData as source:
        audio = r.record(audioData)
    
    outputText = r.recognize_google(audio) or "Failed"
    
    return outputText
    

@app.route("/postAudio", methods = ["POST"])
def recieveAudioData():
    audioData = request.files.get('audio')
    if audioData is None:
        return jsonify({"status": "Failure", "message": "Missing File Data"})
        
    outputText = SpeechToText(audioData)
    
    return  jsonify({"status": "Success", "message": "File received"})
    
