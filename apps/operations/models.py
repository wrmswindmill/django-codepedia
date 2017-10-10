from django.db import models
from users.models import UserProfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from projects.models import Project, File, Function, Line
# Create your models here.


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接受用户")
    message = models.CharField(max_length=200, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    created = models.DateField(auto_now_add=True, verbose_name=u"消息时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserVote(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    limit = models.Q(app_label='projects', model='project')|models.Q(app_label='projects', model='file')|models.Q(app_label='projects', model='function')|\
            models.Q(app_label='projects', model='annotation')|models.Q(app_label='projects', model= 'comment')| models.Q(app_label='qa', model='question')|\
            models.Q(app_label='qa', model='answer')
    vote_type = models.ForeignKey(ContentType, limit_choices_to=limit, verbose_name= u"点赞对象")
    vote_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"数据ID")
    content_object = GenericForeignKey('vote_type', 'vote_id')
    vote_value = models.IntegerField(choices=((1, '点赞'), ( -1, '点踩')), default=0, verbose_name='类型')
    created = models.DateField(auto_now_add=True, verbose_name=u"收藏时间")

    class Meta:
        verbose_name = u"用户点赞"
        verbose_name_plural = verbose_name


