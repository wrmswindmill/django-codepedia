from django.db import models
from taggit.managers import TaggableManager
from users.models import UserProfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from qa.models import Question
# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='编程语言')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "编程语言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='工程名称')
    path = models.CharField(max_length=200, verbose_name='工程全路径')
    rel_path = models.CharField(max_length=200, null=True, verbose_name='工程相对路径')
    language = models.ForeignKey(Language, verbose_name='编程语言')
    github = models.URLField(max_length=100, verbose_name='Github网址')
    ossean = models.URLField(max_length=100, verbose_name='Ossean网址')
    tags = TaggableManager()
    files = models.IntegerField(default=0, verbose_name='文件数量')
    functions = models.IntegerField(default=0, verbose_name='方法数量')
    views = models.IntegerField(default=0, verbose_name='点击数量')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "工程"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['views', ]),
            models.Index(fields=['created', ]),

        ]

    def __str__(self):
        return self.name


class File(models.Model):
    project = models.ForeignKey(Project, verbose_name='工程名称')
    user = models.ForeignKey(UserProfile,default='1', verbose_name='用户')
    name = models.CharField(max_length=255, verbose_name='文件名称')
    path = models.CharField(max_length=200, verbose_name='文件全路径')
    relpath = models.CharField(max_length=200, verbose_name='文件所处路径')
    views = models.IntegerField(default=0, verbose_name='点击数量')
    anno_nums = models.IntegerField(default=0, verbose_name='注释数量')
    summary = models.CharField(max_length=300, default='', verbose_name='摘要')
    note = models.TextField(default='',  verbose_name='首行注释')
    has_summary = models.BooleanField(default=False, verbose_name='是否有注释')
    file_index = models.IntegerField(default=0, verbose_name='文件索引')
    questions = GenericRelation(Question)
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    code = models.TextField(default='', verbose_name='代码')
    has_question = models.BooleanField(default=False, verbose_name='是否添加0行问题')
    has_sonar = models.BooleanField(default=False, verbose_name='是否通过sonar获取问题')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['views', ]),
            models.Index(fields=['created', ]),

        ]

    def __str__(self):
        return '文件{0}_{1}'.format(self.id, self.name)

    def get_vote_num(self):
        return self.vote_up -self.vote_down

    def get_question_num(self):
        return self.questions.count()




class Function(models.Model):
    project = models.ForeignKey(Project, verbose_name='工程名称')
    user = models.ForeignKey(UserProfile, default='1', verbose_name='用户')
    file = models.ForeignKey(File, verbose_name='文件名称')
    name = models.CharField(max_length=255, verbose_name='函数名称')
    path = models.CharField(max_length=200, verbose_name='函数路径')
    views = models.IntegerField(default=0, verbose_name='点击数量')
    anno_nums = models.IntegerField(default=0, verbose_name='注释数量')
    summary = models.CharField(max_length=300, default='',  verbose_name='摘要')
    note = models.TextField(default='',  verbose_name='首行注释')
    has_summary = models.BooleanField(default=False, verbose_name='是否有注释')
    function_index = models.IntegerField(default=0, verbose_name='函数索引')
    questions = GenericRelation(Question)
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    code = models.TextField(default='', verbose_name='代码')
    has_question = models.BooleanField(default=False, verbose_name='是否添加0行问题')
    has_sonar = models.BooleanField(default=False, verbose_name='是否通过sonar获取问题')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "函数"
        verbose_name_plural = verbose_name
        ordering = ['-views']

    def __str__(self):
        return '函数{0}_{1}'.format(self.id, self.name)

    def get_vote_num(self):
        return self.vote_up -self.vote_down

    def get_question_num(self):
        return self.questions.count()


class Annotation(models.Model):
    content = models.TextField(default='', verbose_name='内容')
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    limit = models.Q(app_label='projects')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, verbose_name=u"点赞对象")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"数据ID")
    content_object = GenericForeignKey('content_type', 'object_id')
    project = models.ForeignKey(Project, verbose_name='工程', null=True, related_name='project_anno')
    file = models.ForeignKey(File, verbose_name='文件', null=True,  related_name='file_anno')
    function = models.ForeignKey(Function, verbose_name='函数', null=True,  related_name='function_anno')
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"回答时间")

    class Meta:
        verbose_name = u"注释"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['object_id', 'user_id', ]),
        ]

    def __str__(self):
        return '注释{0}'.format(self.id)

    def get_vote_num(self):
        return self.vote_up -self.vote_down


class Line(models.Model):
    project = models.ForeignKey(Project, verbose_name='工程名称')
    user = models.ForeignKey(UserProfile, default='1', verbose_name='用户')
    file = models.ForeignKey(File, verbose_name='文件名称')
    function = models.ForeignKey(Function, verbose_name='函数', null=True)
    file_linenum = models.IntegerField(verbose_name='文件行号')
    function_linenum = models.IntegerField(verbose_name='函数行号', null=True)
    code = models.TextField(default='', verbose_name='代码')
    annotations = GenericRelation(Annotation)
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "代码行"
        verbose_name_plural = verbose_name



class CallGraph(models.Model):
    project = models.ForeignKey(Project, verbose_name='工程名称')
    callee_function = models.ForeignKey(Function, verbose_name='被调用函数', related_name='callee')
    caller_function = models.ForeignKey(Function, verbose_name='调用函数', related_name='caller')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "调用关系"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    content = models.TextField(default='', verbose_name='内容')
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    annotation = models.ForeignKey(Annotation, verbose_name='注释', related_name='annotation_comment')
    project = models.ForeignKey(Project, verbose_name='工程', null=True, related_name='project_comment')
    file = models.ForeignKey(File, verbose_name='文件', null=True, related_name='file_comment')
    function = models.ForeignKey(Function, verbose_name='函数', null=True, related_name='function_comment')
    vote_up = models.IntegerField(default=0, verbose_name='点赞数量')
    vote_down = models.IntegerField(default=0, verbose_name='点踩数量')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"回答时间")

    class Meta:
        verbose_name = u"评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '评论{0}'.format(self.id)

    def get_vote_num(self):
        return self.vote_up -self.vote_down


class Meta:
    app_label = u"问答管理"



