import random

from flask import Blueprint, session, render_template, jsonify, request,Flask

from common.utility import handle_upload, handle_upload_user
from model.user_shezhi import Shezhi
from model.users import Users
from model.tb_follow import Follow
import main

home = Blueprint('home', __name__)




# 检查是否关注
def follow_status(user_id, followed_vip_id):
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        follow = Follow()
        follow_status = follow.get_follow_status(vip_id=user_id, followed_vip_id=followed_vip_id)
        return follow_status


def find_by_user_id(user_id):
    user = Users()
    result = user.find_by_userid(user_id)
    return result


@home.route("/get_follow_status", methods=["GET"])
def get_follow_status():
    user_id = session.get('userid')
    followed_vip_id = request.form.get('followed_vip_id')
    result = follow_status(user_id, followed_vip_id)
    return jsonify({'follow_status': result})


@home.route('/home/<int:user_id>')
def home_index(user_id):
    user = Users()
    follow = Follow()
    shezhi = Shezhi()
    settings = shezhi.get_message_from_editoruser(user_id)
    userid = session.get('userid')
    user_at = user.find_by_userid(user_id)
    user_ziji = user.find_by_userid(userid=userid)
    # find_by_userid = user.find_by_userid(userid=user_id)
    user_all_6 = follow.find_random_users(num=6)
    user_admin = user.find_by_admin()
    folllow_by_id = follow.get_follow_by_userid(userid=user_id)
    return render_template('/home/index.html', user_ziji=user_ziji, user_all=user_all_6, user_admin=user_admin
                           , folllow_by_id=folllow_by_id, follow_status=follow_status, user_id=user_id,
                           find_by_user_id=find_by_user_id, settings=settings,user_at=user_at)


@home.route('/youke_home')
def youke_home():
    user = Users()
    follow = Follow()
    user_all_6 = follow.find_random_users(num=6)
    user_admin = user.find_by_admin()
    return render_template('/home/youke.html', user_all=user_all_6, user_admin=user_admin
                           , follow_status=follow_status,
                           find_by_user_id=find_by_user_id)


# 获取搜索用户的id
@home.route("/home/search", methods=["GET", "POST"])
def search():
    keyword = request.form.get("keyword")
    user = Users()
    result = user.find_userid_by_nickname(keyword)
    result_dict = {
        "userid": result.userid,
        # 可根据实际情况添加其他属性
    }

    if result:
        return jsonify(success=True, result=result_dict)
    else:
        return jsonify(success=False)


# 获取用户的昵称
@home.route("/home/nickname", methods=["GET"])
def get_nickname():
    user = Users()
    result = user.find_all_users_nickname()

    # 将查询结果转换为列表
    nickname_list = [row.nickname for row in result]

    result_dict = {
        "nickname": nickname_list,
        # 可根据实际情况添加其他属性
    }
    return jsonify(result_dict)




# 新增关注信息
@home.route('/home/follow', methods=['POST'])
def follow():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        vip_id = session['userid']
        followed_vip_id = request.form.get('followed_vip_id')
        # 判断是否已存在相同的关注信息
        if not Follow().query_follow(vip_id, followed_vip_id):
            # 如果不存在，则插入新记录
            Follow().insert_follow(vip_id, followed_vip_id)
        else:
            Follow().switch_status(vip_id, followed_vip_id)
        return 'success'


# 更新关注信息
@home.route('/home/unfollow', methods=['POST'])
def unfollow():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        vip_id = session['userid']
        followed_vip_id = request.form.get('followed_vip_id')
        Follow().switch_status(vip_id, followed_vip_id)
        return 'success'


# 更新用户设置
@home.route('/update_user', methods=['POST'])
def update_user():
    avatar = request.form.get('avatar')
    nickname = request.form.get('nickname')
    introduce = request.form.get('introduce')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        if avatar:
            avatar = handle_upload_user(avatar)
        user = Users()
        try:
            user.update_user(userid=session['userid'], avatar=avatar, nickname=nickname, introduce=introduce)
            return 'add-pass'
        except:
            return 'add-fail'
