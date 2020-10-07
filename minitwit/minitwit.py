from __future__ import with_statement
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash
from werkzeug.security import check_password_hash, generate_password_hash


#configration
DATABASE  = 'minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'pripara'

# app create
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent = True)

def connect_db():
    """returns a new connection to the datsbase"""
    return sqlite3.connect(app.config['DATABASE'])

def query_db(quert, args=(), one = False):
    cur = g.db.execute(query,args)
    rv = [dict((cur.description[idx][0], value) 
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.spl', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?', [session['user_id']], one = True)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()











if __name__ == '__main__':
    init_db()
    app.run()





