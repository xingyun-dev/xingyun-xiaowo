import random
import string
from io import BytesIO
import time
import os
from PIL import Image, ImageFont, ImageDraw
import datetime


class imagecode:
    def __init__(self, font_path):
        self.font_path = font_path
    # 生成用于绘制字符串的随机颜色
    def rand_color(self):
        red = random.randint(32, 127)
        green = random.randint(32, 255)
        blue = random.randint(0, 255)
        return (red, green, blue)

    # 生成用于绘制字符串的随机字符串
    def gen_text(self):
        # sample用于从一个大的列表或字符串中随机选取若干个元素，返回一个新的列表
        list = random.sample(string.ascii_letters + string.digits, 4)
        return ''.join(list)

    def draw_line(self, draw, num, width, height):
        for i in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill=self.rand_color())


    # 绘制验证码图片

    def draw_image(self,font_path):
        code = self.gen_text()
        width, height = 120, 50  # 图片大小
        # 创建图片对象,并设定背景色为白色
        im = Image.new('RGB', (width, height), 'white')
        # 选择使用何种字体及字体大小
        font = ImageFont.truetype(font_path, 40)
        draw = ImageDraw.Draw(im)  # 创建画笔对象
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)

        # 绘制干扰线
        self.draw_line(draw, 5, width, height)
        # im.show()
        return im, code

    # 生成图片验证码并返回给控制器
    def get_code(self):
        font_dir = 'common'  # 字体文件所在的目录
        font_filename = 'Arial.ttf'  # 字体文件名
        font_path = os.path.join(font_dir, font_filename)  # 构建完整路径
        image, code = self.draw_image(font_path)
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return bstring, code


# 发送邮件验证码
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


# 发送QQ邮箱验证码,参数为收件箱地址和随机生成的验证码
def send_email(receiver, ecode):
    # 邮箱账号和发件者签名
    sender = 'xxx <你的邮箱账号>'
    # 定义发送邮件的内容,支持HTML标签和CSS样式
    content = f"<br/>欢迎来到星云小窝，您的邮箱验证码为：<span style='color:red;font-size:20px;'>{ecode}</span>，请在4分钟内填写完成注册，如非本人操作，请忽略此邮件。"
    # 实例化邮件对象,并指定邮件的关键信息。
    message = MIMEText(content, 'html', 'utf-8')
    # 指定邮件的标题,同样使用utf-8编码
    message['Subject'] = Header('星云小窝注册验证码', 'utf-8')
    message['From'] = sender  # 指定发件人信息
    message['To'] = receiver  # 指定收件人邮箱地址

    smtpObj = SMTP_SSL('smtp.qq.com')  # 建立与QQ邮箱服务器的SSL连接
    # 通过邮箱账号和获取到的授权码登录邮箱服务器
    smtpObj.login('你的邮箱账号', '你的授权码')
    # 指定发件人、收件人和邮件内容
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()


# 生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)


# 单个模型类转标准的python字典列表
def model_list(result):
    list = []
    for row in result:
        dict = {}
        for k, v in row.__dict__.items():
            if not k.startswith("_sa_instance_state"):
                # 如果某个字段的值是datetime类型,则将其格式为字符串
                if isinstance(v, datetime.datetime):
                    v = v.strftime("%Y-%m-%d %H:%M:%S")
                dict[k] = v
        list.append(dict)

    return list


# SQLAlchemy连接查询两张表的结果转换为[{},{}]
# Comment,Users, [(comment,users),(comment,users),()....]
def model_join_list(result):
    list = []
    for obj1, obj2 in result:
        dict = {}
        for k1, v1 in obj1.__dict__.items():
            if not k1.startswith("_sa_instance_state"):
                if not k1 in dict:  # 如果字典中存在相同的类则跳过(比如两个表中都有userid)
                    dict[k1] = v1
        for k2, v2 in obj2.__dict__.items():
            if not k2.startswith("_sa_instance_state"):
                if not k2 in dict:
                    dict[k2] = v2
        list.append(dict)

    return list


