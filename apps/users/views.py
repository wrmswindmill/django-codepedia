from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend #通过邮箱登陆
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password #把明文密码加密
from utils.email_send import send_type_email
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


#通过类实现邮箱登陆
class CustomBackend(ModelBackend):  #通过邮箱登陆
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


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

            send_type_email(user_name, 'register')
            return render(request, 'shared/login.html')
        else:
            return render(request, 'shared/register.html', {'register_form': register_form})


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


class LoginView(View):
    def get(self, request):
        return render(request, 'shared/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'shared/login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'shared/login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'shared/login.html', {'login_form': login_form})


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('common/404.html',{})
    response.status_code =404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('common/500.html',{})
    response.status_code = 500
    return response



