from flask import Flask, send_file, jsonify
from fileUtil import get_mp4_files_in_directory, get_jpg_files_in_directory, get_file_name_without_extension
from dbUtil import download_code_exists, code_used, code_download
import sqlite3
import os
import os.path
from utils import decode_time

#Constantes de la base de datos
PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Videos/2017-04-01/mp4'
#PATH_VIDEO_LOCALIZATION = '/home/pi/ViviFutbolLocal/VideosPRUEBA_10/2017-04-16/mp4'

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


#172.24.1.1:5000/getImages
@app.route('/getImages', methods=['GET', 'POST'])
def get_images():
    directory = PATH_VIDEO_LOCALIZATION
    
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


#172.24.1.1:5000/getImages/<name>
@app.route('/getVideo/<name>', methods=['GET', 'POST'])
def get_video(name):
    ## TODO hay que ver como recibimos el codigo aca tmb
    ##code_download(video_code)
    name = name.split('.')[0] + ".mp4"
    directory = PATH_VIDEO_LOCALIZATION
    filePath = directory + "/" + name
    if os.path.isfile(filePath):
        return send_file(filePath, mimetype='video/mp4')
    else:
        return ('',204)


#172.24.1.1:5000/validateCode/<code>
@app.route('/validateCode/<code>', methods=['GET', 'POST'])
def validate_code(code):
    if(len(code) > 4):            
        if code == "ABC123":
            ##TODO DEBUG - sacar
            return ('OK', 200)
        else:
            ##el codigo es toda la string salvo las ultimas 3 letras
            video_code = code[:-3]
            ##el tiempo son las ultimas tres letras
            encrypted_time = code[-3:]
            time = decode_time(encrypted_time)
            if time is not None:
                if(download_code_exists(video_code)):
                    ##code_used(video_code)
                    return jsonify({"status":"ok", "time":time})
                else:
                    return jsonify({"status":"error", "errorMessage":"El codigo es incorrecto"})
            else:
                return jsonify({"status":"error", "errorMessage":"El codigo es incorrecto"})
    else:
        return jsonify({"status":"error","errorMessage":"El codigo debe tener al menos 5 caracteres"})
    

if __name__ == '__main__':
    app.run(debug=True, host='172.24.1.1')
