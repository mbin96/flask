# -*- coding: utf-8 -*-

from flask import Flask, url_for,request, render_template
app = Flask(__name__)

@app.route("/")
def helloworld():
    return "<h1>hello world</h1>"


# @app.route("/profile/<int:user_num>")
# def hell_num(user_num):
#     txt = f"user id : {user_num+1}"
#     txt+= "<h1>hello world</h1>"
#     return txt

# @app.route("/profile/<user_id>")
# def hell(user_id):
#     txt = f"user id : {user_id}"
#     txt+= "<h1>hello world</h1>"
#     return txt

@app.route("/profile/", methods=['POST', 'GET'])
def profile(user = None):
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # if not username and not email :
        #     return add_profile(request.form)
    else:
        error = 'Invalid username and email'
    return render_template('profile.html', error = error)

# jinsha
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



if __name__ == "__main__":
    with app.test_request_context():
        app.run(debug=True)