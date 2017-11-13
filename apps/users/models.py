from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now, timedelta

# Create your models here.


class Grade(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"班级名称", default="")
    year = models.IntegerField(null=True, verbose_name=u"年份")
    college = models.CharField(max_length=50, verbose_name=u"学院", default="")
    school = models.CharField(max_length=50, verbose_name=u"学校", default="")

    class Meta:
        verbose_name = "班级信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.school + ' '+self.college + ' '+ self.name


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female","女")), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    grade = models.ForeignKey(Grade, verbose_name='班级', null=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/users/default.png", max_length=100)
    role = models.CharField(max_length=3, choices=(('1', '学生'), ('2', '老师')))
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def last_three_day_annotation(self):
        from projects.models import Annotation
        date = now().date() + timedelta(days=-3)

        last_three_day_num = Annotation.objects.filter(user_id=self.id, created__gt=date).count()
        return last_three_day_num


    def last_week_annotation(self):
        from projects.models import Annotation
        date = now().date() + timedelta(days=-7)

        last_week_annotation_num = Annotation.objects.filter(user_id=self.id, created__gt=date).count()
        return last_week_annotation_num


    def total_annotation(self):
        from projects.models import Annotation
        total_num = Annotation.objects.filter(user_id=self.id).count()
        return total_num

    total_annotation.short_description = u'总注释数量'
    last_week_annotation.short_description = '最近一周注释数量'
    last_three_day_annotation.short_description = '最近三天注释数量'

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u'验证码类型', choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'修改邮箱')), max_length=30)
    send_time = models.DateTimeField(verbose_name=u'发送时间', auto_now_add=True)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)





