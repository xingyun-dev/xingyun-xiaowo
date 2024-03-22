from flask import session
from sqlalchemy import Table, func, and_, or_
import time

from sqlalchemy.orm import aliased

from common.database import db
from main import app
from model.tb_follow import Follow
from model.users import Users

with ((app.app_context())):
    class Message(db.Model):
        __table__ = Table('message', db.metadata, autoload_with=db.engine)

        # 获取消息内容、创建时间、用户名称、用户头像路径和用户ID(多人聊天室)
        def get_messages(self):
            result = db.session.query(Message.message_id, Message.content, Message.create_time, Users.nickname,
                                      Users.avatar,
                                      Message.user_id).filter(Message.user_id == Users.userid,
                                                              Message.communicate_user == None
                                                              ).all()
            return result

        # 获取用户的总的发送信息数量
        def get_messages_user_count(self, userid):
            result = db.session.query(Message).filter(Message.user_id == Users.userid,
                                                      Message.user_id == userid).count()
            return result

        # 获取聊天室的总的发送信息数量
        def get_messages_all_count(self):
            result = db.session.query(Message).filter(Message.user_id == Users.userid,
                                                      ).count()
            return result

        # 获取用户的多人聊天室发送信息数量
        def get_messagesduo_user_count(self, userid):
            result = db.session.query(Message).filter(Message.user_id == Users.userid, Message.user_id == userid,
                                                      Message.communicate_user==None).count()
            return result

        # 获取多人聊天室的信息总量
        def get_messagesduo_all_count(self):
            result = db.session.query(Message).filter(Message.user_id == Users.userid,
                                                      Message.communicate_user ==None).count()
            return result

        # 获取用户的一对一聊天室发送信息数量
        def get_messagesone_user_count(self, userid):
            result = db.session.query(Message).filter(Message.user_id == Users.userid, Message.user_id == userid,
                                                      Message.communicate_user != None).count()
            return result

        # 获取总的一对一聊天室发送信息数量
        def get_messagesone_all_count(self):
            result = db.session.query(Message).filter(Message.user_id == Users.userid,
                                                      Message.communicate_user !=None).count()
            return result

        # 获取用户的私信数量
        def get_sixin_user_count(self, userid):
            result = db.session.query(Message).filter(Message.user_id == Users.userid,
                                                      Message.communicate_user == userid,
                                                      ).count()
            return result

        # 获得一对一的聊天信息
        def get_messages_onebyone(self, communicate_userid):
            # 使用and_来组合多个条件，并使用join来连接Message和Users表
            result = db.session.query(Message.message_id, Message.content, Message.create_time, Users.nickname,
                                      Users.avatar, Message.user_id, Message.communicate_user).join(Users,
                                                                                                    Message.user_id == Users.userid).filter(
                and_(Message.user_id == session.get('userid'), Message.communicate_user == communicate_userid)
            ).order_by(Message.create_time.asc()).all()
            result += db.session.query(Message.message_id, Message.content, Message.create_time, Users.nickname,
                                       Users.avatar, Message.user_id, Message.communicate_user).join(Users,
                                                                                                     Message.communicate_user == Users.userid).filter(
                and_(Message.communicate_user == session.get('userid'), Message.user_id == communicate_userid)
            ).order_by(Message.create_time.asc()).all()
            result = sorted(result, key=lambda x: x.create_time, reverse=False)

            return result

        #
        # 获得当前登录用户的所有关注者给发的所有私信：
        def get_message_all_follow_user(self):
            # 获取当前登录用户的ID
            current_userid = session.get('userid')

            # 查找当前用户关注的所有用户的ID
            followed_user_ids = db.session.query(Follow.followed_vip_id).filter(
                Follow.vip_id == current_userid).subquery()

            # 构建查询以获取这些关注者发送给当前用户的所有私信
            result = db.session.query(Message.message_id, Message.content, Message.create_time, Users.nickname,
                                      Users.avatar, Message.user_id, Message.communicate_user).join(
                Users,
                Message.user_id == Users.userid
            ).filter(
                Message.communicate_user == current_userid,  # 确保私信是发送给当前用户的
                Message.user_id.in_(followed_user_ids)  # 确保私信是由当前用户的关注者发送的
            ).order_by(Message.create_time.asc())  # 按创建时间降序排序

            return result.all()

        # 将用户的聊天信息插入数据库
        def insert_message(self, content, communicate_userid):
            if communicate_userid:
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                message = Message(user_id=session.get('userid'), create_time=now, content=content,
                                  communicate_user=communicate_userid)
                db.session.add(message)
                db.session.commit()
            # return message.user_id, message.create_time, message.content
            else:
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                message = Message(user_id=session.get('userid'), create_time=now, content=content, communicate_user=None
                                  )
                db.session.add(message)
                db.session.commit()
            return message.user_id, message.create_time, message.content

        # 获取当前用户的头像
        def get_at_avatar(self, user_id):
            user = db.session.query(Users).filter(Users.userid == user_id).first()  # 根据用户 ID 查询用户对象
            if user is not None:
                return user.avatar  # 返回用户的头像 URL
            else:
                return None  # 如果找不到对应的用户，则返回 None

        # 更新用户头像
        def update_avatar(self, user_id, new_avatar):
            user = db.session.query(Users).filter_by(id=user_id).first()
            if user is not None:
                user.avatar = new_avatar  # 更新用户的头像 URL
                db.session.commit()  # 提交事务，将更新写入数据库
                return "Changed successfully"

            else:
                return "Failed"

        # 根据message_id删除发送的信息
        def delete_user_message(self, message_id):
            message = db.session.query(Message).filter(Message.message_id == message_id).first()
            if message:
                db.session.delete(message)
                db.session.commit()
                return True
            else:
                return False
