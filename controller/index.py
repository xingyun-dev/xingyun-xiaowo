import math
import os
from flask import Blueprint, render_template, abort, jsonify, request, session

from model.article import Article
from model.users import Users

index = Blueprint('index', __name__)


def is_markdown(articleid):
    article = Article()
    result = article.find_is_markdown_by_id(articleid)
    if result and result.is_markdown == 1:
        return "md_article"
    else:
        return "article"


@index.route('/notebook')
def home():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    article = Article()
    result = article.find_limit_with_users(0, 10)
    total = math.ceil(article.count_all_articles() / 10)  # 总页数
 
    new, most, recommend = article.find_three_recommend_articles()
    return render_template('/xingyun-notebook/index.html', result=result, total=total, page=1,
                           new=new, most=most, recommend=recommend, is_markdown=is_markdown,userid=userid, avatar=avatar, nickname=nickname)



# 分页代码
@index.route('/notebook/page/<int:page>')
def paginate(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    start = (page - 1) * 10
    article = Article()
    result = article.find_limit_with_users(start, 10)
    total = math.ceil(article.count_all_articles() / 10)  # 总页数
    new, most, recommend = article.find_three_recommend_articles()
    return render_template('/xingyun-notebook/index.html', result=result, total=total, page=page, new=new, most=most,
                           recommend=recommend, is_markdown=is_markdown,userid=userid, avatar=avatar, nickname=nickname)


@index.route('/notebook/type/<int:type>--<int:page>')
def classify(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    article = Article()
    start = (page - 1) * 10
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.count_by_type(type) / 10)
    new, most, recommend = article.find_three_recommend_articles()
    return render_template('/xingyun-notebook/type.html', result=result, total=total, page=page, type=type, new=new,
                           most=most,
                           recommend=recommend, is_markdown=is_markdown,userid=userid, avatar=avatar, nickname=nickname)


@index.route('/notebook/search/<int:page>--<keyword>')
def search(page, keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    keyword = keyword.strip()
    if keyword is None or keyword == "" or "%" in keyword or len(keyword) > 10:
        abort(404)
    article = Article()
    start = (page - 1) * 10
    result = article.find_by_title(keyword, start, 10)
    total = math.ceil(article.count_by_title(keyword) / 10)
    new, most, recommend = article.find_three_recommend_articles()
    return render_template('/xingyun-notebook/search.html', result=result, total=total, page=page, keyword=keyword,
                           new=new, most=most,
                           recommend=recommend, is_markdown=is_markdown,userid=userid, avatar=avatar, nickname=nickname)


@index.route('/recommend')
def recommend():
    article = Article()
    new, most, recommend = article.find_three_recommend_articles()

    new = [(item[0], item[1], item[2]) for item in new]
    most = [(item[0], item[1], item[2]) for item in most]
    recommend = [(item[0], item[1], item[2]) for item in recommend]

    return jsonify(new, most, recommend)


















# ================================Redis=================================#
# 重构index控制器中的代码,新增以下两种方法
# from common.redisdb import redis_connect


# @index.route('/redis')
# def home_redis():
#     red = redis_connect()
#     # 获取有序集合article的总数量
#     count = red.zcard('article')
#     total = math.ceil(count / 10)
#     # 利用zrevrange 从有序集合中倒序取0-9共10条数据,即最新文章
#     result = red.zrevrange('article', 0, 9)
#     # 由于加载进来的每一条数据是一个字符串,需要使用eval函数将其转换为字典对象
#     article_list = []
#     for row in result:
#         article_list.append(eval(row))
#     return render_template('index_redis.html', article_list=article_list, total=total, page=1)


# #

# @index.route('/redis/page/<int:page>')
# def paginate_redis(page):
#     start = (page - 1) * 10  # 根据当前页码定义数据的起始位置
#     red = redis_connect()
#     count = red.zcard('article')
#     total = math.ceil(count / 10)
#     result = red.zrevrange('article', start, start + 10 - 1)
#     article_list = []
#     for row in result:
#         article_list.append(eval(row))
#     return render_template('index_redis.html', article_list=article_list, total=total, page=page)

# # ================================静态化处理===============================#
#
# @index.route('/static')
# def all_static():
#     pagesize = 10
#     article = Article()
#     total = math.ceil(article.count_all_articles() / pagesize)
#     # 遍历每一页的内容,从数据库中查询出来,渲染到对应页面中
#     for page in range(1, total + 1):
#         start = (page - 1) * pagesize
#         result = article.find_limit_with_users(start, pagesize)
#         # 将当前页面正常渲染,但不响应给前端,而是将渲染后的内容写入静态文件
#         content = render_template('index-static.html', result=result, total=total, page=page)
#         #将渲染后的内容写入写入静态文件,其实content本身就是标准的HTML页面
#         with open(f'./template/index-static/index-{page}.html', 'w', encoding='utf-8') as f:
#             f.write(content)
#
#     return '文章列表页面分页静态化处理完成'
#
#
#
# @index.route('/')
# def home():
#     #判断是否存在该页面,如果存在则直接响应,否则正常查询数据库
#     if os.path.exists('./template/index-static/index-1.html'):
#         return render_template('index-static/index-1.html')
#     #如果不存在,则进行静态化处理
#     article = Article()
#     result = article.find_limit_with_users(0, 10)
#     total = math.ceil(article.count_all_articles() / 10)  # 总页数
#     content = render_template('index.html', result=result, total=total, page=1)
#     #如果是第一个用户访问,而静态文件不存在,则生成一个
#     with open('./template/index-static/index-1.html','w',encoding='utf-8') as f:
#         f.write(content)
#
#     return content
#
#
# @index.route('/page/<int:page>')
# def paginate(page):
#     # 判断是否存在该页面,如果存在则直接响应,否则正常查询数据库
#     if os.path.exists(f'./template/index-static/index-{page}.html'):
#         return render_template(f'index-static/index-{page}.html')
#     # 如果不存在,则进行静态化处理
#     article = Article()
#     result = article.find_limit_with_users(0, 10)
#     total = math.ceil(article.count_all_articles() / 10)  # 总页数
#     content = render_template('index.html', result=result, total=total, page=1)
#     # 如果是第一个用户访问,而静态文件不存在,则生成一个
#     with open(f'./template/index-static/index-{page}.html', 'w', encoding='utf-8') as f:
#         f.write(content)
#
#     return content
