from flask import request

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    #post 말고 get으로 왔을때
    else:
        return show_the_login_form()