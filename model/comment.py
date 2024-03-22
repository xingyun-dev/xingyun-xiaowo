import time

from flask import session
from sqlalchemy import Table, func
from common.utility import model_join_list
from common.database import db
from main import app
from model.article import Article
from model.users import Users

# 创建上下文
with (app.app_context()):
    class Comment(db.Model):
        __table__ = Table('comment', db.metadata, autoload_with=db.engine)

        # 新增一条评论
        def insert_comment(self, articleid, content, ipaddr):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            comment = Comment(userid=session.get('userid'), articleid=articleid, content=content,
                              ipaddr=ipaddr, createtime=now, updatetime=now)

            db.session.add(comment)
            db.session.commit()

        # 删除评论,用于隐藏
        def delete_comment(self, comment_id):
            comment = db.session.query(Comment).filter_by(commentid=comment_id).first()
            if comment:
                db.session.delete(comment)
                db.session.commit()

        # 根据文章编号查询所有原始评论
        def find_by_articleid(self, articleid):
            result = db.session.query(Comment).filter_by(articleid=articleid, hide=0, replyid=0).all()
            return result

        # 根据用户发布的文章查询其它用户的评论的数量
        def query_comments_count_by_articleid(self, userid):
            article_ids = db.session.query(Article.articleid).filter(Article.userid == userid).all()
            article_id_list = [article_id[0] for article_id in article_ids]  # 提取文章ID列表

            # 如果当前用户没有文章，直接返回0
            if not article_id_list:
                total = 0

            else:

                # 查询这些文章被收藏的总数
                total = db.session.query(func.count(Comment.commentid)).filter(
                    Comment.articleid.in_(article_id_list),
                ).scalar()

            return total

        # 根据用户查询其所有评论的数量
        def query_comments_count_by_userid(self, userid):
            result = db.session.query(Comment).filter(Comment.userid == userid).count()
            return result

        # 查询所有评论的数量
        def query_comments_count_by_all(self):
            result = db.session.query(Comment).count()
            return result

        # 查询评论与用户信息,注意评论也需要分页 [(comment,users),(comment,users)]
        def find_limit_with_user(self, articleid, start, count):
            result = db.session.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
                .filter(Comment.articleid == articleid, Comment.hide == 0) \
                .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
            return result

        # 新增一条回复,将原始评论的ID作为新评论的replyid字段来进行关联
        def insert_reply(self, articleid, content, commentid, ipaddr):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            reply = Comment(userid=session.get('userid'), articleid=articleid, content=content,
                            replyid=commentid, ipaddr=ipaddr, createtime=now, updatetime=now)
            db.session.add(reply)
            db.session.commit()

        # 查询原始评论与对应的用户信息,带分页参数
        def find_comment_with_user(self, articleid, start, count):
            result = db.session.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
                .filter(Comment.articleid == articleid, Comment.hide == 0, Comment.replyid == 0) \
                .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
            return result

        # 查询回复评论,回复评论不需要分页
        def find_reply_with_user(self, replyid):
            result = db.session.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
                .filter(Comment.replyid == replyid, Comment.hide == 0).all()
            return result

        # 根据原始评论和回复评论生成一个关联列表
        def get_comment_user_list(self, articleid, start, count):
            result = self.find_comment_with_user(articleid, start, count)
            comment_list = model_join_list(result)  # 原始评论的连接结果
            for comment in comment_list:
                # 查询原始评论对应的回复评论,并转换为列表保存到comment_list中
                result = self.find_reply_with_user(comment['commentid'])
                # 为comment_list列表中的原始评论字典对象添加一个新Key叫reply_list
                # 用于存储当前这条原始评论的所有回复评论,如果无回复评论则列表值为空
                comment['reply_list'] = model_join_list(result)
            return comment_list  # 将新的数据结构返回给控制器接口

        # 查询某篇文章的原始评论总数量,用于分页
        def get_count_by_article(self, articleid):
            count = db.session.query(Comment).filter_by(articleid=articleid, hide=0, replyid=0).count()
            return count
