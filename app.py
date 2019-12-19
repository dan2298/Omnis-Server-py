from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess
import os
path = os.path.dirname(os.path.abspath(__file__))
songPath = os.path.join(path, 'songs')

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Hi World!"


@app.route('/www.youtube.com/<string:videoId>')
def youtube(videoId):
    print('yt downloading')
    fileName = videoId + '.mp3'
    filePath = os.path.join(path, 'songs', fileName)
    url = 'https://www.youtube.com/watch?v=' + videoId
    subprocess.call(
        ['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o' + songPath + '/%(id)s.%(ext)s', url], shell=False)
    return send_file(filePath)


@app.route('/spotify/open.spotify.com/<string:type>/<string:url>')
def spotify(type, url):
    print('spt downloading')
    fileName = request.args.get('isrc') + '.mp3'
    filePath = os.path.join(path, 'songs', fileName)
    subprocess.call(['spotdl', '-s open.spotify.com/' +
                     type + '/' + url, '-f' + songPath, '-ff', '{isrc}'], shell=False)
    return send_file(filePath)


@app.route('/soundcloud/info')
def soundcloudInfo():
    term = request.args.get('q')
    url = 'https://soundcloud.com/search?q=' + term
    print(url)
    driver = webdriver.Chrome(path + '/chromedriver')
    driver.get(url)
    print('got url =========')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print('parsed html =========')
    items = soup.findAll("div", {"class": "sound__body"})
    results = []
    print('found =========')
    for x in items:
        results.append(str(x))
    return Response(json.dumps(results),  mimetype='application/json')


@app.route('/soundcloud')
def soundcloud():
    print('sc downloading')
    subprocess.call(
        ['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o' + songPath + '/%(title)s.%(ext)s', 'https://soundcloud.com/jahkoy/letitbe'], shell=False)
    return 'hi'


if __name__ == '__main__':
    app.run(debug=True)
