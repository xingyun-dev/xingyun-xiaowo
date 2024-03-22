import time

from flask import session
from sqlalchemy import Table
from common.database import db
from main import app
from model.users import Users

with ((app.app_context())):
    class Shezhi(db.Model):
        __table__ = Table('user_shezhi', db.metadata, autoload_with=db.engine)

        # 根据用户id查询编辑设置的信息
        def get_message_from_editoruser(self,user_id):
            result = db.session.query(Shezhi.shezhi_id, Shezhi.userid, Shezhi.wang_img, Shezhi.wang_name,
                                      Shezhi.wang_user_name,
                                      Shezhi.wang_lian, Shezhi.wang_user_avatar).filter(
                Shezhi.userid == user_id).all()

            return result

        # 将编辑设置信息插入数据库中
        def insert_message_to_shezhi(self, wang_img, wang_name, wang_user_name, wang_lian, wang_user_avatar):
            user_shezhi = Shezhi(userid=session.get('userid'), wang_img=wang_img, wang_name=wang_name,
                                 wang_user_name=wang_user_name, wang_lian=wang_lian, wang_user_avatar=wang_user_avatar)

            db.session.add(user_shezhi)
            db.session.commit()

        # 删除编辑设置信息
        def delete_message_from_shezhi(self, shezhi_id):
            user_shezhi = db.session.query(Shezhi).filter(Shezhi.shezhi_id == shezhi_id).first()
            if user_shezhi:
                # 找到对应的编辑设置信息
                db.session.delete(user_shezhi)
                db.session.commit()
                return True
            else:
                # 未找到
                return False

         # 更新外链设置信息
        def update_message_from_shezhi(self, shezhi_id, wang_img, wang_name, wang_user_name, wang_lian,
                                       wang_user_avatar):
            user_shezhi = db.session.query(Shezhi).filter_by(shezhi_id=shezhi_id).first()
            if wang_img:
                user_shezhi.wang_img = wang_img
            if wang_name:
                user_shezhi.wang_name = wang_name
            if wang_user_name:
                user_shezhi.wang_user_name = wang_user_name
            if wang_lian:
                user_shezhi.wang_lian = wang_lian
            if wang_user_avatar:
                user_shezhi.wang_user_avatar = wang_user_avatar
            db.session.commit()



