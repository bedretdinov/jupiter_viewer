from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from werkzeug.utils import secure_filename
from notebook import htmlNoteboook
import random
import datetime
from notebook import execNoteboook
from db import Notebooks
import time
import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/notebooks'
ALLOWED_EXTENSIONS = set(['ipynb'])

app = Flask(__name__)
app.secret_key = 'nv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    notebooks = Notebooks.select()
    return render_template('home.html', notebooks=notebooks)


@app.route('/notebook/<file>')
def notebook(file):
    filePath = UPLOAD_FOLDER + '/{0}'.format(file)
    notebooks = Notebooks.select().where(Notebooks.file == file)
    notebooks_list = Notebooks.select()
    for nb in notebooks:
        notebook = nb

    return render_template('content.html', body=htmlNoteboook(filePath), notebook=notebook, notebooks = notebooks_list)


@app.route('/notebook/delete/<file>')
def delete(file):
    filePath = UPLOAD_FOLDER + '/{0}'.format(file)
    query = Notebooks.delete().where(Notebooks.file == file)
    query.execute()
    os.remove(filePath)
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    search = request.args.get("query")

    if (search is None):
        search = ''

    notebooks = Notebooks.select().where(
        (Notebooks.name.contains(search.strip())) |
        (Notebooks.desc.contains(search.strip())) |
        (Notebooks.task.contains(search.strip()))
    )

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

        if (allowed_file(file.filename) == False):
            flash('No allowed file')
            return redirect('/')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = post.get('name')+".ipynb"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            huey = Notebooks()
            huey.name = post.get('name')
            huey.desc = post.get('desc')
            huey.task = post.get('task')
            huey.exec_interval = post.get('time')
            huey.file = filename
            huey.update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            huey.save()

            return redirect(url_for('index'))


@app.route('/notebook/update/<file>', methods=['GET', 'POST'])
def update(file):

    UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/notebooks/{0}'
    notebook_list = Notebooks.select().where(Notebooks.file == file).execute()



    for item in notebook_list:

        execNoteboook(UPLOAD_PATH.format(item.file))
        query = (Notebooks.update(
                    update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ).where(Notebooks.file == file))
        query.execute()
    return redirect('/notebook/{0}'.format(file))


app.run(host='0.0.0.0', port=4000, debug=True)
