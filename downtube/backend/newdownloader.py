from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 
import os
import time 
app = Flask(__name__)
CORS(app)
from pytube import YouTube

def cleanup_downloads():
    directory = os.path.abspath("downtube/gaane")
    threshold = time.time() - (24 * 60 * 60)  # Delete files older than 24 hours

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < threshold:
            os.remove(file_path)

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

@app.route('/test')
def test():
    return "Testing Testing"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    link = data.get('link')
    choice = data.get('choice')
    
    if link and choice:
        file_path = download_video(link, choice)
        if file_path:
            cleanup_downloads()
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'message': 'Invalid choice or unable to download video.'}), 400
    else:
        return jsonify({'message': 'Invalid request. Provide "link" and "choice" in the request body.'}), 400



if __name__ == '__main__':
    cleanup_downloads()
    app.run(debug=True)
