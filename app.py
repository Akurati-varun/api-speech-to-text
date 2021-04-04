from flask import Flask, request, jsonify, make_response
import speech_recognition as sr
from ibm_cloud import processTextCommand
 
app = Flask( __name__ )
r = sr.Recognizer()

def speechToText(file):
    audioData = sr.AudioFile(file )
    with audioData as source:
        audio = r.record(audioData)
    
    outputText = r.recognize_google(audio) or "Failed"
    
    return outputText
    

@app.route("/postAudio", methods = ["POST"])
def recieveAudioData():
    audioData = request.files.get('audio')
    res = {
        "status" : "failure",
        "message": "" 
    }

    if audioData is None:
        res["message"] = "Missing File Data"
        return make_response(jsonify(res), 422)
    
    try:
        outputText = speechToText(audioData)
        processTextCommand(outputText)
    except: 
        res["message"] = "Error in processing command"
        return make_response(jsonify(res), 503)


    res["status"] = "success"
    res["message"] = "File received"
    return  make_response(jsonify(res), 202)
    
