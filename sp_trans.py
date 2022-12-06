from flask import Flask, jsonify, request
from googletrans import Translator
#import urllib.request
import speech_recognition as sr
import requests
#from ffprobe import FFProbe
from pydub import AudioSegment as am

app = Flask(__name__)
translator = Translator()


@app.route('/translator')
def trans():
    param1 = request.args.get('word', default='hello', type=str)
    param2 = request.args.get('lang', default='th', type=str)
    lang = translator.detect(param1).lang
    result = translator.translate(text=param1, src=lang, dest=param2)
    return jsonify({'result':str(result.text)})



@app.route('/sp2txt')
def uploader():
    r = sr.Recognizer()
    language = request.args.get('lang', type=str)
    url = request.args.get('audiourl')
    #print('input lang and url')
    #urllib.request.urlretrieve(url, file)
    response = requests.get(url)
    open('audio.wav', "wb").write(response.content)
    #print('create file')

    sound = am.from_file('audio.wav')
    sound = sound.set_frame_rate(8000)
    sound.export('audio.wav', format='wav')
    #print('save wav')

    with sr.AudioFile('audio.wav') as source:
        #audio = r.listen(source)
        audio = r.record(source)
        text = r.recognize_google(audio, language=language)
    #print('recognize txt')


    return jsonify({"text":text})
    

if __name__ == "__main__":
    app.run(debug=True)