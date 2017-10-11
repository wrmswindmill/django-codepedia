from django.conf.urls import url, include
from .views import NewQuestionView,  NewAnswerView, EvaluateOptionQuestion

urlpatterns = [
    url(r'^new_question/$', NewQuestionView.as_view(), name='new_question'),
    url(r'^new_answer/$', NewAnswerView.as_view(), name='new_answer'),
    url(r'^evaluate_answer/$', EvaluateOptionQuestion.as_view(), name='evaluate_answer'),

]