
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta

from flask import Blueprint, render_template, jsonify, session, request
from pyecharts.charts import Bar, Line, Pie, Scatter, Geo, Timeline
from pyecharts import options as opts
from pyecharts.globals import ChartType, ThemeType
from pyecharts.options import InitOpts

from main import inject_article_type, inject_tools_type
from model.article import Article
from model.chatroom import Message
from model.comment import Comment
from model.favorite import Favorite
from model.tb_follow import Follow
from model.tools import Tools
from model.user_shezhi import Shezhi
from model.users import Users

py_echarts = Blueprint('py_echarts', __name__)

from flask import Flask, render_template


# 获取文章类型和对应数量的字典
def get_article_type_counts():
    article = Article()  # 创建Article类的实例
    article_types = inject_article_type()['article_type']
    type_counts = {}

    # 遍历所有文章类型
    for type_key, type_name in article_types.items():
        # 调用count_by_type函数获取每种类型的数量
        count = article.count_by_type(type_key)
        # 将类型和数量添加到字典中
        type_counts[type_name] = count

    return type_counts


def pie_rosetype_admin() -> Pie:
    type_counts = get_article_type_counts()  # 获取文章类型和对应数量的字典
    labels = list(type_counts.keys())  # 获取标签（文章类型名称）
    values = list(type_counts.values())  # 获取值（对应数量）

    c = (
        Pie()
        .add(
            "",
            list(zip(labels, values)),
            radius=["30%", "70%"],
            center=["50%", "50%"],
            rosetype="area",
        )
    )
    return c


@py_echarts.route("/py_echarts/pie-article-admin")
def get_pie_chart_admin():
    c = pie_rosetype_admin()
    return c.dump_options_with_quotes()


# 用户的文章条形图
@py_echarts.route("/py_echarts/bar-article-user", methods=["POST", "GET"])
def get_bar_chart_user():
    userid = request.form.get("userid")
    article = Article()
    favorite = Favorite()
    comment = Comment()
    favorite_count = favorite.query_my_favorite_count(userid)
    favorited_count = favorite.query_my_article_favorited_count(userid)
    article_count = article.get_count_user_except_drafted(userid)
    drafted_count = article.get_count_user_drafted(user_id=userid)
    comment_count = comment.query_comments_count_by_userid(userid)
    commented_count = comment.query_comments_count_by_articleid(userid)
    read_count = article.get_readcount_by_user(userid)
    recommend_count = article.query_recommend_count_by_user(userid)
    hide_count = article.query_hide_count_by_user(userid)

    # 设置条形图的标签和值
    bar = (
        Bar()
        .add_xaxis(
            ["收藏数", "被收藏数", "文章数", "草稿数", "评论数", "被评论数", "阅读数", "推荐数", "隐藏数"])  # x轴标签

        .add_yaxis("用户文章信息",
                   [favorite_count, favorited_count, article_count, drafted_count, comment_count, commented_count,
                    read_count, recommend_count, hide_count]
                   , itemstyle_opts=opts.ItemStyleOpts(color="#749f83"))  # y轴值，对应上面的标签
    )

    return bar.dump_options_with_quotes()


# 用户的关注条形图
@py_echarts.route("/py_echarts/bar-followed-user", methods=["POST", "GET"])
def get_bar_followed_user():
    userid = request.form.get("userid")
    follow = Follow()
    follow_count = follow.get_follow_by_userid_count(userid)
    followed_count = follow.get_followed_user_count(userid)
    mutal_follow_count = follow.get_mutal_follow_count(userid)

    # 设置条形图的标签和值
    bar = (
        Bar()
        .add_xaxis(
            ["关注用户数量", "被关注数量", "互相关注数量"])  # x轴标签

        .add_yaxis("用户文章信息",
                   [follow_count, followed_count, mutal_follow_count]
                   , itemstyle_opts=opts.ItemStyleOpts(color="#008000"))  # y轴值，对应上面的标签
    )

    return bar.dump_options_with_quotes()


