from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import subprocess
import urllib.parse
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


@app.route('/soundcloud/<string:artist>/<string:song>')
def soundcloud(artist, song):
    print('sc downloading')
    fileName = request.args.get('name') + '.mp3'
    filePath = os.path.join(path, 'songs', fileName)
    url = 'https://soundcloud.com/' + artist + '/' + song
    subprocess.call(
        ['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o' + songPath + '/%(title)s.%(ext)s', url], shell=False)
    return send_file(filePath)


@app.route('/soundcloud/info')
def soundcloudInfo():
    term = str(urllib.parse.quote(request.args.get('q')))
    url = 'https://soundcloud.com/search/sounds?q=' + term
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver = webdriver.Chrome('./chromedriver')  # offline use
    driver.get(url)
    try:
        element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "sound__coverArt"))
        )
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    pics = soup.findAll("a", {"class": "sound__coverArt"})
    content = soup.findAll(
        "div", {"class": "soundTitle__usernameTitleContainer"})
    picsArr = []
    contentArr = []

    if len(content) == 0:
        return {'content': [], 'pics': []}

    for x in range(3):
        contentArr.append(str(content[x]))
        picsArr.append(str(pics[x]))

    results = {'content': contentArr, 'pics': picsArr}
    return Response(json.dumps(results),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
