import redis
from common.database import db
from common.utility import model_list
from model.users import Users
from main import app
import re
from model.article import Article
from datetime import datetime

def redis_connect():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379,decode_responses=True, db=0)
    red = redis.Redis(connection_pool=pool)
    return red

# def redis_mysql_string():
#     red = redis_connect()
#     with (app.app_context()):
#         #查询users表的所有数据,将其从sqlalchemy的模型对象转换成JSON字符串
#         result = db.session.query(Users).all()
#     json = model_list(result)
#     red.set('users', str(json))  #将整张表的数据保存成JSON字符串


# def redis_mysql_string():
#     red = redis_connect()
#     with (app.app_context()):
#         #查询users表的所有数据,将其从sqlalchemy的模型对象转换成JSON字符串
#         result = db.session.query(Users).all()
#     user_list = model_list(result)
#     for user in user_list:
#         red.set(user['username'], user['password'])
#



def redis_mysql_hash():
    red = redis_connect()
    with (app.app_context()):
        #查询users表的所有数据,将其从sqlalchemy的模型对象转换成JSON字符串
        result = db.session.query(Users).all()
    user_list = model_list(result)
    for user in user_list:
        red.hset('users_hash',user['username'],user['password'])


def redis_article_zsort():
    with (app.app_context()):
        result = db.session.query(Article,Users.nickname).join(Users,Users.userid==Article.userid).all()
    list = []
    for article,nickname in result:
        dict = {}
        for k,v in article.__dict__.items():
            if not k.startswith('_sa_instance_state'):   #跳过内置字段
                if isinstance(v,datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                #将文章内容的HTML和不可见字符删除,再截取前面80个字符
                elif k=='content':
                    pattern = re.compile(r'<[^>]+>')
                    temp = pattern.sub('', v)
                    temp = temp.replace('&nbsp;', '')
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\n', '')
                    temp = temp.replace('\t', '')
                    v = temp.strip()[:80]
                dict[k] = v
        dict['nickname'] = nickname
        list.append(dict)   #最终构建一个标准的列表+字典的数据结构

    #将数据缓存到有序集合中
    red = redis_connect()
    for row in list:
        #zadd的命令参数为： (键名,{值:排序依据})
        #此处将文章表中的每一行数据作为值,文章编号作为排序依据
        red.zadd('article',{str(row):row['articleid']})














if __name__ == '__main__':
    # redis_mysql_string()
    # redis_mysql_hash()
    redis_article_zsort()


