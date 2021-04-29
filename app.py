from flask import Flask, request, jsonify, make_response, render_template
from ibm_cloud import processTextCommand
from speech_processing import speechToText
from speech_recognition import UnknownValueError

app = Flask( __name__ )

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/api/postAudio", methods = ["POST", "GET"])
def recieveAudioData():
    if request.method == "GET":
        return render_template("test.html")
        
    audioData = request.files.get('audio')
    languageCode = request.form.get('language-code', 'en-US')

    print(audioData, languageCode)
    res = {
        "status" : "failure",
        "message": "Something went wrong while processing file",
        "translation": ""
    }
    status_code = 503

    if audioData is None:
        res["message"] = "Missing File Data"
        status_code = 422
    
    try:
        outputText = speechToText(audioData, languageCode)
        processTextCommand(outputText)
        res["status"] = "success"
        res["message"] = "File received"
        res["translation"] = outputText
        status_code = 202
    except ValueError as ve:
        print("ValueError", ve)
        res["message"] = "Invalid file format"
        status_code = 415 
    except UnknownValueError as uve:
        print("Empty file/Unsupported Audio/No Voice", uve)
    except:
        pass
    
    response = make_response(jsonify(res), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*" 
    
    return response