# 压缩图片,通过参数width指定压缩后的图片大小
def compress_image(source, dest, width):
    from PIL import Image
    # 如果图片宽度大于1200,则调整为1200的宽度
    im = Image.open(source)
    if im.mode == 'RGBA':
        im = im.convert('RGB')

    x, y = im.size  # 获取图片的宽和高
    if x > width:
        # 等比例缩放
        ys = int(y * width / x)
        xs = width
        # 调整当前图片的尺寸(同时也会压缩大小)
        temp = im.resize((xs, ys), Image.LANCZOS)
        # 将图片保存并使用80%的质量进行压缩
        temp.save(dest, quality=80)
    # 如果尺寸小于指定宽度则不缩减尺寸,只压缩保存
    else:
        im.save(dest, quality=80)


def compress_image_md(source, dest, target_size, quality=80):
    # 打开图片
    im = Image.open(source)

    if im.mode == 'RGBA':
        im = im.convert('RGB')

    original_width, original_height = im.size  # 获取图片原始宽和高

    # 如果图片的任意一边大于目标尺寸，则等比例缩放图片
    ratio_w = target_size[0] / original_width
    ratio_h = target_size[1] / original_height
    ratio = min(ratio_w, ratio_h) if ratio_w != ratio_h else ratio_w

    if ratio < 1:
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        temp = im.resize((new_width, new_height), resample=Image.LANCZOS)
    else:
        temp = im.copy()  # 尺寸小于等于指定尺寸时不缩放，直接复制图像

    # 将压缩后的图片保存，并指定质量
    temp.save(dest, quality=quality)


# 解析文章内容中的图片地址
# def parse_image_url(content):
#     import re
#     # 匹配图片地址
#     temp_list = re.findall('<img src="(.+?)"', content)
#     # 匹配Markdown图片地址
#     # temp_list = re.findall('!\[.*?]\((.*?)\)', content)
#     url_list = []
#     for url in temp_list:
#         # 如果图片类型为gif，则直接跳过,不对其进行任何处理
#         if url.lower().endswith('.gif'):
#             continue
#         else:
#             url_list.append(url)
#     return url_list

import re
def extract_markdown_image_paths(content):
    pattern = r'\(/upload/[^)]*\.png\)'

    image_paths = re.findall(pattern, content)
    cleaned_paths = [path[1:-1] for path in image_paths]  # 去掉括号
    return cleaned_paths

def parse_image_url(content):
    # 匹配图片地址
    temp_list = re.findall('<img src="(.+?)"', content)
    temp_list += extract_markdown_image_paths(content)
    print(temp_list)
    url_list = []
    for url in temp_list:
        # 如果图片类型为gif，则直接跳过,不对其进行任何处理
        if url.lower().endswith('.gif'):
            continue
        else:
            url_list.append(url)
    return url_list




# 远程下载指定URL的图片,并保存到临时目录中
def download_image(url, dest):
    import requests
    import certifi
    res = requests.get(url, verify=False)  # 获图片响应
    # 将图片以二进制方式保存到指定文件中
    with open(file=dest, mode='wb') as f:
        f.write(res.content)


# 解析列表中的图片URL地址并生成缩略图,返回缩略图名称
def generate_thumb(url_list):
    # 根据URL地址解析出其文件名和域名
    # 通常建议使用文章内容中的第一张图片来生成缩略图
    # 先遍历url_list,查找里面是否存在本地上传图片,找到即处理,代码运行结束

    for url in url_list:
        if url.startswith("/upload/"):
            filename = url.split("/")[-1]
            # 找到本地图片后对其进行压缩处理,设置缩略图宽度为400像素即可
            compress_image('./resource/upload/' + filename, './resource/thumb/' + filename, 400)
            return filename

    # 如果在内容中没有找到本地图片,则需要先将网络图片下载到本地再处理
    # 直接将第一张图片作为缩略图,并生成基于时间戳的标准文件名
    url = url_list[0]
    filename = url.split("/")[-1]
    suffix = filename.split(".")[-1]  # 取得文件的后缀名
    thumbname = time.strftime("%Y%m%d_%H%M%S." + suffix)
    download_image(url, './resource/download/' + thumbname)
    compress_image('./resource/download/' + thumbname, './resource/thumb/' + thumbname, 400)
    return thumbname  # 返回当前缩略图的文件名


