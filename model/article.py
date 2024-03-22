import time
from flask import session
from sqlalchemy import Table, func, and_, extract

from common.database import db
from main import app
from model.users import Users

# 创建上下文
with ((app.app_context())):
    class Article(db.Model):
        __table__ = Table('article', db.metadata, autoload_with=db.engine)

        # 查询所有文章
        def find_all_articles(self):
            result = db.session.query(Article).all()
            return result

        # 根据id查询文章,数据格式：（Article,'nickname'）
        def find_by_id(self, article_id):
            # row = db.session.query(Article).filter_by(articleid=article_id).first()
            row = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.hide == 0, Article.drafted == 0, Article.checked == 1, Article.articleid == article_id
            ).first()
            return row

        # 根据id查询所有显示文章的is_markdown
        def find_is_markdown_by_id(self, article_id):
            is_markdown = db.session.query(Article.is_markdown).filter(Article.articleid == article_id,
                                                                       Article.hide == 0,
                                                                       Article.checked == 1).first()
            return is_markdown

        # 指定分页的limit和offset的参数值,同时与用户表做连接查询
        def find_limit_with_users(self, start, count):
            result = (db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid)
                      .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1)
                      .order_by(Article.articleid.desc()).limit(count).offset(start).all())
            return result

        # 统计一下当前文章的总数量
        def count_all_articles(self):
            count = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0,
                                                     Article.checked == 1).count()
            return count

        # 根据文章类型获取文章
        def find_by_type(self, type, start, count):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.hide == 0, Article.drafted == 0,
                Article.checked == 1, Article.category == type).order_by(
                Article.articleid.desc()).limit(count).offset(start).all()
            return result

        # 根据文章类型来获取总数量
        def count_by_type(self, type):
            count = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0,
                                                     Article.checked == 1, Article.category == type).count()
            return count

        # 根据用户的文章的类型来获取数量
        def count_by_type_user(self, type, userid):
            count = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0,
                                                     Article.checked == 1, Article.category == type,
                                                     Article.userid == userid).count()
            return count

        # 根据文章标题进行模糊搜索
        def find_by_title(self, headline, start, count):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.hide == 0, Article.drafted == 0,
                Article.checked == 1, Article.headline.like('%' + headline + '%')).order_by(
                Article.articleid.desc()).limit(count).offset(start).all()
            return result

        # 根据文章标题进行模糊搜索总数量
        def count_by_title(self, headline):
            count = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0,
                                                     Article.checked == 1,
                                                     Article.headline.like('%' + headline + '%')).count()
            return count

        # 最新文章
        def find_newest8_articles(self):
            result = db.session.query(Article.articleid, Article.headline, Article.is_markdown).filter(
                Article.hide == 0, Article.drafted == 0,
                Article.checked == 1).order_by(
                Article.articleid.desc()).limit(8).all()
            return result

        # 最多阅读
        def find_most9_read_articles(self):
            result = db.session.query(Article.articleid, Article.headline, Article.is_markdown).filter(
                Article.hide == 0, Article.drafted == 0,
                Article.checked == 1).order_by(
                Article.readcount.desc()).limit(8).all()
            return result

        # 特别推荐,如果超过8篇,可以考虑order by rand()的方式随机显示8篇
        def find_special_recommend8_articles(self):
            result = db.session.query(Article.articleid, Article.headline, Article.is_markdown).filter(
                Article.hide == 0, Article.drafted == 0,
                Article.checked == 1, Article.recommended == 1).order_by(
                func.rand()).limit(8).all()
            return result

        # 一次性返回三个推荐数据
        def find_three_recommend_articles(self):
            new = self.find_newest8_articles()
            most = self.find_most9_read_articles()
            recommend = self.find_special_recommend8_articles()
            return new, most, recommend

        # 每阅读一次文章,阅读次数+1
        def update_read_count(self, articleid):
            article = db.session.query(Article).filter_by(articleid=articleid).first()
            article.readcount += 1
            db.session.commit()

        # 根据文章编号查询文章标题
        def find_headline_by_articleid(self, articleid):
            row = db.session.query(Article.headline).filter_by(articleid=articleid).first()
            return row.headline

        # 获取当前文章的上一篇和下一篇
        def find_prev_next_by_articleid(self, articleid):
            dict = {}
            # 查询比当前编号小的当中最大的那一个(上一篇)
            row = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1,
                                                   Article.articleid < articleid
                                                   ).order_by(Article.articleid.desc()).limit(1).first()
            # 如果当前已经是第一篇,那么上一篇也是当前文章
            if row is None:
                prev_id = articleid
            else:
                prev_id = row.articleid

            dict['prev_id'] = prev_id
            dict['prev_headline'] = self.find_headline_by_articleid(prev_id)

            # 查询比当前编号大的当中最小的那一个(下一篇)
            row = db.session.query(Article).filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1,
                                                   Article.articleid > articleid
                                                   ).order_by(Article.articleid.asc()).limit(1).first()
            # 如果当前已经是最后一篇,那么下一篇也是当前文章
            if row is None:
                next_id = articleid
            else:
                next_id = row.articleid

            dict['next_id'] = next_id
            dict['next_headline'] = self.find_headline_by_articleid(next_id)

            return dict

        # 当发表或者回复评论后,为文章表字段replycount加1
        def update_replycount(self, articleid):
            row = db.session.query(Article).filter_by(articleid=articleid).first()
            row.replycount += 1
            db.session.commit()

        # 插入一篇新的文章,草稿或投稿通过参数进行区分
        def insert_article(self, category, headline, content, thumbnail, is_markdown, article_introduce, drafted=0,
                           checked=1):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            userid = session.get('userid')
            # 其他字段在数据库中均已设置好默认值,无须手工插入
            article = Article(category=category, headline=headline, content=content, thumbnail=thumbnail,
                              userid=userid, createtime=now, updatetime=now, drafted=drafted, checked=checked,
                              is_markdown=is_markdown, article_introduce=article_introduce)

            db.session.add(article)
            db.session.commit()
            return article.articleid  # 将新的文章编号返回,便于前端页面跳转

        # 根据文章编号更新文章的内容,可用于文章编辑和草稿修改,以及基于草稿的发布
        def update_article(self, articleid, category, headline, content, thumbnail, is_markdown, article_introduce,
                           drafted=0, checked=1):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            article = db.session.query(Article).filter_by(articleid=articleid).first()
            article.category = category
            article.headline = headline
            article.content = content
            article.thumbnail = thumbnail

            article.drafted = drafted
            article.is_markdown = is_markdown
            article.checked = checked
            article.article_introduce = article_introduce
            article.updatetime = now  # 修改文章的更新时间
            db.session.commit()
            return articleid  # 继续将文章ID返回调用处

        # =========================以下方法主要用于后台管理类操作=========================
        # 查询article表中除草稿外的所有数据并返回结果集
        def find_all_except_drafted(self, start, count):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.drafted == 0
            ).order_by(Article.articleid.desc()).limit(count).offset(
                start).all()
            return result

        # 查询除草稿外的所有文章的总数量
        def get_count_all_except_drafted(self):
            result = db.session.query(Article).filter(Article.drafted == 0
                                                      ).count()
            return result

        # 查询所有草稿的总数量
        def get_count_all_drafted(self):
            result = db.session.query(Article).filter(Article.drafted == 1
                                                      ).count()
            return result

        # 按照文章分类进行查询(不含草稿,该方法直接返回文章总数量用于分页)
        def find_by_type_except_drafted(self, start, count, category):
            if category == 0:
                result = self.find_all_except_drafted(start, count)
                total = self.get_count_all_except_drafted()
            else:
                result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                    Article.category == category, Article.drafted == 0).order_by(
                    Article.articleid.desc()).limit(count).offset(start).all()
                total = db.session.query(Article).filter(Article.category == category, Article.drafted == 0).count()
            return result, total  # 返回分页结果集和不分页的总数量

        # 个人文章中心按照文章分类进行查询(不含草稿,该方法直接返回文章总数量用于分页)
        def find_by_type_except_drafted_userid(self, start, count, category, userid):
            if category == 0:
                # result = self.find_all_except_drafted(start, count)
                result = self.user_query_article(start, count, userid)
                # total = self.get_count_all_except_drafted()
                total = self.get_count_user_except_drafted(userid)
            else:
                result = db.session.query(Article, Users.nickname).join(Users,
                                                                        Users.userid == Article.userid).filter(
                    Article.category == category, Article.drafted == 0, Article.userid == userid).order_by(
                    Article.articleid.desc()).limit(count).offset(start).all()
                total = db.session.query(Article).filter(Article.category == category, Article.drafted == 0,
                                                         Article.userid == userid).count()
            return result, total  # 返回分页结果集和不分页的总数量

        # 按照标题模糊查询(不含草稿,不分页)
        def find_by_headline_except_drafted(self, headline):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.headline.like('%' + headline + '%'), Article.drafted == 0
            ).order_by(Article.articleid.desc()).all()
            return result

        # 在个人草稿中心对于每个用户的文章按照标题模糊查询(不含草稿,不分页)
        def find_by_headline_drafted_userid(self, headline, userid):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.userid == userid,
                Article.headline.like('%' + headline + '%'), Article.drafted == 1
            ).order_by(Article.articleid.desc()).all()
            return result

        # 在个人文章中心对于每个用户的文章按照标题模糊查询(不含草稿,不分页)
        def find_by_headline_article_userid(self, headline, userid):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.userid == userid,
                Article.headline.like('%' + headline + '%'), Article.drafted == 0
            ).order_by(Article.articleid.desc()).all()
            return result

        # 按照作者昵称模糊查询(不含草稿, 不分页)
        def find_by_mingzi_except_drafted(self, nickname):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Users.nickname.like('%' + nickname + '%'), Article.drafted == 0
            ).order_by(Article.articleid.desc()).all()
            return result

        # 切换文章的隐藏状态：1表示隐藏,0表示显示
        def switch_hide(self, articleid):
            row = db.session.query(Article).filter_by(articleid=articleid).first()
            if row.hide == 1:
                row.hide = 0
            else:
                row.hide = 1
            db.session.commit()
            return row.hide  # 将当前最新状态返回给控制层

        # 切换文章的推荐状态：1表示推荐,0表示正常
        def switch_recommended(self, articleid):
            row = db.session.query(Article).filter_by(articleid=articleid).first()
            if row.recommended == 1:
                row.recommended = 0
            else:
                row.recommended = 1
            db.session.commit()
            return row.recommended  # 将当前最新状态返回给控制层

        # 切换文章的审核状态：1表示已审核,0表示待审
        def switch_checked(self, articleid):
            row = db.session.query(Article).filter_by(articleid=articleid).first()
            if row.checked == 1:
                row.checked = 0
            else:
                row.checked = 1
            db.session.commit()
            return row.checked  # 将当前最新状态返回给控制层

      

        # 根据某个指定用户查询其下所有文章
        def user_query_article(self, user_id, start, count):
            result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.drafted == 0,
                Users.userid == user_id  # 添加一个条件来指定要查询的用户ID
            ).order_by(Article.articleid.desc()).limit(count).offset(
                start).all()
            return result

        # 根据id查询文章,数据格式：（Article,'nickname'）
        def find_by_article_editor_id(self, article_id):
            row = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.hide == 0, Article.drafted == 0, Article.checked == 1, Article.articleid == article_id
            ).first()
            return row

        # 根据某个指定用户查询其下所有文章的数量
        def get_count_user_except_drafted(self, user_id):
            result = db.session.query(Article, Users).join(Users, Users.userid == Article.userid).filter(
                Article.drafted == 0,
                Users.userid == user_id  # 添加一个条件来指定要查询的用户ID
            ).count()
            return result

        # 根据某个指定用户查询其下所有草稿
        def user_query_drafted(self, user_id, start, count):
            result = db.session.query(Article, Users).join(Users, Users.userid == Article.userid).filter(
                Article.drafted == 1,
                Users.userid == user_id  # 添加一个条件来指定要查询的用户ID
            ).order_by(Article.articleid.desc()).limit(count).offset(
                start).all()
            return result

        # 根据某个指定用户查询其下所有草稿的数量
        def get_count_user_drafted(self, user_id):
            result = db.session.query(Article, Users).join(Users, Users.userid == Article.userid).filter(
                Article.drafted == 1,
                Users.userid == user_id  # 添加一个条件来指定要查询的用户ID
            ).count()
            return result

        # 根据id查询草稿,数据格式：（Article,'nickname'）
        def find_by_drafted_id(self, article_id):
            row = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
                Article.hide == 0, Article.drafted == 1, Article.checked == 1, Article.articleid == article_id
            ).first()
            return row

        # 根据文章id删除文章
        def delete_by_article_id(self, article_id):
            article = db.session.query(Article).filter(Article.articleid == article_id).first()
            if article:
                # 找到对应的文章
                db.session.delete(article)
                db.session.commit()
                return True
            else:
                # 未找到对应的文章
                return False

        # 查询某用户的所有文章的阅读量
        def get_readcount_by_user(self, userid):
            article_ids = db.session.query(Article.articleid).filter(Article.userid == userid).all()
            # 如果该用户没有文章，则直接返回0
            if not article_ids:
                return 0
                # 将查询结果转换为文章ID列表
            article_id_list = [article_id[0] for article_id in article_ids]  # 因为.all()返回的是元组列表
            # 第二步：基于这些文章ID统计总阅读数量
            total_readcount = db.session.query(func.sum(Article.readcount)).filter(
                Article.articleid.in_(article_id_list)
            ).scalar()  # scalar()用于获取单个值
            # 如果没有找到任何阅读量记录（可能是文章刚发表还没人阅读），则返回0
            if total_readcount is None:
                return 0
            return total_readcount

        # 查询所有文章的阅读量
        def get_readcount_by_all(self):
            article_ids = db.session.query(Article.articleid).all()
            # 如果没有文章，则直接返回0
            if not article_ids:
                return 0
                # 将查询结果转换为文章ID列表
            article_id_list = [article_id[0] for article_id in article_ids]  # 因为.all()返回的是元组列表
            # 第二步：基于这些文章ID统计总阅读数量
            total_readcount = db.session.query(func.sum(Article.readcount)).filter(
                Article.articleid.in_(article_id_list)
            ).scalar()  # scalar()用于获取单个值
            # 如果没有找到任何阅读量记录（可能是文章刚发表还没人阅读），则返回0
            if total_readcount is None:
                return 0
            return total_readcount

        # 查询某用户的所有被推荐的文章数量
        def query_recommend_count_by_user(self, userid):
            total = db.session.query(Article).filter(Article.userid == userid,
                                                     Article.recommended == 1).count()
            return total

        # 查询所有被推荐的文章数量
        def query_recommend_count_by_all(self):
            total = db.session.query(Article).filter(
                Article.recommended == 1).count()
            return total

        # 查询某用户的所有被隐藏的文章数量
        def query_hide_count_by_user(self, userid):
            total = db.session.query(Article).filter(Article.userid == userid,
                                                     Article.hide == 1).count()
            return total

        # 查询所有被隐藏的文章数量
        def query_hide_count_by_all(self):
            total = db.session.query(Article).filter(Article.hide == 1).count()
            return total

        # #根据文章最后的发布时间（年、月、日)获取文章信息(用户)
        def get_article_by_timetype_userid(self, timetype, userid):
            # 根据timetype执行相应的查询
            if timetype == 'daily':
                articles = db.session.query(func.date(Article.updatetime).label('date'),
                                            func.count(Article.articleid).label('count')).filter(
                    and_(Article.drafted == 0, Article.hide == 0, Article.userid == userid)).group_by(
                    func.date(Article.updatetime)).all()
                # print("每天的文章信息：")
                # for date, count in articles:
                #     print(f"{date} - {count}篇文章")
                return {'daily': articles}
            elif timetype == 'monthly':
                articles = db.session.query(
                    extract('year', Article.updatetime).label('year'),
                    extract('month', Article.updatetime).label('month'),
                    func.count(Article.articleid).label('count')
                ).filter(
                    and_(Article.drafted == 0, Article.hide == 0, Article.userid == userid)
                ).group_by(
                    extract('year', Article.updatetime),
                    extract('month', Article.updatetime)
                ).all()

                # print("每月的文章信息：")
                # for year, month, count in articles:
                #     print(f"{year}年{month}月 - {count}篇文章")
                return {'monthly': [(year, month, count) for year, month, count in articles]}
            elif timetype == 'yearly':
                articles = db.session.query(func.year(Article.updatetime).label('year'),
                                            func.count(Article.articleid).label('count')).filter(
                    and_(Article.drafted == 0, Article.hide == 0, Article.userid == userid)).group_by(
                    func.year(Article.updatetime)).all()
                # print("每年的文章信息：")
                # # 这里可以取消注释来打印每年的信息，或者根据需求决定是否打印
                # for year, count in articles:
                #     print(f"{year}年 - {count}篇文章")
                return {'yearly': articles}
            else:
                raise ValueError(f"Invalid time type: {timetype}. Valid options are 'daily', 'monthly', or 'yearly'.")

                # #根据文章最后的发布时间（年、月、日)获取文章信息

        def get_article_by_timetype(self, timetype):
            # 根据timetype执行相应的查询
            if timetype == 'daily':
                articles = db.session.query(func.date(Article.updatetime).label('date'),
                                            func.count(Article.articleid).label('count')).filter(
                    and_(Article.drafted == 0, Article.hide == 0)).group_by(
                    func.date(Article.updatetime)).all()
                # print("每天的文章信息：")
                # for date, count in articles:
                #     print(f"{date} - {count}篇文章")
                return {'daily': articles}
            elif timetype == 'monthly':
                articles = db.session.query(
                    extract('year', Article.updatetime).label('year'),
                    extract('month', Article.updatetime).label('month'),
                    func.count(Article.articleid).label('count')
                ).filter(
                    and_(Article.drafted == 0, Article.hide == 0)
                ).group_by(
                    extract('year', Article.updatetime),
                    extract('month', Article.updatetime)
                ).all()

                # print("每月的文章信息：")
                # for year, month, count in articles:
                #     # print(f"{year}年{month}月 - {count}篇文章")
                return {'monthly': [(year, month, count) for year, month, count in articles]}
            elif timetype == 'yearly':
                articles = db.session.query(func.year(Article.updatetime).label('year'),
                                            func.count(Article.articleid).label('count')).filter(
                    and_(Article.drafted == 0, Article.hide == 0)).group_by(
                    func.year(Article.updatetime)).all()
                # print("每年的文章信息：")
                # 这里可以取消注释来打印每年的信息，或者根据需求决定是否打印
                # for year, count in articles:
                #     # print(f"{year}年 - {count}篇文章")
                return {'yearly': articles}
            else:
                raise ValueError(
                    f"Invalid time type: {timetype}. Valid options are 'daily', 'monthly', or 'yearly'.")

        # 根据文章id查询用户的信息
        def query_user_by_articleid(self, articleid):
            result = db.session.query(Users).join(Article, Users.userid == Article.userid).filter(
                Article.articleid == articleid).first()
            return result
