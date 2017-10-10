from django.conf.urls import url, include
from .views import NewFileQuestionView, NewFunctionQuestionView, NewAnswerView

urlpatterns = [
    url(r'^new_question/(?P<file_id>\d+)/$', NewFileQuestionView.as_view(), name='new_file_question'),
    url(r'^new_question/(?P<funtion_id>\d+)/$', NewFunctionQuestionView.as_view(), name='new_function_question'),
    url(r'^new_answer/$', NewAnswerView.as_view(), name='new_answer'),
]