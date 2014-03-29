import os
from . import storage
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def main():
    return "Dude, Programming is Magic!"


@app.route('/poster', methods=['GET', 'POST'])
def poster():
    if request.method == 'POST':
        storage.store_post(str(request.form.get('post')))
    return render_template('base.html', posts=storage.list_posts())
