from flask import session, request
from main import app
from controller.chatroom import chatroom, socketio, Users

# 定义全局拦截器,实现自动登录
@app.before_request
def before():
    url = request.url
    pass_list = ['/login', '/user', '/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.css') or url.endswith('.jpg'):
        pass

    if session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username is not None and password is not None:
            users = Users()
            result = users.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = result[0].username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role
                session['avatar'] = result[0].avatar

#     # if __name__ == "__main__":




from controller.index import *

app.register_blueprint(index)

from controller.user import *

app.register_blueprint(user)

from controller.article import *

app.register_blueprint(article)

from controller.favorite import *

app.register_blueprint(favorite)

from controller.comment import *

app.register_blueprint(comment)

from controller.ueditor import *

app.register_blueprint(ueditor)

from controller.admin import *

app.register_blueprint(admin)

from controller.ucenter import *

app.register_blueprint(ucenter)

from controller.py_echarts import *

app.register_blueprint(py_echarts)

from controller.home import home

app.register_blueprint(home)

from controller.user_shezhi import *

app.register_blueprint(user_shezhi)

from controller.tools import *

app.register_blueprint(tools)

from controller.chatroom import *

app.register_blueprint(chatroom)



# 初始化SocketIO对象
socketio.init_app(app)




#开发环境和生产环境不一样，如果是在开发环境（即在本地）,那么请将下面这行注释取消。
# socketio.run(app, debug=True, host='0.0.0.0', port=1212, allow_unsafe_werkzeug=True)


