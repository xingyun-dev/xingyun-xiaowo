import math

from flask import Blueprint, render_template, session

from model.article import Article
from model.tools import Tools
from model.users import Users

from controller.index import is_markdown

admin = Blueprint('admin', __name__)


# 模块拦截器
@admin.before_request
def before_admin():
    if session.get('islogin') != 'true' or session.get('role') != 'admin':
        return 'perm-denied'


# 为系统管理首页填充文章列表,并绘制分页栏
@admin.route("/admin")
def sys_admin():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    article = Article()
    result = article.find_all_except_drafted(0, pagesize)
    total = math.ceil(article.get_count_all_except_drafted() / pagesize)
    return render_template('/xingyun-notebook/system-admin.html', page=1, result=result, total=total, userid=userid,
                           avatar=avatar, nickname=nickname,is_markdown=is_markdown)


# 为系统管理首页的文章列表进行分页查询
@admin.route("/admin/article/<int:page>")
def admin_article(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    article = Article()
    result = article.find_all_except_drafted(start, pagesize)
    total = math.ceil(article.get_count_all_except_drafted() / pagesize)
    return render_template('/xingyun-notebook/system-admin.html', page=page, result=result, total=total, userid=userid,
                           avatar=avatar, nickname=nickname,is_markdown=is_markdown)


# 按文章进行分类搜索的后台接口
@admin.route("/admin/type/<int:type>--<int:page>")
def admin_search_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    article = Article()
    result, total = article.find_by_type_except_drafted(start, pagesize, type)
    total = math.ceil(total / pagesize)
    return render_template('/xingyun-notebook/system-admin.html', page=page, result=result, total=total, userid=userid,
                           avatar=avatar, nickname=nickname,is_markdown=is_markdown)


# 按照文章标题进行模糊查询的后台接口
@admin.route("/admin/search/<keyword>")
def admin_search_headline(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Article().find_by_headline_except_drafted(keyword)

    return render_template('/xingyun-notebook/system-admin.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname,is_markdown=is_markdown)


# 按照作者昵称进行模糊查询的后台接口
@admin.route("/admin/search_mingzi/<keyword>")
def admin_search_mingzi(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Article().find_by_mingzi_except_drafted(keyword)
    return render_template('/xingyun-notebook/system-admin.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname,is_markdown=is_markdown)


# 文章的隐藏切换接口
@admin.route("/admin/article/hide/<int:articleid>")
def admin_article_hide(articleid):
    hide = Article().switch_hide(articleid)
    return str(hide)


# 文章的推荐切换接口
@admin.route("/admin/article/recommend/<int:articleid>")
def admin_article_recommend(articleid):
    recommended = Article().switch_recommended(articleid)
    return str(recommended)


# 文章的审核切换接口
@admin.route("/admin/article/check/<int:articleid>")
def admin_article_check(articleid):
    checked = Article().switch_checked(articleid)
    return str(checked)


# 为系统管理首页填充用户列表,并绘制分页栏
@admin.route("/admin-user")
def sys_admin_user():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    user = Users()
    result = user.find_all_users(0, pagesize)
    total = math.ceil(user.get_count_all_user() / pagesize)
    return render_template('/xingyun-notebook/system-admin-user.html', page=1, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname)


# 为系统管理首页的用户列表进行分页查询
@admin.route("/admin-user/<int:page>")
def admin_user(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    user = Users()
    result = user.find_all_users(start, pagesize)
    total = math.ceil(user.get_count_all_user() / pagesize)
    return render_template('/xingyun-notebook/system-admin-user.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname)


# 按照作者昵称进行模糊查询的后台接口
@admin.route("/admin-user/search_mingzi/<keyword>")
def admin_user_mingzi(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Users().find_by_mingzi(keyword)
    return render_template('/xingyun-notebook/system-admin-user.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname)


from common.utility import ming_tools_by_type


# 为系统管理首页填充工具列表,
@admin.route("/admin-tools")
def tools_admin():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 30
    tools = Tools()
    result = tools.find_all_tools(0, pagesize)
    total = math.ceil(tools.get_count_all_tools() / pagesize)
    return render_template('/xingyun-notebook/system-admin-tools.html', page=1, result=result, total=total,
                           ming_tools_by_type=ming_tools_by_type, userid=userid, avatar=avatar, nickname=nickname)


# 为系统管理首页的工具列表进行分页查询
@admin.route("/admin/tools/<int:page>")
def admin_tools_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 30
    start = (page - 1) * pagesize
    tools = Tools()
    result = tools.find_all_tools(start, pagesize)
    total = math.ceil(tools.get_count_all_tools() / pagesize)
    return render_template('/xingyun-notebook/system-admin-tools.html', page=page, result=result, total=total,
                           ming_tools_by_type=ming_tools_by_type,userid=userid,avatar=avatar, nickname=nickname)


# 按工具进行分类搜索的后台接口
@admin.route("/admin-tools/type/<int:type>--<int:page>")
def admin_search_tools_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    tools = Tools()
    result, total = tools.find_by_type_tools(start, pagesize, type)
    total = math.ceil(total / pagesize)
    return render_template('/xingyun-notebook/system-admin-tools.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname,ming_tools_by_type=ming_tools_by_type)






# 按工具名称进行模糊查询的后台接口
@admin.route("/admin-tools/search/<keyword>")
def admin_search_tools_name(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    tools = Tools()
    result = tools.find_by_tools_name(keyword)

    return render_template('/xingyun-notebook/system-admin-tools.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname,ming_tools_by_type=ming_tools_by_type)


# 按照作者昵称进行模糊查询的后台接口
@admin.route("/admin-tools/search_mingzi/<keyword>")
def admin_search_tools_user(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    tools = Tools()
    result = tools.find_by_mingzi_tools(keyword)
    return render_template('/xingyun-notebook/system-admin-tools.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname,ming_tools_by_type=ming_tools_by_type)
