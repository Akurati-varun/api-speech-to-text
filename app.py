from flask import Flask, request, jsonify, make_response
from ibm_cloud import processTextCommand
from speech_processing import speechToText

app = Flask( __name__ )

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
    
