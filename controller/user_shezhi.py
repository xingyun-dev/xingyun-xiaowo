import random

from flask import Blueprint, session, jsonify, render_template, request

from common.utility import handle_upload
from model.user_shezhi import Shezhi
from model.users import Users

user_shezhi = Blueprint('user_shezhi', __name__)


# 新建外链
@user_shezhi.route('/editor_user_shezhi', methods=['POST'])
def editor_user_shezhi():
    wang_img = request.form.get('wang_img')
    wang_name = request.form.get('wang_name')
    wang_user_name = request.form.get('wang_user_name')
    wang_lian = request.form.get('wang_lian')
    wang_user_avatar = request.form.get('wang_user_avatar')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        if len(wang_img) > 10:
            wang_img = handle_upload(wang_img)
            wang_user_avatar = handle_upload(wang_user_avatar)
        else:
            # 生成1到6之间的随机整数
            random_int = random.randint(1, 6)
            wang_img = 'wang_img_%d.png' % random_int
            wang_user_avatar = 'wang_user_avatar_%d.png' % random_int
        shezhi = Shezhi()
        try:
            shezhi.insert_message_to_shezhi(wang_img=wang_img, wang_name=wang_name,
                                            wang_user_name=wang_user_name, wang_lian=wang_lian,
                                            wang_user_avatar=wang_user_avatar)
            return 'add-pass'
        except:
            return 'add-fail'

# 更新外链设置
@user_shezhi.route('/update_user_shezhi', methods=['POST'])
def update_user_shezhi():
    wang_img = request.form.get('wang_img')
    wang_name = request.form.get('wang_name')
    wang_user_name = request.form.get('wang_user_name')
    wang_lian = request.form.get('wang_lian')
    wang_user_avatar = request.form.get('wang_user_avatar')
    shezhi_id = request.form.get('shezhi_id')


    if session.get('userid') is None:
        return 'perm-denied'
    else:

        if wang_img:
            wang_img = handle_upload(wang_img)

        if wang_user_avatar:
            wang_user_avatar = handle_upload(wang_user_avatar)
        shezhi = Shezhi()
        try:
            shezhi.update_message_from_shezhi(shezhi_id=shezhi_id, wang_img=wang_img, wang_name=wang_name,
                                              wang_user_name=wang_user_name, wang_lian=wang_lian,
                                              wang_user_avatar=wang_user_avatar)
            return 'add-pass'
        except:
            return 'add-fail'



# 删除编辑设置信息
@user_shezhi.route('/editor_user_shezhi/delete', methods=['POST'])
def delete_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        shezhi = Shezhi()
        shezhi_id = int(request.form.get('shezhi_id'))
        success = shezhi.delete_message_from_shezhi(shezhi_id)
        if success:
            # 删除成功
            return 'delete-success'
        else:
            # 删除失败
            return 'delete-fail'