# 用户的交流条形图
@py_echarts.route("/py_echarts/bar-communicate-user", methods=["POST", "GET"])
def get_bar_communicate_user():
    userid = request.form.get("userid")
    message = Message()
    message_duo_count = message.get_messagesduo_user_count(userid)
    message_one_count = message.get_messagesone_user_count(userid)
    sixin_count = message.get_sixin_user_count(userid)
    # 设置条形图的标签和值
    bar = (
        Bar()
        .add_xaxis(
            ["公共聊天数量", "一对一聊天数量", "私信数量"])  # x轴标签

        .add_yaxis("用户交流信息",
                   [message_duo_count, message_one_count, sixin_count]
                   , itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"))  # y轴值，对应上面的标签
    )

    return bar.dump_options_with_quotes()


# 网站的交流条形图
@py_echarts.route("/py_echarts/bar-communicate-admin", methods=["POST", "GET"])
def get_bar_communicate_admin():
    message = Message()
    message_duo_count = message.get_messagesduo_all_count()
    message_one_count = message.get_messagesone_all_count()
    message_zong_count = message.get_messages_all_count()
    # 设置条形图的标签和值
    bar = (
        Bar()
        .add_xaxis(
            ["公共聊天数量", "一对一聊天数量", "信息总量"])  # x轴标签

        .add_yaxis("网站交流信息",
                   [message_duo_count, message_one_count, message_zong_count]
                   , itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"))  # y轴值，对应上面的标签
    )

    return bar.dump_options_with_quotes()


# 网站的文章条形图
@py_echarts.route("/py_echarts/bar-article-admin")
def get_bar_chart_admin():
    article = Article()
    favorite = Favorite()
    comment = Comment()
    article_count = article.get_count_all_except_drafted()
    drafted_count = article.get_count_all_drafted()
    favorited_count = favorite.query_all_favorited_count()
    # read_count = article.get_readcount_by_all()
    hide_count = article.query_hide_count_by_all()
    recommend_count = article.query_recommend_count_by_all()
    comment_count = comment.query_comments_count_by_all()

    # 设置条形图的标签和值
    bar = (
        Bar()
        .add_xaxis(
            ["文章总量", "草稿总量", "被收藏文章总量", "被隐藏文章总量", "被推荐文章总量",
             "评论总量"])  # x轴标签

        .add_yaxis("用户文章信息",
                   [article_count, drafted_count, favorited_count, hide_count, recommend_count,
                    comment_count]
                   , itemstyle_opts=opts.ItemStyleOpts(color="#749f83"))  # y轴值，对应上面的标签
    )

    return bar.dump_options_with_quotes()


# 用户的文章饼图
@py_echarts.route("/py_echarts/pie-article-user", methods=['POST', "GET"])
def get_pie_chart_user():
    userid = request.form.get("userid")
    article = Article()  # 创建Article类的实例
    article_types = inject_article_type()['article_type']
    type_counts = {}

    # 遍历所有文章类型
    for type_key, type_name in article_types.items():
        # 调用count_by_type_user函数获取每种类型的数量
        count = article.count_by_type_user(type_key, userid)
        # 将类型和数量添加到字典中
        type_counts[type_name] = count
    labels = list(type_counts.keys())  # 获取标签（文章类型名称）
    values = list(type_counts.values())  # 获取值（对应数量）

    c = (
        Pie()
        .add(
            "",
            list(zip(labels, values)),
            radius=["30%", "70%"],
            center=["50%", "50%"],
            rosetype="area",
        )
    )
    return c.dump_options_with_quotes()


# 用户的工具饼图
@py_echarts.route("/py_echarts/pie-tools-user", methods=['POST', "GET"])
def get_pie_tools_user():
    userid = request.form.get("userid")
    tools = Tools()
    tools_types = inject_tools_type()['tools_type']
    type_counts = {}

    # 遍历所有文章类型
    for type_key, type_name in tools_types.items():
        # 调用count_by_type_user函数获取每种类型的数量
        count = tools.get_count_type_tools_user(type_key, userid)
        # 将类型和数量添加到字典中
        type_counts[type_name] = count
    labels = list(type_counts.keys())  # 获取标签（文章类型名称）
    values = list(type_counts.values())  # 获取值（对应数量）

    c = (
        Pie()
        .add(
            "",
            list(zip(labels, values)),
            radius=["30%", "70%"],
            center=["50%", "50%"],
            rosetype="area",
        )
    )
    return c.dump_options_with_quotes()


# 网站的工具饼图
@py_echarts.route("/py_echarts/pie-tools-admin")
def get_pie_tools_admin():
    tools = Tools()
    tools_types = inject_tools_type()['tools_type']
    type_counts = {}

    # 遍历所有文章类型
    for type_key, type_name in tools_types.items():
        # 调用count_by_type_user函数获取每种类型的数量
        count = tools.get_count_type_tools(type_key)
        # 将类型和数量添加到字典中
        type_counts[type_name] = count
    labels = list(type_counts.keys())  # 获取标签（文章类型名称）
    values = list(type_counts.values())  # 获取值（对应数量）

    c = (
        Pie()
        .add(
            "",
            list(zip(labels, values)),
            radius=["30%", "70%"],
            center=["50%", "50%"],
            rosetype="area",
        )
    )
    return c.dump_options_with_quotes()


# 用户的文章时间记录（按月份计算)
@py_echarts.route("/py_echarts/time-article-user", methods=['POST', "GET"])
def get_time_article_user():
    userid = request.form.get("userid")
    article = Article()
    article_count_time_daily = article.get_article_by_timetype_userid('daily',userid)
    article_count_time_month = article.get_article_by_timetype_userid('monthly',userid)
    article_count_time_year = article.get_article_by_timetype_userid('yearly',userid)
    yearly = article_count_time_year['yearly']
    monthly = article_count_time_month['monthly']
    daily = article_count_time_daily['daily']
    # 使用 defaultdict 来按年份和月份分组数据
    monthly_data = defaultdict(lambda: defaultdict(int))
    for year, month, article_count in monthly:
        monthly_data[year][month] += article_count  # 使用实际的文章数量来更新分组数据



    # 创建一个Timeline对象，用于存放不同年份的饼图
    tl = Timeline()
    tl.add_schema(is_auto_play=True, play_interval=1000)  # 设置Timeline的播放方式

    # 为每个年份创建一个柱状图，并添加到Timeline中
    years = sorted(monthly_data.keys())  # 获取所有年份并按顺序排序
    for year in years:
        # 获取该年份的所有月份和文章数量，并按月份排序
        months = sorted(monthly_data[year].keys())
        article_counts = [monthly_data[year][month] for month in months]

        bar = (
            Bar()
            .add_xaxis(months)  # X轴为月份，已经按1到12月排序
            .add_yaxis("文章数量", article_counts, itemstyle_opts=opts.ItemStyleOpts(color="#749f43"))  # Y轴为文章数量
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{year} 年文章数据"))
        )
        tl.add(bar, str(year))  # 将柱状图添加到Timeline中，并使用年份作为key

    # 返回Timeline对象的配置选项
    return tl.dump_options_with_quotes()




# 用户的文章时间记录（按年份计算)
@py_echarts.route("/py_echarts/time-article-user-year", methods=['POST', "GET"])
def time_article_user_year():
    article = Article()
    userid = request.form.get("userid")
    article = Article()
    article_count_time_year = article.get_article_by_timetype_userid('yearly',userid)
    yearly = article_count_time_year['yearly']

    # 创建一个Timeline对象，用于存放不同年份的饼图
    tl = Timeline()
    tl.add_schema(is_auto_play=True, play_interval=1000)  # 设置Timeline的播放方式

    # 遍历每一个年份和对应的文章数量
    for i, (year, count) in enumerate(yearly):
        # 创建饼图对象
        pie = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("文章数量", [(f"{year}年", count)], rosetype="radius", radius=["30%", "55%"])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{year}年文章数据"))
        )
        # 将饼图添加到Timeline中
        tl.add(pie, str(year))



    return tl.dump_options_with_quotes()




# 用户近20天发布文章情况
@py_echarts.route("/py_echarts/time-article-user-day", methods=['POST', "GET"])
def time_article_user_day():
    userid = request.form.get('userid')
    article = Article()
    article_count_time_daily = article.get_article_by_timetype_userid('daily',userid)
    # 获取当前日期
    today = datetime.now().date()

    # 计算20天前的日期
    twenty_days_ago = today - timedelta(days=19)

    # 从给定的日期列表中筛选出近二十天的数据，并确保日期唯一
    date_to_count = defaultdict(int)  # 使用defaultdict来存储每个日期的总计数
    for date, count in article_count_time_daily['daily']:
        if twenty_days_ago <= date <= today:
            date_to_count[date] += count  # 累加每个日期的计数

    # 获取处理后的日期和计数列表
    dates = list(date_to_count.keys())
    counts = list(date_to_count.values())

    # 使用zip将dates和counts组合成元组的列表，然后按照日期排序
    sorted_items = sorted(zip(dates, counts))

    # 使用列表推导式将排序后的元组列表拆分为两个列表：sorted_dates和sorted_counts
    sorted_dates, sorted_counts = zip(*sorted_items)

    # 转换为列表
    dates = list(sorted_dates)
    counts = list(sorted_counts)

    # 如果数据不足二十天，则填充剩余的天数为0
    while len(dates) < 20:
        yesterday = dates[-1] - timedelta(days=1)
        if twenty_days_ago <= yesterday < today:  # 确保日期在范围内
            dates.append(yesterday)
            counts.append(0)
        else:
            break

            # 创建柱状图
    bar = (
        Bar()
        .add_xaxis(dates)  # X轴为日期
        .add_yaxis("文章发布数量", counts, itemstyle_opts=opts.ItemStyleOpts(color="#749f83"))  # Y轴为文章数量

    )
    # 返回Timeline对象的配置选项
    return bar.dump_options_with_quotes()


















# 个人中心的首页
@py_echarts.route("/person/<int:userid>")
def index(userid):
    article = Article()
    tools = Tools()
    follow = Follow()
    message = Message()
    shezhi = Shezhi()
    article_count = article.get_count_user_except_drafted(userid)
    tools_count = tools.get_count_user_tools(userid)
    follow_count = follow.get_follow_by_userid_count(userid)
    message_count = message.get_messages_user_count(userid)
    user_shezhi = shezhi.get_message_from_editoruser(user_id=userid)
    user_at = Users().find_by_userid(userid)
    followed_count = follow.get_followed_user_count(userid)
    return render_template("/shujumianbang/index.html", article_count=article_count, tools_count=tools_count
                           , follow_count=follow_count, message_count=message_count, user_shezhi=user_shezhi,
                           user_at=user_at, followed_count=followed_count, userid=userid)


# 个人中心的文章数据
@py_echarts.route("/person/article/<int:userid>")
def index_article(userid):
    article = Article()
    favorite = Favorite()
    comment = Comment()
    favorite_count = favorite.query_my_favorite_count(userid)
    favorited_count = favorite.query_my_article_favorited_count(userid)
    article_count = article.get_count_user_except_drafted(userid)
    drafted_count = article.get_count_user_drafted(user_id=userid)
    comment_count = comment.query_comments_count_by_userid(userid)
    commented_count = comment.query_comments_count_by_articleid(userid)
    read_count = article.get_readcount_by_user(userid)
    user_at = Users().find_by_userid(userid)
    recommend_count = article.query_recommend_count_by_user(userid)
    hide_count = article.query_hide_count_by_user(userid)

    return render_template('/shujumianbang/index_article.html', article_count=article_count
                           , favorite_count=favorite_count, favorited_count=favorited_count,
                           drafted_count=drafted_count, comment_count=comment_count, commented_count=commented_count,
                           user_at=user_at, userid=userid, read_count=read_count,
                           recommend_count=recommend_count, hide_count=hide_count)


# 根据tools_type查询tools表中一级分类数量
def get_count_type_tools_user(majortype, userid):
    tools = Tools()
    result = tools.get_count_type_tools_user(majortype, userid)
    return result


# 个人中心的工具数据
@py_echarts.route("/person/tools/<int:userid>")
def index_tools(userid):
    tools = Tools()
    user_at = Users().find_by_userid(userid)
    tools_count = tools.get_count_user_tools(userid)
    tools_unchecked_count = tools.get_count_user_tools_unchecked(userid)
    return render_template('/shujumianbang/index_tools.html', tools_count=tools_count,
                           tools_unchecked_count=tools_unchecked_count,
                           get_count_type_tools_user=get_count_type_tools_user, userid=userid, user_at=user_at)


# 个人中心的关注数据
@py_echarts.route("/person/followed/<int:userid>")
def index_followed(userid):
    follow = Follow()
    user_at = Users().find_by_userid(userid)
    follow_count = follow.get_follow_by_userid_count(userid)
    followed_count = follow.get_followed_user_count(userid)
    mutal_follow_count = follow.get_mutal_follow_count(userid)
    return render_template('/shujumianbang/index_follow.html', follow_count=follow_count,
                           userid=userid, user_at=user_at, followed_count=followed_count,
                           mutal_follow_count=mutal_follow_count)


# 个人中心的交流数据
@py_echarts.route("/person/communicate/<int:userid>")
def index_communicate(userid):
    message = Message()
    user_at = Users().find_by_userid(userid)
    message_duo_count = message.get_messagesduo_user_count(userid)
    message_one_count = message.get_messagesone_user_count(userid)
    sixin_count = message.get_sixin_user_count(userid)
    return render_template('/shujumianbang/index_communicate.html',
                           userid=userid, user_at=user_at, message_one_count=message_one_count
                           , message_duo_count=message_duo_count, sixin_count=sixin_count)

#管理后台的文章中心
@py_echarts.route("/person/admin/article")
def article_admin():
    user_at = Users().find_by_admin()
    article = Article()
    favorite = Favorite()
    comment = Comment()
    article_count = article.get_count_all_except_drafted()
    drafted_count = article.get_count_all_drafted()
    favorited_count = favorite.query_all_favorited_count()
    read_count = article.get_readcount_by_all()
    hide_count = article.query_hide_count_by_all()
    recommend_count = article.query_recommend_count_by_all()
    comment_count = comment.query_comments_count_by_all()


    article_count_time_daily = article.get_article_by_timetype('daily')
    # 获取当前日期
    today = datetime.now().date()

    # 计算20天前的日期
    twenty_days_ago = today - timedelta(days=19)

    # 从给定的日期列表中筛选出近二十天的数据，并确保日期唯一
    date_to_count = defaultdict(int)  # 使用defaultdict来存储每个日期的总计数
    for date, count in article_count_time_daily['daily']:
        if twenty_days_ago <= date <= today:
            date_to_count[date] += count  # 累加每个日期的计数

    # 获取处理后的日期和计数列表
    dates = list(date_to_count.keys())
    counts = list(date_to_count.values())

    # 使用zip将dates和counts组合成元组的列表，然后按照日期排序
    sorted_items = sorted(zip(dates, counts))

    # 使用列表推导式将排序后的元组列表拆分为两个列表：sorted_dates和sorted_counts
    sorted_dates, sorted_counts = zip(*sorted_items)

    # 转换为列表
    dates = list(sorted_dates)
    counts = list(sorted_counts)

    # 如果数据不足二十天，则填充剩余的天数为0
    while len(dates) < 20:
        yesterday = dates[-1] - timedelta(days=1)
        if twenty_days_ago <= yesterday < today:  # 确保日期在范围内
            dates.append(yesterday)
            counts.append(0)
        else:
            break

            # 创建柱状图
    bar = (
        Bar()
        .add_xaxis(dates)  # X轴为日期
        .add_yaxis("文章发布数量", counts, itemstyle_opts=opts.ItemStyleOpts(color="#749f83"))  # Y轴为文章数量

    )

    # 生成嵌入代码
    chart_bar = bar.render_embed()

    article_count_time_year = article.get_article_by_timetype('yearly')
    yearly = article_count_time_year['yearly']

    # 创建一个Timeline对象，用于存放不同年份的饼图
    tl_pie = Timeline()
    tl_pie.add_schema(is_auto_play=True, play_interval=1000)  # 设置Timeline的播放方式

    # 遍历每一个年份和对应的文章数量
    for i, (year, count) in enumerate(yearly):
        # 创建饼图对象
        pie = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("文章数量", [(f"{year}年", count)], rosetype="radius", radius=["30%", "55%"])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{year}年文章数据"))
        )
        # 将饼图添加到Timeline中
        tl_pie.add(pie, str(year))

    tl_pie = tl_pie.render_embed()

    article_count_time_month = article.get_article_by_timetype('monthly')

    monthly = article_count_time_month['monthly']

    # 使用 defaultdict 来按年份和月份分组数据
    monthly_data = defaultdict(lambda: defaultdict(int))
    for year, month, article_count in monthly:
        monthly_data[year][month] += article_count  # 使用实际的文章数量来更新分组数据

    # 创建一个Timeline对象，用于存放不同年份的饼图
    tl_bar = Timeline()
    tl_bar.add_schema(is_auto_play=True, play_interval=1000)  # 设置Timeline的播放方式

    # 为每个年份创建一个柱状图，并添加到Timeline中
    years = sorted(monthly_data.keys())  # 获取所有年份并按顺序排序
    for year in years:
        # 获取该年份的所有月份和文章数量，并按月份排序
        months = sorted(monthly_data[year].keys())
        article_counts = [monthly_data[year][month] for month in months]

        bar = (
            Bar()
            .add_xaxis(months)  # X轴为月份，已经按1到12月排序
            .add_yaxis("文章数量", article_counts, itemstyle_opts=opts.ItemStyleOpts(color="#749f43"))  # Y轴为文章数量
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{year} 年文章数据"))
        )
        tl_bar.add(bar, str(year))  # 将柱状图添加到Timeline中，并使用年份作为key

    tl_bar = tl_bar.render_embed()

    return render_template('/shujumianbang/article_admin.html', user_at=user_at, article_count=article_count,
                           drafted_count=drafted_count, favorited_count=favorited_count, read_count=read_count,
                           hide_count=hide_count, recommend_count=recommend_count,
                           comment_count=comment_count,chart_bar=chart_bar,tl_pie=tl_pie,tl_bar=tl_bar)


