# Kütüphaneleri import ederek başlıyoruz
import os
from face_recognition_app import face_rec
from flask import Flask, request, render_template, send_from_directory
import shutil

__author__ = "OrhanSertkaya"

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    images_list = []
    person_name = request.form['person_name']
    target = os.path.join(APP_ROOT, 'images/')

    if os.path.isdir(target):
        shutil.rmtree("images/")
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    for upload in request.files.getlist("file"):
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        images_list.append(filename)
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    for upload2 in request.files.getlist("file2"):
        print(upload2)
        print("{} is the file name".format(upload2.filename))
        filename = upload2.filename
        images_list.append(filename)
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload2.save(destination)

    result = face_rec.find_face(images_list,person_name)
    images_list.append(result)
    return render_template("complete.html", image_names=images_list)

@app.route('/upload/<string:filename>')
def send_image(filename):
    return send_from_directory("images/", filename)

if __name__ == "__main__":
    app.run(debug=True)