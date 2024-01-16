#This file is used to download youtube videos 
from flask import Flask, request, jsonify
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)
from pytube import YouTube
import requests


def download_video(link, choice):
    yt = YouTube(link)
    if choice == '1':
        stream = yt.streams.filter(only_audio=True).first()
    elif choice == '2':
        stream = yt.streams.filter(file_extension='mp4').first()
    else:
        return None
    
    if stream:
        stream.download(output_path="./downtube/gaane",filename=stream.title.replace(" ","")+".mp4")
        return stream.title 
    else:
        return None
@app.route('/download', methods=['POST'])
def download():
    data = request.json #Takes data from the body of request in raw format ex: {"link": "https://www.youtube.com/watch?v=6nTcdw7bVdc", "choice": "1"}
    link = data.get('link') #finds link from above data (youtube link)
    choice = data.get('choice') #finds choice from above data (1 or 2)
    if link and choice:
        title = download_video(link, choice)
        if title:
            return jsonify({'message': f'Download successful! Title: {title}', 'title':title}), 200
        else:
            return jsonify({'message': 'Invalid choice or unable to download video.'}), 400
    else:
        return jsonify({'message': 'Invalid request. Provide "link" and "choice" in the request body.'}), 400

if __name__ == '__main__':
    app.run(debug=True)    