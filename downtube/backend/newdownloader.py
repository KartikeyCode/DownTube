from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app)

from pytube import YouTube

def download_video(link, choice):
    yt = YouTube(link)
    if choice == '1':
        stream = yt.streams.filter(only_audio=True).first()
    elif choice == '2':
        stream = yt.streams.filter(file_extension='mp4').first()
    else:
        return None
    
    if stream:
        filename = stream.title.replace(" ","") + ".mp4"
        file_path = os.path.abspath(os.path.join("downtube", "gaane", filename))
        stream.download(output_path="downtube/gaane", filename=filename)
        return file_path
    else:
        return None

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    link = data.get('link')
    choice = data.get('choice')
    
    if link and choice:
        file_path = download_video(link, choice)
        if file_path:
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'message': 'Invalid choice or unable to download video.'}), 400
    else:
        return jsonify({'message': 'Invalid request. Provide "link" and "choice" in the request body.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
