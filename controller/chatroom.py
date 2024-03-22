import time

from flask import Blueprint, request, abort, render_template, session, redirect, url_for, flash
from flask_cors import CORS

from flask_socketio import emit, join_room, SocketIO

from model.tb_follow import Follow
from model.users import Users
from model.chatroom import Message

chatroom = Blueprint('chaom', __name__)
CORS(chatroom)
socketio = SocketIO(cors_allowed_origins="*")


def find_userid(userid):
    result = Users().find_by_userid(userid)
    return result


# 删除发送的信息
@chatroom.route("/delete-message", methods=['POST'])
def delete_message():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            message_id = int(request.form.get('message_id'))
            success = Message().delete_user_message(message_id)
            if success:
                # 删除成功
                return 'delete-success'
            else:
                # 删除失败
                return 'delete-fail'
        else:
            return 'perm-denied'


# 聊天室首页
@chatroom.route("/chatroom/index", methods=['POST', 'GET'])
def chatroom_index():
    if session.get('islogin') is None:
        return redirect(url_for("index"))
    else:
        user_one = Users().find_by_userid(session.get('userid'))
        # user = Users().find_all_users_all()
        follow = Follow()
        user_guanzhu = follow.get_follow_users_with_details(userid=session.get('userid'))
        return render_template("/chatroom/index.html", user_guanzhu=user_guanzhu, user_one=user_one)


@chatroom.route("/chatroom/chatroom", methods=['POST', 'GET'])
def chatroom_chatroom():
    if session.get('islogin') is None:
        return redirect(url_for('index'))
    else:
        user_id = session.get('userid')
        message = Message()
        message_result = message.get_messages()
        # users = Users().find_all_users_all()
        follow = Follow()
        user_guanzhu = follow.get_follow_users_with_details(userid=session.get('userid'))
        avatar = message.get_at_avatar(user_id=user_id)
        # nickname = session.get('nickname')
        return render_template("/chatroom/chatroom.html", message_result=message_result, user_guanzhu=user_guanzhu,
                               avatar=avatar)


# 一对一聊天室(私信)
@chatroom.route('/chatroom/<int:userid>--<int:follow_userid>', methods=['POST', 'GET'])
def chatroom_one(userid, follow_userid):
    if session.get('islogin') is None or userid != session.get('userid'):
        return redirect(url_for('index'))
    else:
        follow = Follow()
        message = Message()
        message_one = message.get_messages_onebyone(communicate_userid=follow_userid)
        user_guanzhu = follow.get_follow_users_with_details(userid=session.get('userid'))
        avatar = message.get_at_avatar(user_id=userid)
        return render_template("/chatroom/chatroom_one.html", user_guanzhu=user_guanzhu,
                               avatar=avatar, userid=userid, follow_userid=follow_userid, message_one=message_one,
                               find_userid=find_userid)


# 个人的私信接受展示
@chatroom.route('/sixin/<int:userid>')
def chatroom_sixin(userid):
    if session.get('islogin') is None or userid != session.get('userid'):
        return redirect(url_for('index'))
    else:
        message = Message()
        follow = Follow()
        avatar = message.get_at_avatar(user_id=userid)
        message_sixin = message.get_message_all_follow_user()
        user_guanzhu = follow.get_follow_users_with_details(userid=session.get('userid'))

        return render_template('/chatroom/chat_sixin.html', user_guanzhu=user_guanzhu, message_sixin=message_sixin,
                               avatar=avatar, userid=userid)


# 连接聊天室
@socketio.on('connect', namespace='/chatroom/chatroom')
def connect():
    print('连接成功!!')


# 加入房间
@socketio.on('joined', namespace='/chatroom/chatroom')
def joined(information):
    # 'joined'路由是传入一个room_name,给该websocket连接分配房间,返回一个'status'路由
    room_name = 'chat room'
    user_name = session.get('nickname')
    print(user_name)
    join_room(room_name)
    emit('status', {'server_to_client': user_name + ' enter the room'}, 'room=room_name')


# 接收聊天信息
@socketio.on('text', namespace='/chatroom/chatroom')
def text(information):
    text = information.get('text')
    nick_name = session.get('nickname')  # 获取用户名称
    user_id = session.get('userid')  # 获取用户ID
    communicate_user = request.form.get('communicate_user')

    Message().insert_message(content=text, communicate_userid=communicate_user)  # 将聊天信息插入数据库，更新数据库
    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    avatar = Message().get_at_avatar(user_id=user_id)  # 获取用户头像

    # 返回聊天信息给前端
    emit('message', {
        'nickname': nick_name,
        'text': text,
        'create_time': create_time,
        'avatar': avatar,
    })
    

@socketio.on('connect', namespace='/chatroom/chatroom_one')
def handle_user_info():
    print('连接成功!!!!!!')


@socketio.on('text', namespace='/chatroom/chatroom_one')
def text_one(information):
    text = information.get('text')
    nick_name = session.get('nickname')  # 获取用户名称
    user_id = session.get('userid')  # 获取用户ID
    follow_userid = information.get('follow_userid')

    # 这里处理数据库操作和消息存储
    Message().insert_message(content=text, communicate_userid=follow_userid)
    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    avatar = Message().get_at_avatar(user_id=user_id)  # 获取用户头像

    # 发送消息给接收者
    emit('message', {
        'nickname': nick_name,
        'text': text,
        'create_time': create_time,
        'avatar': avatar,
        'userid': user_id,
    })


# 连接主页
@socketio.on('Iconnect', namespace='/chatroom/index')
def Iconnect():
    print('连接成功')