# 根据tools_type查询tools表中一级分类数量
def get_count_type_tools_all(majortype):
    tools = Tools()
    result = tools.get_count_type_tools(majortype)
    return result


@py_echarts.route("/person/admin/tools")
def admin_tools():
    tools = Tools()
    user_at = Users().find_by_admin()
    tools_count = tools.get_count_all_tools()
    tools_unchecked_count = tools.get_count_all_tools_unchecked()
    return render_template('/shujumianbang/tools_admin.html', tools_count=tools_count,
                           tools_unchecked_count=tools_unchecked_count,
                           get_count_type_tools_all=get_count_type_tools_all, user_at=user_at)


# 管理后台的交流数据
@py_echarts.route("/person/admin/communicate")
def admin_communicate():
    message = Message()
    user_at = Users().find_by_admin()
    message_duo_count = message.get_messagesduo_all_count()
    message_one_count = message.get_messagesone_all_count()
    message_zong_count = message.get_messages_all_count()
    return render_template('/shujumianbang/communicate_admin.html',
                           user_at=user_at, message_one_count=message_one_count
                           , message_duo_count=message_duo_count, message_zong_count=message_zong_count)


# 管理后台的用户数据
@py_echarts.route("/person/admin/user")
def admin_user():
    user = Users()
    user_at = user.find_by_admin()
    user_count = user.get_count_all_user()
    user_locations = user.find_all_users_location()
    # 在这里执行生成地图的代码
    from pyecharts import options as opts


    # 创建 Geo 地图实例
    c = (
        Geo(InitOpts(width="1000px", height="1000px"))

        .add_schema(maptype="china")  # 设置地图类型为中国地图
    )

    data = []
    # 遍历 user_locations，添加每个用户的地理位置到地图中
    for userid, time, lon, lat in user_locations:
        # 添加坐标点，这里假设每个用户的位置都有一个唯一的名称
        # 例如，可以使用时间戳或者用户ID作为名称
        name = userid
        c.add_coordinate(name, lon, lat)
        value = str(time)  # 或者其他您想展示的值

        # 将当前用户的位置和值添加到 data 列表中
        data.append((name, value))

    series_name = "用户来源"

    c.add(series_name, data, type_=ChartType.EFFECT_SCATTER)

    # 设置系列和全局选项
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 设置标签不显示
    c.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_show=False),  # 设置视觉映射配置项，比如颜色条
        title_opts=opts.TitleOpts(title="用户地理位置分布")  # 设置图表标题
    )

    # 生成嵌入代码
    rendered_chart = c.render_embed()
    return render_template('/shujumianbang/user_admin.html',
                           user_at=user_at, user_count=user_count, chart=rendered_chart)

