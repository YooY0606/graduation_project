#!/usr/bin/env python3
#處理flask當中呼叫不同網址的任務
from app import app, handler
from flask import request, abort,render_template, redirect, url_for
from linebot.exceptions import InvalidSignatureError
from app.custom_models import CallDatabase

@app.route('/')
def user():
	return render_template("user.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        nm = request.form['暱稱']
        blood = request.form['血型']
        year = request.form['出生年']
        gender = request.form['性別']
        place = request.form['地區']
        other = request.form['備註']
        user_id = request.form['userid']
        CallDatabase.insert_userlist(user_id,nm,blood,year,gender,place,other)
        CallDatabase.r_leaderboard_n(user_id,nm)
        msg = "資料成功新增!"
        return render_template("result.html",msg = msg)
    
@app.route('/record')
def record():
	return render_template("record.html")
    
@app.route('/r_result',methods = ['POST', 'GET'])
def r_result():
    if request.method == 'POST':
        year = request.form['時間']
        way = request.form['捐血方式']
        user_id = request.form['userid']
        CallDatabase.record(user_id,year,way)
        CallDatabase.r_leaderboard(user_id,way)
        msg = "資料成功新增!"
        return render_template("r_result.html",msg = msg)


@app.route('/r_record',methods = ['POST', 'GET'])
def r_record():
    user_id = request.form.get('userid')
    dataclip = CallDatabase.r_record(user_id)
    return render_template("r_record.html",dataclip=dataclip)

@app.route('/list',methods = ['POST', 'GET'])
def list():
    user_id = request.form.get('userid')
    dataclip = CallDatabase.read_userlist(user_id)
    return render_template("list.html",dataclip=dataclip)

@app.route('/lb_250',methods = ['POST', 'GET'])
def leaderboard_250():
    dataclip = CallDatabase.read_leaderboard()
    return render_template("lb_250.html",dataclip=dataclip)

@app.route('/lb_500',methods = ['POST', 'GET'])
def leaderboard_500():
    dataclip = CallDatabase.read_leaderboard()
    return render_template("lb_500.html",dataclip=dataclip)

@app.route('/lb_one',methods = ['POST', 'GET'])
def leaderboard_one():
    dataclip = CallDatabase.read_leaderboard()
    return render_template("lb_one.html",dataclip=dataclip)

@app.route('/lb_two',methods = ['POST', 'GET'])
def leaderboard_two():
    dataclip = CallDatabase.read_leaderboard()
    return render_template("lb_two.html",dataclip=dataclip)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'