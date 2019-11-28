# -*- coding: utf-8 -*-
import json
import tinify
import schedule, requests
import os, time, smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  # 发送多个部分
from email.mime.text import MIMEText  # 专门发送正文

# 配置图片压缩
tinify.key = 'mhDgfkycPsLfqZyrB5D8TrqlXR8fKPt2'


def job():
    if (datetime.now().strftime("%H:%M") == "09:12"):
        holiday(time.strftime("%Y-%m-%d", time.localtime()), "早上")
    else:
        holiday(time.strftime("%Y-%m-%d", time.localtime()), "晚上")


def holiday(time, text):
    url = "https://tool.bitefu.net/jiari/?d=" + time
    response = json.loads(requests.get(url).text)
    if (response == 0):
        daka(text)
    else:
        print("不用打卡")


def daka(text):
    os.system('adb kill-server')
    os.system('adb start-server')
    os.system('adb shell input keyevent 26')
    os.system('adb shell am force-stop com.alibaba.android.rimet')
    os.system('adb shell am start -n com.alibaba.android.rimet/com.alibaba.android.rimet.biz.LaunchHomeActivity')
    time.sleep(20)
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')
    source = tinify.from_file("autojump.png")
    source.to_file("autojump.png")
    send_email(text)


def send_email(text):
    msg = MIMEMultipart()
    msg['Subject'] = '钉钉自动打卡'  # 主题
    msg['From'] = '248276846@qq.com'  # 发件人
    msg['To'] = '898763215@qq.com'  # 收件人
    # 正文
    part_text = MIMEText('Hello 易大宝' + time.strftime("%Y-%m-%d", time.localtime()) + text + "成功打卡")
    msg.attach(part_text)  # 把正文加到邮件体里面去
    with open('autojump.png', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename='tp.png')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='autojump.png')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    # 发送邮件 SMTP
    smtp = smtplib.SMTP('smtp.qq.com', 25)  # 连接服务器，SMTP_SSL是安全传输
    smtp.login('248276846@qq.com', 'jhsejyfnsblzcbec')
    smtp.sendmail('248276846@qq.com', '898763215@qq.com', msg.as_string())  # 发送邮件
    print('邮件发送成功！')
    #删除图片
    if os.path.exists('autojump.png'):
        os.remove('autojump.png')
    else:
        print('图片删除失败！')

if __name__ == '__main__':
    schedule.every().day.at("09:09").do(job)
    schedule.every().day.at("18:00").do(job)
    while True:
        # 启动服务，run_pending()运行所有可以运行的任务
        schedule.run_pending()
        time.sleep(1)
