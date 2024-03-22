import math
import random

from flask import Blueprint, render_template, session, request

from common.utility import handle_upload, handle_upload_tools
from model.article import Article
from model.tools import Tools
from model.users import Users

tools = Blueprint('tools', __name__)


# 根据tools_type查询tools表中二级分类信息
def get_tools_by_type(type):
    tools = Tools()
    result = tools.get_tools_message_by_type(type)
    return result


# 根据tools_type查询tools表中一级分类信息
def get_tools_by_majortype(majortype):
    tools = Tools()
    result = tools.get_tools_message_by_major_category(majortype)
    return result


# 根据tools_type命名对应的分类信息
from common.utility import ming_tools_by_type


# 根据工具的分类随机查询6条工具信息（充当相关导航）
def get_tools_random_6(type):
    tools = Tools()
    result = tools.get_tools_random_6_by_type(type)
    return result


# 工具仓库首页接口
@tools.route('/tools', methods=['GET', 'POST'])
def tools_submit():
    return render_template('/gongjuku/index.html', get_tools_by_type=get_tools_by_type,
                           get_tools_by_majortype=get_tools_by_majortype, ming_tools_by_type=ming_tools_by_type)


# 工具提交接口
@tools.route('/tools/submit', methods=['GET', 'POST'])
def tools_index():
    return render_template('/gongjuku/submit.html')


# 工具详情介绍接口
@tools.route('/tools/jieshao/<int:tools_id>', methods=['GET', 'POST'])
def tools_jieshao(tools_id):
    tools = Tools()
    tools_at = tools.get_tools_message_by_id(tools_id)
    return render_template('/gongjuku/jieshao.html', tools_id=tools_id, tools_at=tools_at, ming_tools_by_type=
    ming_tools_by_type, get_tools_random_6=get_tools_random_6)


# 工具二级分类后的大页面接口
@tools.route('/tools/type/<int:type>', methods=['GET', 'POST'])
def tools_type(type):
    return render_template('/gongjuku/fenlei.html', type=str(type), ming_tools_by_type=ming_tools_by_type,
                           get_tools_by_type=get_tools_by_type, get_tools_by_majortype=get_tools_by_majortype)


# 所有工具后的大页面接口
@tools.route('/tools/type/all', methods=['GET', 'POST'])
def tools_type_all():
    tools = Tools()
    all_tools = tools.get_tools_message()
    return render_template('/gongjuku/all_tools.html', all_tools=all_tools, ming_tools_by_type=ming_tools_by_type)


# 新建工具接口
@tools.route('/insert_tools', methods=['POST'])
def insert_tools():
    tools_avatar = request.form.get('tools_avatar')
    tools_name = request.form.get('tools_name')
    tools_introduce = request.form.get('tools_introduce')
    tools_link = request.form.get('tools_link')
    tools_type = request.form.get('tools_type')
    tools_jianjie = request.form.get('tools_jianjie')
    tools_userid = session.get('userid')
    tools_user_nickname = session.get('nickname')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        tools_avatar = handle_upload_tools(tools_avatar)
        tools = Tools()
        try:
            tools.insert_tools_message(tools_avatar=tools_avatar, tools_name=tools_name,
                                       tools_introduce=tools_introduce,
                                       tools_link=tools_link,
                                       tools_type=tools_type, tools_jianjie=tools_jianjie,
                                       tools_userid=tools_userid,
                                       tools_user_nickname=tools_user_nickname)
            return 'add-pass'
        except:
            return 'add-fail'


# 编辑工具接口
@tools.route('/editor_tools', methods=['POST'])
def editor_tools():
    tools_id = request.form.get('tools_id')
    tools_avatar = request.form.get('tools_avatar')
    tools_name = request.form.get('tools_name')
    tools_introduce = request.form.get('tools_introduce')
    tools_link = request.form.get('tools_link')
    tools_type = request.form.get('tools_type')
    tools_jianjie = request.form.get('tools_jianjie')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        tools_avatar = handle_upload_tools(tools_avatar)
        tools = Tools()
        try:
            tools.update_tools_message(tools_id=tools_id, tools_avatar=tools_avatar, tools_name=tools_name,
                                       tools_introduce=tools_introduce,
                                       tools_link=tools_link,
                                       tools_type=tools_type, tools_jianjie=tools_jianjie,
                                       )
            return 'add-pass'
        except:
            return 'add-fail'



# 删除工具信息
@tools.route('/tools/delete', methods=['POST'])
def delete_tools():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        tools = Tools()
        tools_id = int(request.form.get('tools_id'))
        success = tools.delete_tools_message(tools_id)
        if success:
            # 删除成功
            return 'delete-success'
        else:
            # 删除失败
            return 'delete-fail'


#审核工具接口
@tools.route('/tools/checked', methods=['POST'])
def checked_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            tools_id = int(request.form.get('tools_id'))
            tools = Tools()
            success = tools.switch_checked(tools_id=tools_id)
            if success == 1:
                # 已经审核
                return 'checked-success'
            elif success == 0:
                # 还未审核
                return 'checked-cancel'
        else:
            return 'perm-denied'

