from flask import Flask
from flask import send_file
from fileUtil import get_mp4_files_in_directory
from fileUtil import get_jpg_files_in_directory
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    marks = []
    conn = sqlite3.connect("vivifutbol.db")
    cur = conn.cursor()
    to_return = ""
    for row in cur.execute('SELECT * FROM video_marks'):
        to_return = to_return + row[0] + ","
    conn.close()
    return to_return


@app.route('/pruebas/<id>', methods=['GET', 'POST'])
def get_prueba(id):
    return "" + id

@app.route('/getImages', methods=['GET', 'POST'])
def get_images():
    #return "Seba"
    directory = '/home/pi/ViviFutbol/Videos/2016-11-12/mp4'
    newDirectoryName = "tmp"
    newDirectory = directory + "/" + newDirectoryName
    if(not os.path.exists(newDirectory)):
        os.makedirs(newDirectory)
        
    videos = get_mp4_files_in_directory(directory)
    for video in videos:
        imageName = video.replace(directory, newDirectory)
        imageName = imageName.replace(".mp4",".jpg")
        os.system("avconv -i "+video+" -vframes 1 -f image2 "+imageName);

    zipName = "thumbs.zip"
    os.system("cd "+directory+"; zip "+zipName+" "+newDirectoryName+"/*")
    return send_file(directory+"/"+zipName, mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1')
