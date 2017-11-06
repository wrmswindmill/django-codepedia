from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend #通过邮箱登陆
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import RegisterForm, LoginForm, ForgetForm, UserInfoForm
from django.contrib.auth.hashers import make_password #把明文密码加密
from .tasks import send_type_email
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import requests
import json

#通过类实现邮箱登陆
class CustomBackend(ModelBackend):  #通过邮箱登陆
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'shared/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email = user_name):
                return render(request,'shared/register.html', {
                    'register_form': register_form,
                    'msg': '用户已经存在'
                })
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'shared/register.html', {
                    'register_form': register_form,
                    'msg': '密码不一样'
                })
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pwd1)
            user_profile.save()

            send_type_email.delay(user_name, 'register')
            return render(request, 'shared/login.html')
        else:
            return render(request, 'shared/register.html', {'register_form': register_form})


#用户激活
class ActiveView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code= active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'shared/active_fail.html')
        return render(request, 'shared/login.html')


# #用户登陆
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'shared/login.html', {})
#
#     def post(self, request):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user_name = request.POST.get('username', '')
#             pass_word = request.POST.get('password', '')
#             user = authenticate(username=user_name, password=pass_word)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse('index'))
#                 else:
#                     return render(request, 'shared/login.html', {'msg': '用户未激活!'})
#             else:
#                 return render(request, 'shared/login.html', {'msg': '用户名或密码错误!'})
#         else:
#             return render(request, 'shared/login.html', {'login_form': login_form})




# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, 'shared/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user_params = {'username':user_name,'password':pass_word}
            trustie_url = 'https://www.trustie.net/account/codepedia_login'
            response = requests.get(trustie_url, params=user_params)
            response = json.loads(response.text)
            status = response['status']
            if status == 1:
                user_message = response['user']['user']
                email = user_message['mail']
                exist_records = UserProfile.objects.filter(email=email).first()
                if not exist_records:
                    user = UserProfile()
                    user.username = user_name
                    user.password = make_password(pass_word)
                    user.email = email
                    if user_message['lastname']:
                        user.nick_name = user_message['lastname']
                    elif user_message['nickname']:
                        user.nick_name = user_message['nickname']
                    else:
                        user.nick_name = user_message['firstname']
                    user.is_active = True
                    user.save()
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'shared/login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'shared/login.html', {'login_form': login_form})

#用户登出
class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_type_email(email, 'forget')
            return render(request, 'users/email_send_success.html')
        else:
            return render(request, 'users/', {'forget_form': forget_form})


class UserinfoView( View):
    """
    用户个人信息
    """
    def get(self, request):
        user = UserProfile.objects.get(id= request.user.id)
        return render(request, 'users/user_info.html', {'user':user})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

#404页面
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('common/404.html',{})
    response.status_code =404
    return response

#500错误
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('common/500.html',{})
    response.status_code = 500
    return response



