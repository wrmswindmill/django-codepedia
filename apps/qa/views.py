from django.shortcuts import render
from django.views import View
from qa.models import Question, Answer
from projects.forms import QuestionForm
from projects.models import Function, File
from django.http import HttpResponse
# Create your views here.


class NewFileQuestionView(View):
    def post(self, request, file_id):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        content = request.POST.get('content', '')

        if int(file_id) >0 and content:
            question = Question()
            file = File.objects.get(id=file_id)
            question.content =  content
            question.content_object = file
            question.question_type = '2'
            question.user = request.user
            question.save()
            return HttpResponse('{"status":"success","msg":"提问成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提问失败"}', content_type='application/json')


class NewFunctionQuestionView(View):
    def post(self, request, function_id):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        content = request.POST.get('content', '')
        if int(function_id) > 0 and content:
            question = Question()
            function = Function.objects.get(id=function_id)
            question.content =  content
            question.content_object = function
            question.question_type = '2'
            question.user = request.user
            question.save()
            return HttpResponse('{"status":"success","msg":"提问成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提问失败"}', content_type='application/json')


class NewAnswerView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        content = request.POST.get('content', '')
        question_id = request.POST.get('question_id', '')
        if int(question_id) > 0 and content:
            answer = Answer()
            question = Question.objects.get(id=question_id)
            answer.question_id = question.id
            answer.content =  content
            answer.user = request.user
            answer.save()
            return HttpResponse('{"status":"success","msg":"提问成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提问失败"}', content_type='application/json')

