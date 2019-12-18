from flask import Flask, request, send_file
import subprocess
import os
path = os.path.dirname(os.path.abspath(__file__))
songPath = os.path.join(path, 'songs')

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hi World!"


@app.route('/www.youtube.com/<string:videoId>')
def youtube(videoId):
    print('yt downloading!')
    fileName = videoId + '.mp3'
    filePath = os.path.join(path, 'songs', fileName)
    print(filePath)
    print(os.getcwd())
    url = 'https://www.youtube.com/watch?v=' + videoId
    subprocess.call(
        ['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o' + songPath + '/%(id)s.%(ext)s', url], shell=False)
    return send_file(filePath)


@app.route('/spotify/open.spotify.com/<string:type>/<string:url>')
def spotify(type, url):
    print('spt downloading!')
    fileName = request.args.get('isrc') + '.mp3'
    filePath = os.path.join(path, 'songs', fileName)
    subprocess.call(['spotdl', '-s open.spotify.com/' +
                     type + '/' + url, '-f' + songPath, '-ff', '{isrc}'], shell=False)
    return send_file(filePath)


if __name__ == '__main__':
    app.run(debug=True)
