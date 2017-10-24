from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)

class RegisterForm(forms.Form):  # 注册
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):   #忘记密码
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

class UserInfoForm(forms.Form):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']