from flask import Flask, request, jsonify, make_response, render_template
from ibm_cloud import processTextCommand
from speech_processing import speechToText

app = Flask( __name__ )

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/postAudio", methods = ["POST"])
def recieveAudioData():

    audioData = request.files.get('audio')
    languageCode = request.form.get('language-code', 'en-US')
    
    print(audioData, languageCode)
    res = {
        "status" : "failure",
        "message": "",
        "translation": ""
    }

    if audioData is None:
        res["message"] = "Missing File Data"
        return make_response(jsonify(res), 422)
    
    try:
        outputText = speechToText(audioData, languageCode)
        processTextCommand(outputText)
    except Exception as e:
        print(e)
        res["message"] = "Error in processing command"
        return make_response(jsonify(res), 503)


    res["status"] = "success"
    res["message"] = "File received"
    res["translation"] = outputText

    return  make_response(jsonify(res), 202)
    
