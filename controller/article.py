import math
from flask import Blueprint, request, abort, render_template, session, Flask
from common.utility import *
from model.article import Article
from model.comment import Comment
from controller.index import is_markdown

from model.favorite import Favorite
from model.users import Users


article = Blueprint('article', __name__)


@article.route('/notebook/article/<int:articleid>')
def read(articleid):
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]
    Article().update_read_count(articleid)  # 阅读次数+1
    is_favorited = Favorite().check_favorite(articleid)

    # 获取当前文章的上一篇和下一篇
    prev_next = Article().find_prev_next_by_articleid(articleid)

    # 显示当前文章对应的评论
    # comment_user = Comment().find_limit_with_user(articleid,0,50)
    comment_list = Comment().get_comment_user_list(articleid, 0, 10)

    # 评论总页数
    count = Comment().get_count_by_article(articleid)
    total = math.ceil(count / 10)

    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')

    #获取文章对应的用户信息
    user_info = Article().query_user_by_articleid(articleid)

    return render_template("/xingyun-notebook/article-user.html", article=dict,
                           is_favorited=is_favorited, prev_next=prev_next, comment_list=comment_list,
                           total=total, is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname,user_info=user_info)


@article.route('/notebook/md_article/<int:articleid>')
def read_md(articleid):
    try:
        # 数据格式：（Article,'nickname'）
        result = Article().find_by_id(articleid)
        if result is None:
            abort(404)

    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result[1]
    Article().update_read_count(articleid)  # 阅读次数+1
    is_favorited = Favorite().check_favorite(articleid)

    # 获取当前文章的上一篇和下一篇
    prev_next = Article().find_prev_next_by_articleid(articleid)

    # 显示当前文章对应的评论
    # comment_user = Comment().find_limit_with_user(articleid,0,50)
    comment_list = Comment().get_comment_user_list(articleid, 0, 10)

    # 评论总页数
    count = Comment().get_count_by_article(articleid)
    total = math.ceil(count / 10)

    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')

    #获取文章对应的用户信息
    user_info = Article().query_user_by_articleid(articleid)


    return render_template("/xingyun-notebook/md_article-user.html", article=dict,
                           is_favorited=is_favorited, prev_next=prev_next, comment_list=comment_list,
                           total=total, is_markdown=is_markdown, userid=userid, avatar=avatar, nickname=nickname,user_info=user_info)


@article.route('/prepost')
def pre_post():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    return render_template("/xingyun-notebook/post-user.html", userid=userid, avatar=avatar, nickname=nickname)


@article.route('/mdpost')
def md_post():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    return render_template("/xingyun-notebook/post-article-md.html", userid=userid, avatar=avatar, nickname=nickname)


# 新增文章
@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    category = request.form.get('type')
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    is_markdown = int(request.form.get('is_markdown'))
    articleid = int(request.form.get('articleid'))
    article_introduce = request.form.get('article_introduce')
    thumb = request.form.get('thumbnail')
    # new_article = request.form.get('new_article')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            # 权限合格,可以执行发布文章的代码
            if len(thumb) > 10:
                thumbname = handle_upload(thumb)
            else:
                # 首先为文章生成缩略图,优先从内容中找,找不到则随机生成一张
                url_list = parse_image_url(content)
                if len(url_list) > 0:  # 表示文章中存在图片
                    thumbname = generate_thumb(url_list)
                else:
                    # 如果文章中没有图片,则根据文章类别指定一张缩略图片
                    thumbname = '%d.png' % int(category)

            article = Article()
            # 再判断articleid是否为0,如果为0则表示是新数据
            if articleid == 0:
                try:
                    id = article.insert_article(category=category, headline=headline,
                                                content=content, thumbnail=thumbname,
                                                drafted=drafted, checked=checked, is_markdown=is_markdown,
                                                article_introduce=article_introduce)

                    return str(id)
                except Exception as e:
                    return 'post-fail'
            else:
                # 如果是已经添加过的文章,则做修改操作
                try:
                    id = article.update_article(articleid=articleid, category=category, headline=headline,
                                                content=content, thumbnail=thumbname,
                                                drafted=drafted, checked=checked, is_markdown=is_markdown)
                    return str(id)
                except Exception as e:
                    return 'post-fail'

        # 如果角色不是作者,则只能投稿,不能正式发布
        elif checked == 1:
            return 'perm-denied'
        else:
            return 'perm-denied'


# 编辑文章
@article.route('/editor_article', methods=['POST'])
def editor_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    category = request.form.get('type')
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    is_markdown = int(request.form.get('is_markdown'))
    articleid = int(request.form.get('articleid'))
    article_introduce = request.form.get('article_introduce')
    thumb = request.form.get('thumbnail')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            # 权限合格,可以执行发布文章的代码
            if len(thumb) > 10:
                thumbname = handle_upload(thumb)
            else:
                # 首先为文章生成缩略图,优先从内容中找,找不到则随机生成一张
                url_list = parse_image_url(content)
                if len(url_list) > 0:  # 表示文章中存在图片
                    thumbname = generate_thumb(url_list)
                else:
                    # 如果文章中没有图片,则根据文章类别指定一张缩略图片
                    thumbname = '%d.png' % int(category)

            article = Article()
            try:
                id = article.update_article(articleid=articleid, category=category, headline=headline,
                                            content=content, thumbnail=thumbname,
                                            drafted=drafted, checked=checked, is_markdown=is_markdown,article_introduce=article_introduce)
                return str(id)
            except Exception as e:
                return 'post-fail'

        # 如果角色不是作者,则只能投稿,不能正式发布
        elif checked == 1:
            return 'perm-denied'
        else:
            return 'perm-denied'


# 删除文章
@article.route('/article/delete', methods=['POST'])
def delete_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            article_id = int(request.form.get('articleid'))
            article = Article()
            success = article.delete_by_article_id(article_id)
            if success:
                # 删除成功
                return 'delete-success'
            else:
                # 删除失败
                return 'delete-fail'
        else:
            return 'perm-denied'


# 隐藏文章
@article.route('/article/hidden', methods=['POST'])
def hidden_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            article_id = int(request.form.get('articleid'))
            article = Article()
            success = article.switch_hide(article_id)
            if success == 1:
                # 隐藏成功
                return 'hidden-success'
            elif success == 0:
                # 取消隐藏
                return 'hidden-cancel'
        else:
            return 'perm-denied'


# 推荐文章
@article.route('/article/recommend', methods=['POST'])
def recommend_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            article_id = int(request.form.get('articleid'))
            article = Article()
            success = article.switch_recommended(article_id)
            if success == 1:
                # 隐藏成功
                return 'recommend-success'
            elif success == 0:
                # 取消隐藏
                return 'recommend-cancel'
        else:
            return 'perm-denied'


# 审核文章
@article.route('/article/checked', methods=['POST'])
def checked_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            article_id = int(request.form.get('articleid'))
            article = Article()
            success = article.switch_checked(article_id)
            if success == 1:
                # 已经审核
                return 'checked-success'
            elif success == 0:
                # 还未审核
                return 'checked-cancel'
        else:
            return 'perm-denied'

