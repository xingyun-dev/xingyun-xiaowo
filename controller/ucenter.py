import math
from flask import Blueprint, request, abort, render_template, session
from model.article import Article
from controller.index import is_markdown
from model.favorite import Favorite
from model.tools import Tools
from model.users import Users

ucenter = Blueprint('ucenter', __name__)


# 我收藏的文章

# 我收藏的文章
@ucenter.route('/ucenter')
def user_center():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    # article = Article()
    favorite = Favorite()
    result, total = favorite.find_my_favorite(0, pagesize)
    total = math.ceil(total / pagesize)
    # result = Favorite().find_my_favorite()
    return render_template('/xingyun-notebook/user-center.html', is_markdown=is_markdown, userid=userid,
                           avatar=avatar, nickname=nickname, result=result, total=total, page=1)


@ucenter.route('/ucenter/<int:page>')
def user_center_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    # article = Article()
    favorite = Favorite()
    result, total = favorite.find_my_favorite(start, pagesize)
    total = math.ceil(total / pagesize)
    # result = Favorite().find_my_favorite()
    return render_template('/xingyun-notebook/user-center.html', is_markdown=is_markdown, userid=userid,
                           avatar=avatar, nickname=nickname, page=page, result=result, total=total)


@ucenter.route('/user/favorite/<int:favoriteid>')
def user_favorite(favoriteid):
    canceled = Favorite().switch_favorite(favoriteid)
    return str(canceled)


@ucenter.route('/user/post')
def user_post():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    return render_template('/xingyun-notebook/user-post.html', userid=userid, avatar=avatar, nickname=nickname)


