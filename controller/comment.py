from flask import Blueprint, request, session, jsonify

from model.article import Article
from model.comment import Comment

from model.users import Users

comment = Blueprint("comment", __name__)


# 蓝图拦截器
@comment.before_request
def before_comment():
    if session.get("islogin") is None or session.get("islogin") != 'true':
        return "not-login"


@comment.route("/comment", methods=["POST"])
def add_comment():
    articleid = request.form.get("articleid")
    content = request.form.get("content").strip()
    ipaddr = request.remote_addr  # 直接获取ip地址

    # 对文章的评论内容进行简单校验
    if len(content) > 1000:
        return 'content-invalid'
    comment = Comment()
    try:
        comment.insert_comment(articleid, content, ipaddr)
        return 'add-pass'
    except:
        return 'add-fail'



@comment.route("/reply", methods=["POST"])
def reply():
    articleid = request.form.get("articleid")
    commentid = request.form.get("commentid")
    content = request.form.get("content").strip()
    ipaddr = request.remote_addr

    # 如果评论的字数多于1000个,则视为不合法
    if len(content) > 1000:
        return 'content-invalid'

    comment = Comment()
    # 没有超出限制才能发表评论

    try:
        comment.insert_reply(articleid, content, commentid, ipaddr)
        return 'reply-pass'
    except:
        return 'reply-fail'

@comment.route("/delete", methods=["POST"])
def delete():
    commentid = request.form.get("commentid")
    # ipaddr = request.remote_addr
    comment = Comment()
    try:
        comment.delete_comment(commentid)
        return 'delete-pass'
    except:
        return 'delete-fail'




# 为了使用Ajax分页,特创建此接口用于演示
# 由于分页栏已经完成渲染,此接口仅根据前端的页码请求后台对应的数据
@comment.route('/comment/<int:articleid>-<int:page>')
def comment_page(articleid, page):
    start = (page - 1) * 10
    comment = Comment()
    list = comment.get_comment_user_list(articleid, start, 10)
    return jsonify(list)