from PIL import Image
import base64
import io



def handle_upload(encoded_thumbnail):
    # 解码 base64 字符串
    data_url = encoded_thumbnail
    decoded_bytes = base64.b64decode(data_url)
    image_stream = io.BytesIO(decoded_bytes)

    # 打开图片
    image = Image.open(image_stream)
    thumbname = time.strftime("%Y%m%d_%H%M%S." + "png")
    # 保存缩略图到文件
    image.save('./resource/download/' + thumbname, format='png')
    compress_image('./resource/download/' + thumbname, './resource/thumb/' + thumbname, 400)

    # 返回缩略图文件名
    return thumbname


#下载用户头像
def handle_upload_user(encoded_thumbnail):
    # 解码 base64 字符串
    data_url = encoded_thumbnail
    decoded_bytes = base64.b64decode(data_url)
    image_stream = io.BytesIO(decoded_bytes)

    # 打开图片
    image = Image.open(image_stream)
    thumbname = time.strftime("%Y%m%d_%H%M%S." + "png")
    # 保存缩略图到文件
    image.save('./resource/download/' + thumbname, format='png')
    compress_image('./resource/download/' + thumbname, './resource/chat_room/images/' + thumbname, 400)

    # 返回缩略图文件名
    return thumbname


#下载工具图标
def handle_upload_tools(encoded_thumbnail):
    # 解码 base64 字符串
    data_url = encoded_thumbnail
    decoded_bytes = base64.b64decode(data_url)
    image_stream = io.BytesIO(decoded_bytes)

    # 打开图片
    image = Image.open(image_stream)
    thumbname = time.strftime("%Y%m%d_%H%M%S." + "png")
    # 保存缩略图到文件
    image.save('./resource/download/' + thumbname, format='png')
    compress_image('./resource/download/' + thumbname, './resource/tools/img/' + thumbname, 200)

    # 返回缩略图文件名
    return thumbname





# 根据tools_type命名对应的分类信息
def ming_tools_by_type(type):
    primary_category = ""
    secondary_category = ""
    if type.startswith("1"):
        primary_category = "AI工具"
        if type == "11":
            secondary_category = "常用"
        elif type == "12":
            secondary_category = "AI图像工具"
        elif type == "13":
            secondary_category = "AI聊天工具"
        elif type == "14":
            secondary_category = "AI视频工具"
    elif type.startswith("2"):
        primary_category = "生信软件"
        if type == "21":
            secondary_category = "常用"
        elif type == "22":
            secondary_category = "基因相关"
        elif type == "23":
            secondary_category = "环境相关"
        elif type == "24":
            secondary_category = "其它"
    elif type.startswith("3"):
        primary_category = "生信网站"
        if type == "31":
            secondary_category = "常用"
        elif type == "32":
            secondary_category = "基因相关"
        elif type == "33":
            secondary_category = "环境相关"
        elif type == "34":
            secondary_category = "其它"
    elif type.startswith("4"):
        primary_category = "消息获取"
        if type == "41":
            secondary_category = "日常"
        elif type == "42":
            secondary_category = "生信相关"
        elif type == "43":
            secondary_category = "AI相关"
        elif type == "44":
            secondary_category = "古诗词文化"
    elif type == "5":
        primary_category = "设计美化"

    elif type == "6":
        primary_category = "学习网站"

    elif type == "7":
        primary_category = "其他"

    return primary_category, secondary_category

