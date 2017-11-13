from CodePedia.celery import app
from .models import EmailVerifyRecord
from django.core.mail import send_mail
from CodePedia.settings import EMAIL_FROM
from utils.email_send import random_str
from celery import shared_task



@shared_task
def send_type_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'CodePedia注册激活链接'
        email_body = '请点击下面的链接激活你的账号: http://codepedia.trustie.net/users/active/{0}'.format(code)
        send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == 'forget':
        email_title = 'CodePedia密码重置链接'
        email_body = '请点击下面的链接重置你的账号: ttp://codepedia.trustie.net/users/reset/{0}'.format(code)
        send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == 'update_email':
        email_title = 'CodePedia邮箱修改链接'
        email_body = '你的邮箱验证码为{0}'.format(code)
        send_mail(email_title, email_body, EMAIL_FROM, [email])