import random
from _init_ import mail,app
from flask_mail import Message
from db import DB
import datetime


class Verify:
    d = DB()

    #生成六位验证码
    def gen_verification_code(self):
        return random.randint(100000, 999999)

    #存储验证码
    def write_code(self, email):
        code = self.gen_verification_code()
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        try:
            self.send_email(email, code)
        except Exception:
            return 'fail'
        else:
            self.d.add_code(email, str(code), time)
            return 'success'

    #进行验证
    def verification(self, email, code):
        c = self.d.query_code_by_email(email)
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        d1 = datetime.datetime.strptime(time, '%Y-%m-%d-%H-%M')
        d2 = datetime.datetime.strptime(c.time, '%Y-%m-%d-%H-%M')
        delta = d1 - d2
        if int(str(delta).split(', ')[-1].split(':')[-2]) < 15 and int(str(delta).split(', ')[-1].split(':')[-3]) == 0 and len(str(delta).split(', ')) == 1:
            if c.code == code:
                return '验证成功'
            else:
                return '验证码错误！'
        else:
            return '验证码超时！'



    def send_email(self, email, code):
        #定义邮件内容
        msg = Message('【验证码】', sender='1250483717@qq.com', recipients=[email])
        msg.body = str(code)
        msg.html = "<h1>您的验证码是："+str(code)+"<h1>"
        with app.app_context():
            mail.send(msg)



