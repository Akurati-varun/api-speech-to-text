from flask import Flask, request, jsonify, make_response, render_template
from googletrans import LANGUAGES
from speech_recognition import UnknownValueError
<<<<<<< HEAD
from PIL import Image, ImageOps
=======
>>>>>>> c057e58b027924cbb5ec0a02c89952b0b9e4c992

from ibm_cloud import processTextCommand, processImageData
from speech_processing import speechToText, translateText
from face_recognition import FacePrediction
from config import Config


app = Flask( __name__ )

def validateFile(file):
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
<<<<<<< HEAD
<<<<<<< HEAD
    ImageData = request.files['image']
    image = Image.open(ImageData)
    gray_image = ImageOps.grayscale(image)
=======
    imageData = request.files.get('image')
    imageï¿½=ï¿½Image.open(imageData)
ï¿½ï¿½ï¿½ï¿½gray_imageï¿½=ï¿½ImageOps.grayscale(image)
>>>>>>> c057e58b027924cbb5ec0a02c89952b0b9e4c992

=======
    imageData = request.files.get("image")
>>>>>>> 8ed54d0fc9ea22cb5e86f917d923b60a3d2d893b
    res = {
        "status" : "failure",
        "message": "Something went wrong while processing file",
        "person" : ""
    }
    status_code=503

<<<<<<< HEAD
    if validateFile(imageData):
        res["message"] = "Missing File Data"
        status_code=422
    
    try:
<<<<<<< HEAD
        identified_name= FacePrediction(gray_image)
=======
        imageData = Image.open(imageData)
        imageData = ImageOps.grayscale(imageData)
        
        identified_name= FacePrediction(imageData)
>>>>>>> 8ed54d0fc9ea22cb5e86f917d923b60a3d2d893b
=======
    if imageData is None:
        res["message"] = "Missing File Data"
        status_code=422
    
    try:        
        identified_name= FacePrediction(imageData)
        
>>>>>>> c057e58b027924cbb5ec0a02c89952b0b9e4c992
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
    
    if not validateFile(audioData) and textCommand is None:
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
<<<<<<< HEAD
    
    return response
<<<<<<< HEAD
=======
    print(response)
    return response
>>>>>>> 8ed54d0fc9ea22cb5e86f917d923b60a3d2d893b
=======

>>>>>>> c057e58b027924cbb5ec0a02c89952b0b9e4c992
