from django.contrib import admin
import xadmin
from xadmin import views
from xadmin.plugins.auth import  UserAdmin


from .models import EmailVerifyRecord , UserProfile, Grade


class BaseSetting(object):
    # 主题
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    #管理页头 和底部
    site_title = "CodePedia Admin"
    site_footer = "Trustie-Group"
    #折叠菜单
    menu_style = "accordion"

class GradeAdmin(object):
    list_display = ['name', 'year']

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Grade, GradeAdmin)