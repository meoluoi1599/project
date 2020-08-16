from flask import Flask, render_template,jsonify, json, request,send_from_directory
# from flask_socketio import SocketIO,send,emit,join_room,leave_room
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# from flask_mail import Mail, Message

# from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['JWT_SECRET_KEY'] = 'Meow meow meow'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)


# socketio = SocketIO(app,cors_allowed_origins="*")
cors = CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

FILE_DIRECTORY = "D://save_file"
if not os.path.exists(FILE_DIRECTORY):
   os.makedirs(FILE_DIRECTORY)

import mymodel 
from mymodel import database
database = database() 

#login for users
@app.route('/login', methods = ['POST'])
def login():
    token = ''
    username = request.json.get('username')
    get_password = request.json.get('password')
    account = database.login((username,))
    name =''
    if account is None:
        return jsonify({'token':''})
    role = account['role']
    if account is not None:
        print(account)
        if role == 'user':
            db_password = account['user_pw']
            name = account['nick_name']
        elif role == 'manager':
            db_password = account['manager_pw']
            name = account['manager_nick_name']
    if bcrypt.check_password_hash(db_password, get_password):
        token = create_access_token(identity = username)
    return jsonify({'token':token,'role':role,'username':username, 'name':name})
    
# create account for user
@app.route('/signup', methods = ['POST'])
def signup():
    # get data from frontend
    username = request.json.get('username')
    password = request.json.get('password')
    nick_name = request.json.get('fullname')
    email = request.json.get('email')
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password)
    # get data from database.signup of mymodel.py
    values = (username,password,email,nick_name)
    new_account = database.signup(values)
    return jsonify({'new_account': new_account})

# get list books
@app.route('/', methods = ['GET'])
def getBooks():
    result = database.getBooks()
    story_id = database.Column('story_id',database.Integer, primary_key=True)
    story_title = database.Column('story_title',database.String(200), null = False)
    story_description = database.Column('story_description',database.String(500))
    story_img = database.Column('story_img',database.String(200))
    story_part = database.Column('story_part',database.Integer)
    author_id = database.Column('author_id',database.String(200), null = False)

    result = database.getBooks.query.paginate(page = page,per_page=1).items
    re = []
    for story in result:
        json_result = (story.story_id,story.story_title, story.story_description, story.story_img, story.story_part, story.author_id)
        re.append(json_result)
    return jsonify(re)

# get list catagoty
@app.route('/category', methods = ['GET'])
def getCategory():
    result = database.getCategory()
    return jsonify({'result':result})

# create story
@app.route('/create_story', methods = ['POST']) 
def createStory():
    title_story = request.json.get('title_story')
    story_description = request.json.get('story_description')
    story_img = request.json.get('story_img')
    author_id = request.json.get('user_id')
    values = (title_story, story_description, story_img, author_id)
    result = database.createStory(values)
    return jsonify({'result': result})

# get chapter
@app.route('/chapter', methods = ['GET'])
def getChapter():
    result = database.getChapter()
    return jsonify({'result': result})

# upload chapter
@app.route('/upload_chapter', methods = ['POST']) 
def uploadChapter():
    chapter_name = request.json.get('chapter_name')
    chapter_content = request.json.get('chapter_content')
    story_id = request.json.get('story_id')
    upload_date = request.json.get('upload_date')
    values = (chapter_name, chapter_content, story_id, upload_date)
    result = database.createStory(values)
    return jsonify({'result': result})
    
if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000)
    #app.run(port=5000)
    app.run(host="0.0.0.0",port=5000)
    # app.run(host="192.168.0.103", port=5000)