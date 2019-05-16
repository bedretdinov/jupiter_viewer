from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from werkzeug.utils import secure_filename
from notebook import htmlNoteboook
import random
from datetime import datetime
from notebook import execNoteboook
from db import SqlLite
import time
import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/notebooks'
ALLOWED_EXTENSIONS = set(['ipynb'])

app = Flask(__name__)
app.secret_key = 'nv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    sql = SqlLite()
    notebooks = sql.fetchAll('select * from notebooks')

    return render_template('home.html', notebooks=notebooks)

@app.route('/notebook/<file>')
def notebook(file):
    filePath =  UPLOAD_FOLDER+'/{0}'.format(file)
    sql = SqlLite()
    notebook = sql.fetchOne('select * from notebooks where file="{0}"'.format(file))

    # import json
    # return json.dumps(dict(notebook))

    return  render_template('content.html', body=htmlNoteboook(filePath), notebook=notebook)

@app.route('/notebook/delete/<file>')
def delete(file):
    filePath =  UPLOAD_FOLDER+'/{0}'.format(file)
    sql = SqlLite()
    sql.query('DELETE FROM  notebooks where file="{0}"'.format(file))
    os.remove(filePath)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = request.args.get("query")

    if(search is None):
        search = ''

    sql = SqlLite()
    notebooks = sql.fetchAll('select * from notebooks where lower(name) like "%{0}%" OR lower(desc) like "%{0}%" OR lower(task) like "%{0}%"'.format(search.strip().lower()))

    return render_template('search.html', notebooks=notebooks, query=search)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        post = request.form

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/')

        if(allowed_file(file.filename)==False):
            flash('No allowed file')
            return redirect('/')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(random.randint(1,9999999))+str(random.randint(1,9999999))+str(random.randint(1,9999999))+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            record = (post.get('name'), post.get('desc'), post.get('task'), post.get('time'), filename)

            sql = SqlLite()
            sql.insert("REPLACE INTO notebooks (name,desc,task,exec_interval,file) VALUES (?,?,?,?,?)", record)

            return redirect(url_for('index'))


@app.route('/notebook/update/<file>', methods=['GET', 'POST'])
def update(file):

    sql = SqlLite()

    sql.query('''
        CREATE TABLE IF NOT EXISTS notebooks
                 (name text, desc text, task text, exec_interval int, file text, update_date text )
    ''')

    UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/notebooks/{0}'

    notebooks = sql.fetchAll("select update_date,file,exec_interval, name from notebooks where file='{0}'".format(file))

    for item in notebooks:
        execNoteboook(UPLOAD_PATH.format(item['file']))
        sql.query("UPDATE notebooks SET update_date='{date:%Y-%m-%d %H:%M:%S}'".format(date=datetime.now()))

    return redirect('/notebook/{0}'.format(file))

app.run(host='0.0.0.0', port=4000 , debug=True)

