from common.database import db
import time
import random
from sqlalchemy import Table, func
from main import app
from flask import session
from model.article import Article
from model.users import Users

# 创建上下文
with ((((app.app_context())))):
    class Favorite(db.Model):
        __table__ = Table('favorite', db.metadata, autoload_with=db.engine)

        # 插入文章收藏数据
        def insert_favorite(self, articleid):
            row = db.session.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
            if row is not None:
                row.canceled = 0

            else:
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                favorite = Favorite(articleid=articleid, userid=session.get('userid'), canceled=0, createtime=now,
                                    updatetime=now)
                db.session.add(favorite)
            db.session.commit()

        # 取消收藏
        def cancel_favorite(self, articleid):
            row = db.session.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
            row.canceled = 1
            db.session.commit()

        # 判断是否已经被收藏
        def check_favorite(self, articleid):
            row = db.session.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
            if row is None:
                return False
            elif row.canceled == 1:
                return False
            else:
                return True

        # 为用户中心查询我的收藏添加数据操作方法
        def find_my_favorite(self, start, count):
            rows = db.session.query(Favorite, Article, Users.nickname).join(
                Article, Favorite.articleid == Article.articleid).join(
                Users, Article.userid == Users.userid).filter(
                Favorite.canceled == 0, Favorite.userid ==
                session.get('userid')).order_by(Article.articleid.desc()).limit(count).offset(start).all()
            total = db.session.query(Favorite).join(
                Article, Favorite.articleid == Article.articleid).join(
                Users, Article.userid == Users.userid).filter(
                Favorite.canceled == 0, Favorite.userid ==
                session.get('userid')).count()

            return rows, total

        # 我的收藏的数量
        def query_my_favorite_count(self, userid):
            total = db.session.query(Favorite).join(
                Article, Favorite.articleid == Article.articleid).join(
                Users, Article.userid == Users.userid).filter(
                Favorite.canceled == 0, Favorite.userid ==
                userid).count()
            return total

        # 网站所有被收藏文章的数量
        def query_all_favorited_count(self):
            article_ids = db.session.query(Article.articleid).all()
            article_id_list = [article_id[0] for article_id in article_ids]  # 提取文章ID列表

            # 如果当前用户没有文章，直接返回0
            if not article_id_list:
                total = 0

            else:

                # 查询这些文章被收藏的总数
                total = db.session.query(func.count(Favorite.favoriteid)).filter(
                    Favorite.articleid.in_(article_id_list),
                    Favorite.canceled == 0  # canceled字段用来标记是否取消收藏，0表示未取消
                ).scalar()

            return total

        # 查询我的文章被收藏的总数量
        def query_my_article_favorited_count(self, userid):
            article_ids = db.session.query(Article.articleid).filter(Article.userid == userid).all()
            article_id_list = [article_id[0] for article_id in article_ids]  # 提取文章ID列表

            # 如果当前用户没有文章，直接返回0
            if not article_id_list:
                total = 0

            else:

                # 查询这些文章被收藏的总数
                total = db.session.query(func.count(Favorite.favoriteid)).filter(
                    Favorite.articleid.in_(article_id_list),
                    Favorite.canceled == 0  # 假设canceled字段用来标记是否取消收藏，0表示未取消
                ).scalar()

            return total

            # 切换收藏和取消收藏的状态

        def switch_favorite(self, favoriteid):
            row = db.session.query(Favorite).filter_by(favoriteid=favoriteid).first()
            if row.canceled == 1:
                row.canceled = 0
            else:
                row.canceled = 1
            db.session.commit()
            return row.canceled

      
        def find_by_headline_favorite_userid(self, headline, userid):
            result = db.session.query(Favorite, Article, Users.nickname).join(
                Article, Favorite.articleid == Article.articleid).join(
                Users, Article.userid == Users.userid).filter(
                Favorite.canceled == 0,
                Favorite.userid == userid,
                Article.headline.ilike('%' + headline + '%'),  # 使用 ilike 实现不区分大小写的模糊查询
                Article.drafted == 0
            ).order_by(Article.articleid.desc()).all()
            return result

        # 按照作者昵称模糊查询(不含草稿, 不分页)
        def find_by_mingzi_favorite(self, nickname, userid):
            result = db.session.query(Favorite, Article, Users.nickname).join(
                Article, Favorite.articleid == Article.articleid).join(
                Users, Article.userid == Users.userid).filter(
                Favorite.canceled == 0,
                Favorite.userid == userid,
                Users.nickname.ilike('%' + nickname + '%'),  # 使用 ilike 实现不区分大小写的模糊查询
                Article.drafted == 0
            ).order_by(Article.articleid.desc()).all()
            return result

        def find_by_type_favorite_userid(self, start, count, category, userid):
            if category == 0:
                result = db.session.query(Favorite, Article, Users.nickname).join(
                    Article, Favorite.articleid == Article.articleid).join(
                    Users, Article.userid == Users.userid).filter(
                    Favorite.canceled == 0,
                    Favorite.userid == userid,
                    Article.drafted == 0
                ).order_by(Article.articleid.desc()).limit(count).offset(start).all()
                total = db.session.query(Favorite).join(
                    Article, Favorite.articleid == Article.articleid).filter(
                    Favorite.canceled == 0,
                    Favorite.userid == userid,
                    Article.drafted == 0
                ).count()
            else:
                result = db.session.query(Favorite, Article, Users.nickname).join(
                    Article, Favorite.articleid == Article.articleid).join(
                    Users, Article.userid == Users.userid).filter(
                    Favorite.canceled == 0,
                    Favorite.userid == userid,
                    Article.category == category,
                    Article.drafted == 0
                ).order_by(Article.articleid.desc()).limit(count).offset(start).all()
                total = db.session.query(Favorite).join(
                    Article, Favorite.articleid == Article.articleid).filter(
                    Favorite.canceled == 0,
                    Favorite.userid == userid,
                    Article.category == category,
                    Article.drafted == 0
                ).count()
            return result, total  # 返回分页结果集和不分页的总数量
