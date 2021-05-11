from flask import Flask, request, jsonify, make_response, render_template
from googletrans import LANGUAGES
from speech_recognition import UnknownValueError

from ibm_cloud import processTextCommand, processImageData
from speech_processing import speechToText, translateText
from face_recognition import FacePrediction
from config import Config

app = Flask( __name__ )

def validateAudioFile(file):
    if file and file.name.strip() != '':
        return True
    return False
    
def validateLanguageCode(code):
    if code == '' or code is None:  
        return False
        
    lang = code.split("-")[0]
    return lang in LANGUAGES
    
@app.route("/")
def index():
    url = Config.stream_url()
    return render_template('index.html', stream_url=url)

@app.route("/api/postImage", methods=["POST"])
def receiveImageData():
    ImageData = request.files['image']
    res = {
        "status" : "failure",
        "message": "Something went wrong while processing file",
        "person" : ""
    }
    status_code=503

    if ImageData is None:
        res["message"] = "Missing File Data"
        status_code=422
    
    try:
        
        identified_name= FacePrediction(ImageData.read())
        processImageData(identified_name)
        res["status"] = "success"
        res["message"] = "File received"
        res["person"]=identified_name
        status_code=202
    except Exception as ex:
        res["error-type"]=ex.args
        print("In receiveImageData except block: ", ex)
        res["message"] = "Error in processing Image"


    response = make_response(jsonify(res), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*" 
    
    return response


@app.route("/api/postCommand", methods = ["POST", "GET"])
def receiveCommandData():
    if request.method == "GET":
        url = request.args.get('url') or Config.stream_url()
        return render_template("test.html", stream_url = url)
        
    audioData = request.files.get('audio')
    textCommand = request.form.get('text-command', "").strip() or None
    languageCode = request.form.get('language-code', 'en-US').strip()
    
    print(audioData, languageCode)
    res = {
        "status" : "failure",
        "message": "Something went wrong while processing command",
        "transcript": "",
        "warnings":[]
    }
    status_code = 503
    
    if not validateLanguageCode(languageCode):
        res["warnings"].append("Missing or Invalid Language Code using default code 'en-US'")
        languageCode = "en-US"
    
    if not validateAudioFile(audioData) and textCommand is None:
        res["message"] = "Missing or Invalid audio file/text command."
        status_code = 422
    else:
        try:
            if textCommand is not None:
                outputText = textCommand
            else:
                outputText = speechToText(audioData, languageCode)
            print(outputText)
            if not languageCode.startswith("en"):
                language = languageCode.split("-")[0]
                outputText = translateText(outputText, language) 

            processTextCommand(outputText)
            
            res["status"] = "success"
            res["message"] = "Command received"
            res["transcript"] = outputText
            status_code = 202
        
        except ValueError as ve:
            print("ValueError", ve)
            res["message"] = "Invalid file format"
            status_code = 415 
        
        except UnknownValueError as uve:
            print("Empty file/Unsupported Audio/No Voice", uve)
        
        except Exception as e:
            print("Other Error", e)
    
    response = make_response(jsonify(res), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*" 
    print(response)
    return response