# 我的文章
@ucenter.route('/ucenter/article')
def ucenter_article():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    article = Article()
    user_id = session.get('userid')
    result = article.user_query_article(user_id, 0, pagesize)
    total = math.ceil(article.get_count_user_except_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-myarticle.html', page=1, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname)


# 为我的文章页面的文章列表进行分页查询
@ucenter.route("/ucenter/article/<int:page>")
def ucenter_article_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    user_id = session.get('userid')
    article = Article()
    result = article.user_query_article(user_id, start, pagesize)
    total = math.ceil(article.get_count_user_except_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-myarticle.html', page=page, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname)



# 文章展示
@ucenter.route('/ucenter/articleuser/<int:user_id>')
def ucenter_article_user(user_id):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 15
    article = Article()
    user_info = Users().find_by_userid(user_id)
    result = article.user_query_article(user_id, 0, pagesize)
    total = math.ceil(article.get_count_user_except_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-userarticle.html', page=1, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname,user_id=user_id,user_info=user_info)





# 为文章展示列表进行分页查询
@ucenter.route("/ucenter/articleuser/<int:user_id>--<int:page>")
def ucenter_userarticle_page(page,user_id):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 15
    start = (page - 1) * pagesize
    article = Article()
    user_info = Users().find_by_userid(user_id)

    result = article.user_query_article(user_id, start, pagesize)
    total = math.ceil(article.get_count_user_except_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-userarticle.html', page=page, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname,user_id=user_id,user_info=user_info)




@ucenter.route('/notebook/article_editor/<int:articleid>')
def editor_article(articleid):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_article_editor_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]

    return render_template("/xingyun-notebook/article-editor-user.html", article=dict, userid=userid, avatar=avatar,
                           nickname=nickname)


@ucenter.route('/notebook/md_article_editor/<int:articleid>')
def md_editor_article(articleid):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_article_editor_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]

    return render_template("/xingyun-notebook/markdown_editor-user.html", article=dict, userid=userid, avatar=avatar,
                           nickname=nickname)


# 我的草稿
@ucenter.route('/ucenter/drafted')
def ucenter_drafted():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    article = Article()
    user_id = session.get('userid')
    result = article.user_query_drafted(user_id, 0, pagesize)
    total = math.ceil(article.get_count_user_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-mydrafted.html', page=1, result=result, total=total
                           , is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname)


# 为我的草稿页面的文章列表进行分页查询
@ucenter.route("/ucenter/drafted/<int:page>")
def ucenter_drafted_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    user_id = session.get('userid')
    article = Article()
    result = article.user_query_drafted(user_id, start, pagesize)
    total = math.ceil(article.get_count_user_drafted(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-mydrafted.html', page=page, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname)


# 文章编辑页面
@ucenter.route('/notebook/article_drafted/<int:articleid>')
def read_drafted(articleid):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_drafted_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]

    return render_template("/xingyun-notebook/drafted-user.html", article=dict, userid=userid, avatar=avatar,
                           nickname=nickname)


@ucenter.route('/notebook/md_article_drafted/<int:articleid>')
def read_markdown_drafted(articleid):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_drafted_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]

    return render_template("/xingyun-notebook/markdown_drafted-user.html", article=dict, userid=userid, avatar=avatar,
                           nickname=nickname)


# 我的收藏中心按文章进行分类搜索的后台接口
@ucenter.route('/ucenter/type/<int:type>--<int:page>')
def ucenter_favorite_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    # article = Article()
    favorite = Favorite()
    result, total = favorite.find_by_type_favorite_userid(start, pagesize, type, session.get('userid'))
    total = math.ceil(total / pagesize)
    return render_template('/xingyun-notebook/user-center.html', page=page, result=result, total=total,
                           is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname)


# 我的收藏中心按照文章标题进行模糊查询的后台接口
@ucenter.route("/ucenter/search/<keyword>")
def ucenter_favorite_search_headline(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    favorite = Favorite()
    result = favorite.find_by_headline_favorite_userid(keyword, userid)
    return render_template('/xingyun-notebook/user-center.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname, is_markdown=is_markdown)


# 我的收藏中心按照作者昵称进行模糊查询的后台接口
@ucenter.route("/ucenter/search_mingzi/<keyword>")
def ucenter_search_mingzi(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    favorite = Favorite()
    result = favorite.find_by_mingzi_favorite(keyword, userid)
    return render_template('/xingyun-notebook/user-center.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname, is_markdown=is_markdown)


# 个人文章中心按文章进行分类搜索的后台接口
@ucenter.route("/ucenter/article/type/<int:type>--<int:page>")
def user_search_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    article = Article()
    result, total = article.find_by_type_except_drafted_userid(start, pagesize, type, userid)
    total = math.ceil(total / pagesize)
    return render_template('/xingyun-notebook/user-myarticle.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, is_markdown=is_markdown)


# 个人文章中心按照文章标题进行模糊查询的后台接口
@ucenter.route("/ucenter/article/search/<keyword>")
def user_search_headline(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Article().find_by_headline_article_userid(keyword, userid)

    return render_template('/xingyun-notebook/user-myarticle.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname, is_markdown=is_markdown)




# 文章展示中心按文章进行分类搜索的后台接口
@ucenter.route("/ucenter/articleuser/<int:user_id>/type/<int:type>--<int:page>")
def articleuser_search_type(type, page,user_id):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 15
    start = (page - 1) * pagesize
    article = Article()
    user_info = Users().find_by_userid(user_id)
    result, total = article.find_by_type_except_drafted_userid(start, pagesize, type, user_id)
    total = math.ceil(total / pagesize)
    return render_template('/xingyun-notebook/user-userarticle.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, is_markdown=is_markdown,user_id =user_id,user_info=user_info)


# 文章展示界面按照文章标题进行模糊查询的后台接口
@ucenter.route("/ucenter/articleuser/<int:user_id>/search/<keyword>")
def articleuser_search_headline(keyword,user_id):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    user_info = Users().find_by_userid(user_id)

    result = Article().find_by_headline_article_userid(keyword, user_id)

    return render_template('/xingyun-notebook/user-userarticle.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname, is_markdown=is_markdown,user_id=user_id,user_info=user_info)




# 个人草稿中心按照文章标题进行模糊查询的后台接口
@ucenter.route("/ucenter/drafted/search/<keyword>")
def user_drafted_search_headline(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Article().find_by_headline_drafted_userid(keyword, userid)

    return render_template('/xingyun-notebook/user-mydrafted.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname, is_markdown=is_markdown)


from common.utility import ming_tools_by_type


# 我的工具
@ucenter.route("/ucenter/tools")
def user_tools():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 20
    tools = Tools()
    user_id = session.get('userid')
    result = tools.user_query_tools(user_id, 0, pagesize)
    total = math.ceil(tools.get_count_user_tools(user_id) / pagesize)
    return render_template('/xingyun-notebook/user-mytools.html', page=1, result=result, total=total,
                           ming_tools_by_type=ming_tools_by_type,userid=userid, avatar=avatar, nickname=nickname)


# 我的工具分页
@ucenter.route("/ucenter/tools/<int:page>")
def ucenter_tools_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 20
    start = (page - 1) * pagesize
    tools = Tools()
    result = tools.user_query_tools(userid, start, pagesize)
    total = math.ceil(tools.get_count_user_tools(userid) / pagesize)
    return render_template('/xingyun-notebook/user-mytools.html', page=page, result=result, total=total,
                           ming_tools_by_type=ming_tools_by_type,userid=userid, avatar=avatar, nickname=nickname)


# 工具编辑页面
@ucenter.route('/tools/tools_editor/<int:tools_id>')
def tools_editor(tools_id):
    try:
        tools = Tools()
        result = tools.get_tools_message_by_id(tools_id)
        if result is None:
            abort(404)

    except:
        abort(500)
    return render_template("/xingyun-notebook/tools-editor.html", result=result,ming_tools_by_type=ming_tools_by_type)



# 个人工具中心按照工具名称进行模糊查询的后台接口
@ucenter.route("/ucenter/tools/search/<keyword>")
def user_tools_search_name(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    tools = Tools()
    result = tools.find_by_name_tools_userid(keyword, session.get('userid'))
    return render_template('/xingyun-notebook/user-mytools.html', page=1, result=result, total=1,
                           ming_tools_by_type=ming_tools_by_type,userid=userid, avatar=avatar, nickname=nickname
                           )

