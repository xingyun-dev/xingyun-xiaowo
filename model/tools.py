import random
import time

from flask import session
from sqlalchemy import Table, func

from common.database import db
from main import app
from model.users import Users

# 创建上下文
with app.app_context():
    class Tools(db.Model):
        __table__ = Table('tools', db.metadata, autoload_with=db.engine)

        # 1代表AI工具、11代表AI工具下的”常用"、12代表AI工具下的”AI图像工具"、13代表AI工具下的”AI聊天工具"、14代表AI工具下的”AI 视频工具"
        # 2代表生信软件，21、22、23、24
        # 3代表生信网站，31、32、33、34
        # 4代表消息获取
        # 5代表设计美化
        # 6代表学习网站
        # 7代表其它

        # 根据tools_type查询tools表中信息
        def get_tools_message_by_type(self, tools_type):
            result = db.session.query(Tools).filter(Tools.tools_type == tools_type, Tools.tools_check == 1).all()
            return result

        # 查询某一大类下的所有工具，使用startswith和%通配符
        def get_tools_message_by_major_category(self, major_category):
            result = db.session.query(Tools).filter(Tools.tools_type.startswith(major_category),Tools.tools_check == 1).all()
            return result

        # 查询所有工具
        def get_tools_message(self):
            result = db.session.query(Tools).filter(Tools.tools_check == 1).all()
            return result

        # 根据tools_id查询工具的信息
        def get_tools_message_by_id(self, tools_id):
            result = db.session.query(Tools).filter(Tools.tools_id == tools_id,Tools.tools_check == 1).first()
            return result

        # 根据工具的分类随机查询6条工具信息（充当相关导航）
        def get_tools_random_6_by_type(self, tools_type):
            # 首先根据工具类型筛选工具
            filtered_tools = self.get_tools_message_by_type(tools_type)
            # 如果没有找到该类型的工具，返回空列表
            if not filtered_tools:
                return []
                # 从筛选后的工具中随机选择6条
            random_tools = random.sample(filtered_tools, min(6, len(filtered_tools)))

            return random_tools

        # 插入工具信息
        def insert_tools_message(self, tools_avatar, tools_name, tools_introduce, tools_link, tools_type,
                                 tools_jianjie, tools_userid, tools_user_nickname):
            role = db.session.query(Users.role).filter(Users.userid == tools_userid).first()
            if role == "admin":
                tools_check = 1
            else:
                tools_check = 0

            tools = Tools(tools_avatar=tools_avatar, tools_name=tools_name, tools_introduce=tools_introduce, tools_link=
            tools_link, tools_type=tools_type, tools_jianjie=tools_jianjie, tools_check=tools_check,
                          tools_userid=tools_userid, tools_user_nickname=tools_user_nickname)
            db.session.add(tools)
            db.session.commit()

        # 更新/编辑工具信息
        def update_tools_message(self, tools_id, tools_avatar, tools_name, tools_introduce, tools_link, tools_type,
                                 tools_jianjie):
            tools = db.session.query(Tools).filter_by(tools_id=tools_id).first()
            if session['role'] == "admin":
                tools_check = 1
            else:
                tools_check = 0
            tools.tools_avatar = tools_avatar
            tools.tools_name = tools_name
            tools.tools_introduce = tools_introduce
            tools.tools_link = tools_link
            tools.tools_type = tools_type
            tools.tools_jianjie = tools_jianjie
            tools.tools_check = tools_check
            db.session.commit()

        # 删除工具信息
        def delete_tools_message(self, tools_id):
            tools = db.session.query(Tools).filter(Tools.tools_id == tools_id).first()
            if tools:
                # 找到对应的编辑设置信息
                db.session.delete(tools)
                db.session.commit()
                return True
            else:
                # 未找到
                return False

        # 审核提交的工具提交信息
        def switch_checked(self, tools_id):
            row = db.session.query(Tools).filter_by(tools_id=tools_id).first()
            if row.tools_check == 0:
                row.tools_check = 1
            else:
                row.tools_check = 0
            db.session.commit()
            return row.tools_check  # 将当前最新状态返回给控制层

        # 根据某个指定用户查询其下所有提交的工具
        def user_query_tools(self, user_id, start, count):
            result = db.session.query(Tools, Users).join(Users, Users.userid == Tools.tools_userid).filter(
                Users.userid == user_id ,Tools.tools_check == 1 # 添加一个条件来指定要查询的用户ID
            ).order_by(Tools.tools_id.desc()).limit(count).offset(
                start).all()
            return result

        # 根据某个指定用户查询其下所有提交工具的数量 (已经通过审核)
        def get_count_user_tools(self, user_id):
            result = db.session.query(Tools, Users).join(Users, Users.userid == Tools.tools_userid).filter(
                Users.userid == user_id, Tools.tools_check == 1  # 添加一个条件来指定要查询的用户ID
            ).count()
            return result

        # 根据某个指定用户查询其下所有未通过审核的工具的数量
        def get_count_user_tools_unchecked(self, user_id):
            result = db.session.query(Tools, Users).join(Users, Users.userid == Tools.tools_userid).filter(
                Users.userid == user_id, Tools.tools_check == 0  # 添加一个条件来指定要查询的用户ID
            ).count()
            return result

        # 在个人工具中心对于每个用户的提交的工具按照名称模糊查询(不分页)
        def find_by_name_tools_userid(self, tools_name, userid):
            result = db.session.query(Tools, Users).join(Users, Users.userid == Tools.tools_userid).filter(
                Tools.tools_userid == userid,Tools.tools_check == 1,
                Tools.tools_name.like('%' + tools_name + '%'),
            ).order_by(Tools.tools_id.desc()).all()
            return result

        # 查询tools表中的所有数据并返回结果集
        def find_all_tools(self, start, count):
            result = db.session.query(Tools).join(Users, Users.userid == Tools.tools_userid).order_by(
                Tools.tools_id.desc()).limit(count).offset(
                start).all()
            return result

            # 查询所有工具的数量

        def get_count_all_tools(self):
            result = db.session.query(Tools).join(Users, Users.userid == Tools.tools_userid,
                                                  ).filter(Tools.tools_check == 1).count()
            return result

        # 查询所有未通过审核的工具的数量
        def get_count_all_tools_unchecked(self):
            result = db.session.query(Tools, Users).join(Users, Users.userid == Tools.tools_userid,
                                                         ).filter(
                Tools.tools_check == 0
            ).count()
            return result

        # 查询不同分类工具的数量（按照一级分类)
        def get_count_type_tools(self, major_category):
            result = db.session.query(Tools).filter(Tools.tools_type.startswith(major_category),
                                                    Tools.tools_check == 1).count()
            return result

        # 查询当前用户提交的不同分类工具的数量（按照一级分类)
        def get_count_type_tools_user(self, major_category, userid):
            result = db.session.query(Tools).filter(Tools.tools_type.startswith(major_category),
                                                    Tools.tools_userid == userid,
                                                    Tools.tools_check == 1).count()
            return result

        # 按照工具分类进行查询(该方法直接返回工具总数量用于分页)
        def find_by_type_tools(self, start, count, category):
            if category == 0:
                result = self.find_all_tools(start, count)
                total = self.get_count_all_tools()
            else:
                result = db.session.query(Tools).join(Users,
                                                      Users.userid == Tools.tools_userid).filter(
                    Tools.tools_type == category).order_by(
                    Tools.tools_id.desc()).limit(count).offset(start).all()

                total = db.session.query(Tools).filter(Tools.tools_type == category).count()
            return result, total  # 返回分页结果集和不分页的总数量

        # 按照工具名称模糊查询(不分页)
        def find_by_tools_name(self, headline):
            result = db.session.query(Tools).join(Users, Users.userid == Tools.tools_userid).filter(
                Tools.tools_name.like('%' + headline + '%')
            ).order_by(Tools.tools_id.desc()).all()
            return result

        # 按照作者昵称模糊查询( 不分页)
        def find_by_mingzi_tools(self, nickname):
            result = db.session.query(Tools).join(Users, Users.userid == Tools.tools_userid).filter(
                Tools.tools_user_nickname.like('%' + nickname + '%')
            ).order_by(Tools.tools_id.desc()).all()
            return result
