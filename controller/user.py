import hashlib
import os
import re

from flask import Blueprint, make_response, session, request, url_for, jsonify

from common.redisdb import redis_connect
from common.utility import imagecode, gen_email_code, send_email

from model.users import Users
import json

user = Blueprint('user', __name__)

font_dir = 'common'  # 字体文件所在的目录
font_filename = 'Arial.ttf'  # 字体文件名
font_path = os.path.join(font_dir, font_filename)  # 构建完整路径


@user.route('/vcode')
def vcode():
    bstring, code = imagecode(font_path=font_path).get_code()
    response = make_response(bstring)
    response.headers['content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response


@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match(r'.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code  # 保存邮箱验证码到session中
        return 'send-pass'
    except:
        return 'send-fail'


@user.route('/user', methods=['POST'])
def register():
    users = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    latitude = request.form.get('latitude').strip()
    longitude = request.form.get('longitude').strip()
    ecode = request.form.get('ecode').strip()
    if latitude == "null":
        latitude = None
    if longitude =='null':
        longitude = None

    # 校验邮箱验证码是否正确
    if ecode != session.get('ecode'):
        return 'ecode-error'
    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'

    # 验证用户名是否已经存在
    elif len(users.find_by_username(username)) > 0:
        return 'username-exist'

    else:
        # 实现注册功能
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        result = users.do_register(username, password, latitude, longitude)
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = result.username
        session['nickname'] = result.nickname
        session['role'] = result.role

        return 'reg-pass'


@user.route('/reset', methods=['POST'])
def reset():
    users = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()

    # 校验邮箱验证码是否正确
    if ecode != session.get('ecode'):
        return 'ecode-error'
    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'
    else:
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        user = users.do_reset(username, password)  # 调用密码重置方法
        if user:
            # 密码重置成功
            return 'reset-pass'
        else:
            # 用户不存在，密码重置失败
            return 'user-not-found'

   
@user.route('/login', methods=['POST'])
def login():
    users = Users()
    latitude = request.form.get('latitude').strip()
    longitude = request.form.get('longitude').strip()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()  # 图形验证码
    
    if latitude == "null":
        latitude = None
    if longitude =='null':
        longitude = None

    # 校验图形验证码是否正确
    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'
    else:
        # 实现登录功能
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        users.update_user_location(latitude, longitude, username)
        result = users.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = result[0].username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            
            # 将cookie写入浏览器
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
            response.set_cookie('password', password, max_age=7 * 24 * 3600)
            return response

        else:
            return 'login-fail'


@user.route('/logout')
def logout():
    # 清空session,页面跳转
    session.clear()
    response = make_response('注销并进行重定向', 302)
    # response.headers['Location'] = url_for('index.home')
    response.headers['Location'] = "/"
    response.delete_cookie('username')
    response.set_cookie('password', '', max_age=0)
    return response


# 用户注册时生成邮箱验证码并保存到缓存中
@user.route('/redis/code', methods=['POST'])
def redis_ccode():
    username = request.form.get('username').strip()
    code = gen_email_code()
    red = redis_connect()  # 连接到redis服务器
    red.set(username, code)
    red.expire(username, 300)  # 设置username变量的有效期为5min
    # 设置好缓存变量的过期时间后,发送邮件完成处理,此处代码略

    return 'done'


# 根据用户的注册邮箱去缓存中查找验证码进行验证
@user.route('/redis/reg', methods=['POST'])
def redis_reg():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').lower().strip()

    try:
        red = redis_connect()  # 连接到redis服务器
        redis_code = red.get(username).lower()
        if redis_code == ecode:
            return '验证码正确'
            # 开始进行注册，此处代码略
        else:
            return '验证码错误'

    except:
        return '验证码已经失效'


#
# @user.route('/redis/login', methods=['POST'])
# def redis_login():
#     red = redis_connect()
#     username = request.form.get('username').strip()
#     password = request.form.get('password').strip()
#     password = hashlib.md5(password.encode()).hexdigest()
#
#     result = red.get('users')
#     list = eval(result)
#
#     for row in list:
#         if row['username'] == username and row['password'] == password:
#             return '用户名和密码正确,登录成功'
#
#     return '登录失败'

#
# @user.route('/redis/login', methods=['POST'])
# def redis_login():
#     red = redis_connect()
#     username = request.form.get('username').strip()
#     password = request.form.get('password').strip()
#     password = hashlib.md5(password.encode()).hexdigest()
#
#     try:
#         result = red.get(username)
#         # user = eval(result)
#         # if password == user['password']:
#         if password == result:
#             return '密码正确,登录成功'
#         else:
#             return '密码错误'
#     except:
#         return '用户名不存在'
#


# @user.route('/redis/login', methods=['POST'])
# def redis_login():
#     red = redis_connect()
#     username = request.form.get('username').strip()
#     password = request.form.get('password').strip()
#     password = hashlib.md5(password.encode()).hexdigest()

#     try:
#         result = red.hget('users_hash', username)
#         # user = eval(result)
#         if password == result:
#             return '密码正确,登录成功'
#         else:
#             return '密码错误'
#     except:
#         return '用户名不存在'


@user.route('/loginfo')
def loginfo():
    # 没有登录,则直接响应一个空JSON给前端,用于前端判断
    if session.get('islogin') is None:
        return jsonify(None)
    else:
        # 登录了,则响应用户信息给前端
        dict = {}
        dict['islogin'] = session.get('islogin')
        dict['userid'] = session.get('userid')
        dict['username'] = session.get('username')
        dict['nickname'] = session.get('nickname')
        dict['role'] = session.get('role')
        return jsonify(dict)


# 删除用户
@user.route('/user/delete', methods=['POST'])
def checked_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or user.role == 'admin':
            users = Users()
            userid = int(request.form.get('userid'))
            success = users.delete_by_user_id(userid)
            if success:
                # 删除成功
                return 'delete-success'
            else:
                # 删除失败
                return 'delete-fail'
        else:
            return 'perm-denied'
