# Store this code in 'app.py' file
from flask import Flask, redirect, url_for, render_template, request, session, flash
import datetime
from io import BytesIO
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///audio.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)

uploads_dir = os.path.join(app.instance_path, 'uploads')
if os.path.exists(uploads_dir):
    pass
else:
    os.makedirs(uploads_dir)

class audio(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    type = db.Column("type", db.String(100))
    name = db.Column("name", db.String(100))
    duration = db.Column("duration", db.Float)
    uploadtime = db.Column("uploadtime", db.String(100))
    host = db.Column("host", db.String(100))
    participants = db.Column("participants", db.String(100))
    author = db.Column("author", db.String(100))
    narrator = db.Column("narrator", db.String(100))
    audio_file = db.Column("audio_file", db.String)

    def __init__(
        self,
        id,
        type,
        name,
        duration,
        uploadtime,
        host,
        participants,
        author,
        narrator,
        audio_file,
    ):
        self.id = id
        self.type = type
        self.name = name
        self.duration = duration
        self.uploadtime = uploadtime
        self.host = host
        self.participants = participants
        self.author = author
        self.narrator = narrator
        self.audio_file = audio_file


@app.route("/")
@app.route("/", methods=["POST"])  # this sets the route to this page
def home():
    if request.method == "POST":
        if request.files:
            file = {}
            file["id"] = request.form["id"]
            file["name"] = request.form["name"]
            file["duration"] = request.form["duration"] 
            audio_file = request.files["audio"]

            audio_file.save(os.path.join(uploads_dir, audio_file.filename))
            path = os.path.join(uploads_dir, audio_file.filename)
            print(path, type(path))
            file["audio_file"] = str(path)
            file["uploadtime"] = datetime.datetime.now()
            file["host"] = ""
            file["participants"] = ""
            file["author"] = ""
            file["narrator"] = ""

            if request.form["type"] == "song":
                file["type"] = "song"
                print("song")

            if request.form["type"] == "podcast":

                file["type"] = "podcast"
                file["host"] = request.form["host"]
                file["participants"] = request.form["participants"]

                print("podcast")

            if request.form["type"] == "audiobook":
                file["type"] = "audiobook"
                file["author"] = request.form["author"]
                file["narrator"] = request.form["narrator"]

                print("audiobook")

            # print(id, name, duration, uploadtime, type)

            found_audio = audio.query.filter_by(id=file["id"]).first()
            if found_audio:

                flash("Enter unique ID, file already exists")

            else:
                aud = audio(
                    file["id"],
                    file["type"],
                    file["name"],
                    file["duration"],
                    file["uploadtime"],
                    file["host"],
                    file["participants"],
                    file["author"],
                   file["narrator"],
                   file["audio_file"],
                )
                db.session.add(aud)
                db.session.commit()
                flash("Data Entered", "info")
            return render_template("home.html")

        else:
            flash("Audio file not found")
            return render_template("home.html")

    else:
        return render_template("home.html")


@app.route("/get/<atype>/<aid>", methods = ["GET"])
def find_file(atype,aid):
    value = audio.query.filter_by(id = int(aid), type = atype)
    num_results = audio.query.filter_by(id = int(aid), type = atype).count()

    if int(num_results) != 0:
        return render_template("get.html", value = value, BytesIO = BytesIO)
    else:
        flash("File not present in Database")
        return render_template("home.html")

@app.route("/get/<atype>", methods = ["GET"])
def find_all(atype):
    value = audio.query.filter_by(type = atype)
    num_results = value.count()
    if int(num_results) != 0:
        return render_template("get.html", value = value, BytesIO = BytesIO)
    else:
        flash("File not present in Database")
        return render_template("home.html")

@app.route("/delete/<atype>/<aid>", methods = ["GET"])
def delete_file(atype,aid):
    value = audio.query.filter_by(id = int(aid), type = atype).delete()
        # num_results = value.count()
    # if int(num_results) != 0:
    # for item in value:
    #     item.delete()

    db.session.commit()
    if value != 0:
        flash("File deleted")   
    else:
        flash("File does not exists")

    return render_template("home.html")


# @app.route("/update/<atype>/<aid>", methods=["POST"])  # this sets the route to this page
# def update(atype, aid):
#     if request.method == "POST":
#         if request.files:
#             id = request.form["id"]
#             name = request.form["name"]
#             duration = request.form["duration"]
#             audio_file = request.files["audio"].read()
#             uploadtime = datetime.datetime.now()
#             host = ""
#             participants = ""
#             author = ""
#             narrator = ""

#             if request.form["type"] == "song":
#                 type = "song"
#                 print("song")

#             if request.form["type"] == "podcast":

#                 type = "podcast"
#                 host = request.form["host"]
#                 participants = request.form["participants"]

#                 print("podcast")

#             if request.form["type"] == "audiobook":
#                 type = "audiobook"
#                 author = request.form["author"]
#                 narrator = request.form["narrator"]

#                 print("audiobook")

#             print(id, name, duration, uploadtime, type)

#             found_audio = audio.query.filter_by(id = id, name = name).first()
#             found_audio2 = audio.query.filter_by(id = aid, name = aname).first()

#             if found_audio or found_audio2:
#                 if found_audio:
#                     found_audio.

#                 else:


#             else:
#                 print("File not found")

#             return render_template("home.html")

#         else:
#             print("File not found")
#             return render_template("home.html")

#     else:
#         return render_template("home.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
