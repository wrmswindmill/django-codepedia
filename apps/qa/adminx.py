import xadmin
from .models import Question, Answer


class QuestionAdmin(object):
    list_display = ['user', 'object_id', 'content_type', 'question_level', 'question_type']
    search_field = ['user',  'object_id', 'content_type', 'question_level', 'question_type']
    list_filter = ['user',  'object_id', 'content_type', 'question_level', 'question_type']


class AnswerAdmin(object):
    list_display = ['user', 'question']
    search_field = ['user', 'question']
    list_filter = ['user', 'question']





xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Answer, AnswerAdmin)