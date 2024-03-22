import random
import time

from flask import session
from sqlalchemy import Table, func

from common.database import db
from main import app
from model.users import Users

# 创建上下文
with app.app_context():
    class Follow(db.Model):
        __table__ = Table('tb_vip_follow', db.metadata, autoload_with=db.engine)

        # 随机查询用户
        def find_random_users(self, num):
            # 随机查询用户
            random_users = db.session.query(Users).order_by(func.random()).limit(num).all()
            return random_users

        def find_by_mingzi(self, nickname):
            result = db.session.query(Users.nickname).filter(
                Users.nickname.like('%' + nickname + '%'),
            ).all()
            return result

        # 插入关注信息
        def insert_follow(self, vip_id, followed_vip_id):
            new_follow = Follow(vip_id=vip_id, followed_vip_id=followed_vip_id, status=1)
            db.session.add(new_follow)
            db.session.commit()
            return new_follow.vip_id, new_follow.followed_vip_id

        def query_follow(self, vip_id, followed_vip_id):
            follow = db.session.query(Follow).filter_by(vip_id=vip_id, followed_vip_id=followed_vip_id).first()
            # 如果已存在相同的关注信息，则返回True，否则返回False
            return follow is not None

        # 获取关注的状态
        def get_follow_status(self, vip_id, followed_vip_id):
            # 在这里查询数据库获取关注状态，假设使用ORM框架，并且关注状态存储在status字段中
            row = db.session.query(Follow).filter_by(vip_id=vip_id, followed_vip_id=followed_vip_id).first()

            if row is not None:
                return row.status
            else:
                return 0

        # 切换用户的关注状态：1表示已关注,0表示未关注
        def switch_status(self, vip_id, followed_vip_id):
            row = db.session.query(Follow).filter_by(vip_id=vip_id, followed_vip_id=followed_vip_id).first()
            if row is None:
                Follow().insert_follow(vip_id, followed_vip_id)
                # row.status = 1

            else:
                if row.status == 1:
                    row.status = 0
                else:
                    row.status = 1
                db.session.commit()
            return row.status  # 将当前最新状态返回给控制层

        # 根据用户ID查询关注了哪些用户
        def get_follow_user(self):
            result = db.session.query(Follow.followed_vip_id, Users).join(Users,
                                                                          Users.userid == Follow.vip_id).filter(
                Follow.status == 1).all()
            return result

        # 根据用户ID查询某个用户关注了哪些用户
        def get_follow_by_userid(self, userid):
            result = db.session.query(Follow.followed_vip_id, Users).join(Users,
                                                                          Users.userid == Follow.vip_id).filter(
                Follow.status == 1, Follow.vip_id == userid).all()
            return result

        #     # 根据用户ID查询某个用户关注了哪些用户的数量
        def get_follow_by_userid_count(self, userid):
            result = db.session.query(Follow.followed_vip_id, Users).join(Users,
                                                                          Users.userid == Follow.vip_id).filter(
                Follow.status == 1, Follow.vip_id == userid).count()
            return result

        # 获取关注用户的详细信息
        def get_follow_users_with_details(self, userid):
            # 首先，从Follow表中获取关注的用户ID
            followed_user_ids = db.session.query(Follow.followed_vip_id).filter(
                Follow.vip_id == userid, Follow.status == 1
            ).distinct().all()  # 使用distinct()确保没有重复的ID

            # 提取关注的用户ID列表
            followed_user_id_list = [item[0] for item in followed_user_ids]

            # 然后，使用这些ID从Users表中获取用户的详细信息
            followed_users_details = db.session.query(Users).filter(
                Users.userid.in_(followed_user_id_list)
            ).all()

            return followed_users_details

        # 查询被哪些用户关注了
        def get_followed_user(self, userid):
            result = db.session.query(Follow.vip_id).filter(Follow.followed_vip_id == userid,
                                                            Follow.status == 1).all()
            return result

        # 查询被哪些用户关注的数量
        def get_followed_user_count(self, userid):
            result = db.session.query(Follow.vip_id).filter(Follow.followed_vip_id == userid,
                                                                Follow.status == 1).count()
            return result

        # 查询和某个用户共同的关注列表
        def get_together_followed_by(self, userid):
            # 查询用户关注的所有用户
            user_following = db.session.query(Follow.followed_vip_id).filter(Follow.vip_id == userid,
                                                                             Follow.status == 1).all()
            # 查询共同关注的用户
            result = db.session.query(Follow.vip_id).filter(Follow.followed_vip_id.in_(user_following),
                                                            Follow.status == 1).distinct().all()
            return result

        # 查询是否互相关注
        def check_mutual_follow(self, user1_id, user2_id):
            subquery = db.session.query(Follow.followed_vip_id).filter_by(vip_id=user2_id).subquery()

            # 查询用户1关注用户2的有效记录
            user1_follow_user2 = db.session.query(Follow).filter_by(vip_id=user1_id, followed_vip_id=user2_id,
                                                                    status=1).first()

            # 查询用户2关注用户1的有效记录
            user2_follow_user1 = db.session.query(Follow).filter_by(vip_id=user2_id, followed_vip_id=user1_id,
                                                                    status=1).first()

            if user1_follow_user2 and user2_follow_user1:
                return True  # 互相关注
            else:
                return False  # 不是互相关注


        #查询用户的互相关注的数量

        def get_mutal_follow_count(self, userid):
            # 查询该用户关注的所有用户ID
            following_ids = db.session.query(Follow.followed_vip_id
                                             ).filter(Follow.vip_id == userid,Follow.status==1).all()
            following_ids = [id_[0] for id_ in following_ids]  # 提取ID列表

            # 查询关注该用户的所有用户ID
            followers_ids = db.session.query(Follow.vip_id).filter(Follow.followed_vip_id == userid,Follow.status==1).all()
            followers_ids = [id_[0] for id_ in followers_ids]  # 提取ID列表

            # 计算互相关注的用户数量
            # 使用set交集来找出两个列表中共有的ID，然后计算长度
            mutual_follow_count = len(set(following_ids) & set(followers_ids))

            return mutual_follow_count
