import glob
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, session, Blueprint,render_template
from flask.globals import request
from common.database import db

#app = Flask(__name__, static_url_path="/", static_folder="resource", template_folder="template")
app = Flask(__name__,template_folder="template",static_folder="resource",static_url_path="/")
app.config['SECRET_KEY'] = os.urandom(24)

# 使用集成方式处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://数据库的账号:密码@localhost:3306/数据库名?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型的修改检测,如果为True,则会跟踪数据库的修改,及时发送信号

# 设置允许上传的文件类型和大小（这里仅示例，实际应用中请根据需求调整）
ALLOWED_EXTENSIONS = {'gif', 'jpg', 'jpeg', 'png', 'bmp', "webp"}

# 图片保存路径
UPLOAD_FOLDER = './resource/upload/'  # 替换为实际路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 实例化db对象
db.init_app(app)


def clear_cache():
    list_of_files = glob.glob(r"./resource/download/*.png")
    for f in list_of_files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting file {f}: {e}")
    print("4:00: 清空缓存完成")


# 初始化调度器
scheduler = BackgroundScheduler()
scheduler.add_job(clear_cache, 'cron', hour=4, minute=0)  # 每天4:00执行
scheduler.start()


#
# # 确保在关闭应用时停止调度器
# @app.teardown_appcontext
# def shutdown_scheduler(exception=None):
#     if scheduler.running:
#         scheduler.shutdown()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_md', methods=['POST'])
def upload_image():
    if 'editormd-image-file' not in request.files:
        return jsonify({"success": 0, "message": "No file part in the request."})

    file = request.files['editormd-image-file']

    if file.filename == '':
        return jsonify({"success": 0, "message": "No selected file."})

    if file and allowed_file(file.filename):
        # 使用时间戳生成唯一文件名
        from datetime import datetime
        from common.utility import compress_image_md

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"{timestamp}.{file.filename.split('.')[-1]}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 对图片进行压缩,并覆盖原始文件
        source = dest = "./resource/upload/" + filename
        compress_image_md(source, dest, (1200, 400))

        # 假设返回的是一个可以直接访问的URL
        url = f"/upload/{filename}"
        return jsonify({"success": 1, "message": "Image uploaded successfully.", "url": url})
    else:
        return jsonify({"success": 0, "message": "Invalid file type. Only GIF, JPG, JPEG, PNG, BMP are allowed."})


# 定义首页页面
@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/submitceshi')
def submitceshi():
    return render_template('/ceshi.html')


# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/xingyun-notebook/error-404.html')


# 定义500错误页面
@app.errorhandler(500)
def serve_error(e):
    return render_template('/xingyun-notebook/error-500.html')


# 定义自定义过滤器
def my_truncate(s, length, end='...'):
    count = 0
    new_s = ''
    if len(s) <= length:
        return s
    for c in s:
        new_s += c  # 每循环一次,将一个字符添加到new_s字符串后面
        if ord(c) <= 128:  # 如果字符的ASCII码小于128,则是英文字符
            count += 1  # 英文字符占一个字符的长度
        else:
            count += 2  # 非英文字符占两个字符的长度
        if count > length:
            break
    return new_s + end


# 注册自定义过滤器
app.jinja_env.filters.update(truncate=my_truncate)


# 定义文章类型的自定义函数,供模板页面直接调用
@app.context_processor
def inject_article_type():
    type = {
        '1': 'R语言应用',
        '2': '设计美化',
        '3': 'Python学习',
        '4': '生信分析',
        '5': '人工智能',
        '6': 'web开发',
        '7': '项目实战',
        '8': '其它',
    }
    return dict(article_type=type)


@app.context_processor
def inject_tools_type():
    type = {
        '1': 'AI工具',
        '2': '生信软件',
        '3': '生信网站',
        '4': '消息获取',
        '5': '设计美化',
        '6': '学习网站',
        '7': '其它',
    }
    return dict(tools_type=type)


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


if __name__ == '__main__':
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

    from controller.home import *

    app.register_blueprint(home)

    from controller.user_shezhi import *

    app.register_blueprint(user_shezhi)

    from controller.tools import *

    app.register_blueprint(tools)

    from controller.chatroom import *

    app.register_blueprint(chatroom)

    # 初始化SocketIO对象
    socketio.init_app(app)

    socketio.run(app,port='5555', debug=True)
    # except (KeyboardInterrupt, SystemExit):
    #     # 确保在程序退出时关闭调度器
    #     shutdown_scheduler()
