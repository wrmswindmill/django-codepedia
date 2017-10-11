from django.db import models
from users.models import UserProfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Question(models.Model):
    content = models.TextField(default='', verbose_name='文件问题内容')
    function_content = models.TextField(null=True, verbose_name='函数问题内容')
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    limit = models.Q(app_label='projects')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, verbose_name=u"提问对象")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"数据ID")
    content_object = GenericForeignKey('content_type', 'object_id')
    question_source = models.CharField(choices=(('1', '系统'), ('2', '用户')), default='1', max_length=3, verbose_name='问题类型')
    question_type = models.CharField(choices=(('1', '选择题'), ('2', '判断题'), ('3', '问答题')), default='1', max_length=3, verbose_name='问题类型')
    question_level = models.CharField(choices=(('jd', '简单'), ('zd', '中等'), ('n', '难')),default='jd', max_length=5, verbose_name='问题类型')
    function_id = models.IntegerField(null=True, verbose_name=u"函数")
    file_id = models.IntegerField(null=True, verbose_name=u"方法")
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    sonar_id = models.IntegerField(default=0, verbose_name='Sonar')
    file_linenum = models.IntegerField(default=0, verbose_name='文件行号')
    function_linenum = models.IntegerField(default=0, verbose_name='问题行号')
    created = models.DateField(auto_now_add=True, verbose_name=u"提问时间")

    class Meta:
        verbose_name = u"问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '问题{0}'.format(self.id)

    def get_vote_num(self):
        return self.vote_up -self.vote_down


class QuestionChoices(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题', related_name='question_choices')
    choice_text = models.TextField(default='', verbose_name='选项内容')
    choice_position = models.CharField(default='', max_length=10, verbose_name='选项位置')
    created = models.DateField(auto_now_add=True, verbose_name=u"提问时间")

    class Meta:
        verbose_name = u"选择题选项"
        verbose_name_plural = verbose_name


class QuestionStandardAnswers(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题')
    choice_position = models.CharField(default='', max_length=10,  verbose_name='正确选项位置')
    created = models.DateField(auto_now_add=True, verbose_name=u"提问时间")

    class Meta:
        verbose_name = u"标准答案"
        verbose_name_plural = verbose_name


class Answer(models.Model):
    content = models.TextField(default='', verbose_name='内容')
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    question = models.ForeignKey(Question, verbose_name='问题')
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    correct = models.BooleanField(default=True, verbose_name='正确与否')
    created = models.DateField(auto_now_add=True, verbose_name=u"回答时间")

    class Meta:
        verbose_name = u"回答"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '回答{0}'.format(self.id)

    def get_vote_num(self):
        return self.vote_up -self.vote_down










