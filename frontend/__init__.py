

from flask import Flask, session, flash, render_template, redirect, url_for, request

from flask_bootstrap import Bootstrap
import pickle
from os import path
import frontend.config

static_path = '/' + config.base_dir + '/static'
app = Flask(__name__, static_path = static_path)
Bootstrap(app)

app.secret_key = config.secret_key

import frontend.content

@ app.route('/')
def _redirect():
    if not config.development:
        return redirect(config.main_url + '/' + config.base_dir)
    return redirect(request.base_url + url_for('show')[1:])

@ app.route('/' + config.base_dir + '/', strict_slashes=False)
def show():
    try:
        if session['key'] == config.password:
            return render_template("index.html", videos=content.videos)
        else:
            return render_template("login.html")
    except:
        return render_template("login.html")


@ app.route('/' + config.base_dir +'/login',  methods=['POST'])
def session_begin():
    if config.development or request.form['key'] == config.password:
        session['key'] = config.password
    else:
        flash("Falsches Passwort!")
    return redirect(request.referrer)


@ app.route('/' + config.base_dir + '/detail/<id>')
def detail(id):
    if int(id) < 0:
        if not config.development:
            return redirect(config.main_url + url_for('detail', id=len(content.videos) -1))
        else:
            return redirect(url_for('detail', id=len(content.videos) -1))
        
    if int(id) == len(content.videos):
        if not config.development:
           return redirect(config.main_url + url_for('detail', id=0))
        else:
            return redirect(url_for('detail', id=0))
        
    try:
        if session['key'] == config.password:
            return render_template("detail.html", video=content.videos[int(id)], id=id, config=config)
        else:
            return render_template("login.html")
    except:
        return render_template("login.html")

if __name__ == "__main__":
    app.run()

