# Flask Audio Server

- This project is a Web API that simulates the behavior of an audio file server using Flask and SQL.
- API is used to upload, retrieve, update and delete audio file and its metadata from SQL database.


## Audio file Type and Structure 
  1. Song
  2. Podcast
  3. Audiobook

  ### Song file Structure:
  
    - ID : mandatory, integer, unique
    - Name of the song : mandatory, string, cannot be larger than 100 characters
    - Duration in number of seconds : mandatory, integer, positive
    - Uploaded time : mandatory, Datetime, cannot be in the past


  ### Podcast file fields:
  
    - ID : mandatory, integer, unique
    - Name of the podcast : mandatory, string, cannot be larger than 100 characters
    - Duration in number of seconds : mandatory, integer, positive
    - Uploaded time : (mandatory, Datetime, cannot be in the past)
    - Host : (mandatory, string, cannot be larger than 100 characters)
    - Participants : (optional, list of strings, each string cannot be larger than 100 characters, maximum of 10 participants possible)

  ### Audiobook file fields:
  
    - ID : mandatory, integer, unique
    - Title of the audiobook : mandatory, string, cannot be larger than 100 characters
    - Author of the title : mandatory, string, cannot be larger than 100 characters
    - Narrator : mandatory, string, cannot be larger than 100 characters
    - Duration in number of seconds : mandatory, integer, positive
    - Uploaded time : mandatory, Datetime, cannot be in the past

## Database Info

  - All the files had stored in single table.
  - ID has been set as primary key
  - Requirements of the Fields are handled in the HTML form itself
  - Audio file is stored locally and its path is stored in database
  
  ### Table Info
    -Fields : ID, Type of Audio File, Name of the file, Duration of Audio File, Upload Time, Host Name, Participants Name, Author Name, Narrator, Audio File Path 
    - Fields are based on properties mention in file structre.
    - Audio File path is String that contains path where the fiel is stored

## API Endpoints

  ### Four endpoints are implement:
    1. Create 
    2. Delete
    3. Update
    4. Get
  
  ### Create API:
    The request will have the following fields:
    - Example : `http://127.0.0.1:5000` will display home.html will dropdown menu to display appropriate form based on selected audio file type.
    - HTML form data will stored in dictionary and dictionary will be used to enter data into the SQL database
  
  ### Delete API:
    - This is delete the file matching audioFileType and audioFileID mentioned in the url if it exists and redirectted to home.html
    - The route will be in the following format: “<audioFileType>/<audioFileID>”
    - Example : `http://127.0.0.1:5000/delete/song/29` will delete file of type SONG and ID 29
 
  ### Update API
    - The route be in the following format: “<audioFileType>/<audioFileID>”
      - Example : `http://127.0.0.1:5000/update/audiobook/100` will generate a form for SONG, prefilled with ID(100) to be update in database if file exist. If file is not present in the database url will be redirected to home.html


  ### Get API
    - The route “<audioFileType>/<audioFileID>” will return the specific audio file
      - Example : `http://127.0.0.1:5000/get/song/10` will retrive and display Details and file for File type SONG and ID 10 if it exists in database else url will be redirected to home.html
    - The route “<audioFileType>” will return all the audio files of that type
      - Example : `http://127.0.0.1:5000/get/podcast` will retrive and display Details and file for all File type PODCAST present in database else url will be redirected to home.html

## HTML Structure :

  1. Home.html : Page to upload files
    - Form for a particular audio file will displayed based on the type of audio file selected in dropdown menu
    
  2. Get.html : Page to display results

  3. Update.html : Page to update exsisting files
    - Form for a particular audio file will displayed based on the url route passed.
    - Example : Form for "audiotype" and autofilled wiht id will be displayed when url mentions `http://127.0.0.1:5000/update/<type>/<id>`
   
  4. Layout.html : Contains the layout and design of the website


## Run file 

  To install dependencies : 
  `pip install -r requirements.txt`

  To run the file :
  `python app.py`

## Api is Deployed on Heroku 

  Link : https://flask-audio-server.herokuapp.com/
  
  API Calls are same as mentioned above for localhost with `https://flask-audio-server.herokuapp.com/` url instead of localhost url

***Note : Audio format issues with Safari. Run with Chrome***

***Note : If you are testing the server with Heroku link, try to uplaod smaller audio file***

