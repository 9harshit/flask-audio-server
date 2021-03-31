# Importing libaries

from flask import Flask, redirect, url_for, render_template, request, session, flash
import datetime

import os

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///audio.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# create directory to save audio file locally

uploads_dir = os.path.join(app.instance_path, "uploads")
if os.path.exists(uploads_dir):
    pass
else:
    os.makedirs(uploads_dir)

# Creating SQLalchemy database

db = SQLAlchemy(app)

# Class for a database table


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

    # Pass data into the table

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


# Create API


@app.route("/")
@app.route("/", methods=["POST", "GET"])
def home():

    session["type"] = None
    session["id"] = None

    # on POST request from HTML page data will be retireved into a dictionary
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

            # Qurey to find if file exists
            found_audio = audio.query.filter_by(id=file["id"]).first()

            # Checking if ID alrealy exists in table since ID is primary
            if found_audio:
                flash("Enter unique ID, file already exists")

            else:

                # Creating a new row in the database table
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

                # Adding row to the table

                db.session.add(aud)
                db.session.commit()

                flash("Data Entered", "info")

            return render_template("home.html")

        else:
            flash("Audio file not found")
            return render_template("home.html")

    else:
        # Rendering page
        return render_template("home.html")


# GET API


@app.route("/get/<atype>/<aid>", methods=["GET"])

# if url contains both file type and file id


def find_file(atype, aid):

    # qurey to retrieve file from database
    value = audio.query.filter_by(id=int(aid), type=atype)

    # getting number of files retrieved
    num_results = audio.query.filter_by(id=int(aid), type=atype).count()

    # if a file is retrived display the data
    if int(num_results) != 0:
        return render_template("get.html", value=value)

    # No file is retrieved
    else:
        flash("File not present in Database")
        return render_template("home.html")


# if url contains only file type


@app.route("/get/<atype>", methods=["GET"])
def find_all(atype):

    # qurey to retrieve all files of type from database
    value = audio.query.filter_by(type=atype)

    # getting count of files retrived
    num_results = value.count()

    # if files exists, data is displayed
    if int(num_results) != 0:
        return render_template("get.html", value=value)

    else:
        flash("File not present in Database")
        return render_template("home.html")


# DELETE API


@app.route("/delete/<atype>/<aid>", methods=["GET"])
def delete_file(atype, aid):

    # Retrieve and deleting file
    value = audio.query.filter_by(id=int(aid), type=atype).delete()

    db.session.commit()

    # if value is not 0 means a file was deleted and displaying message
    if value != 0:
        flash("File deleted")
    else:
        flash("File does not exists")

    # Returing to home page
    return render_template("home.html")


# UPDATE API


@app.route(
    "/update/<atype>/<aid>", methods=["POST", "GET"]
)  # this sets the route to this page
def update(atype, aid):

    if request.method == "POST":

        if request.files:

            # getting data from HTML form and storing it in dictionary

            file = {}
            file["id"] = request.form["id"]
            file["name"] = request.form["name"]
            file["duration"] = request.form["duration"]
            audio_file = request.files["audio"]

            audio_file.save(os.path.join(uploads_dir, audio_file.filename))
            path = os.path.join(uploads_dir, audio_file.filename)
            # print(path, type(path))

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

            # accesing row to be updated if row exist data will updated else error will generated and redirected to home.html
            found_audio = audio.query.filter_by(id=int(aid), type=atype).first()

            if found_audio:
                found_audio.name = file["name"]
                found_audio.duration = file["duration"]
                found_audio.uploadtime = file["uploadtime"]
                found_audio.host = file["host"]
                found_audio.participants = file["participants"]
                found_audio.author = file["author"]
                found_audio.narrator = file["narrator"]
                found_audio.audio_file = file["audio_file"]

                # db.session.add(aud)
                db.session.flush()
                db.session.commit()

                flash("File Update")

            else:
                flash("File not found")

            return render_template("home.html")

        else:
            flash("Audio File not found")
            return render_template("home.html")

    else:
        # redering page based on type of file mentioned in url
        return render_template("update.html", type=atype, id=aid)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)
