
from flask import *
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from bson import ObjectId
from random import shuffle
import pymongo
import os
from dotenv import load_dotenv


# loading environment from .env file

app_path = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(app_path, '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
Bootstrap(app)
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jumble', methods = ['GET', 'POST'])
def jumble():
    if request.method == 'GET':
        return render_template('jumble.html')
    elif request.method == 'POST':
        word = request.form['word'].strip().upper()
        mongo.db.jumble.insert_one({'word': word})
        return redirect('/')

@app.route('/figureout', methods = ['GET', 'POST'])
def figureout():
    word_docs = list(mongo.db.jumble.find())
    if request.method == 'GET':
        if not word_docs:
            return render_template('message_template.html')
        for word_doc in word_docs:
            word = list(word_doc['word'])
            shuffle(word)
            word_doc['word'] = ''.join(word)
        return render_template('figureout.html', word_docs = word_docs)
    elif request.method == 'POST':
        score = 0 
        for word_id, word_doc in zip(request.form, word_docs):
            if request.form[word_id].strip().upper() == word_doc['word']:
                score += 1
        return render_template('score.html', score = score)

if __name__ == '__main__':
    app.run(debug = True)

