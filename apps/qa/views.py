from django.shortcuts import render
from django.views import View
from qa.models import Question, Answer, QuestionStandardAnswers, QuestionComment
from projects.forms import QuestionForm
from projects.models import Function, File
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
import json
# Create your views here.


class NewQuestionView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status":"fail","msg":"用户未登录"}), content_type='application/json')
        content = request.POST.get('content', '')
        obj_type = request.POST.get('obj_type', '')
        obj_id = request.POST.get('obj_id', '')
        if int(obj_id) > 0 and content:
            question = Question()
            question.content = content
            question.user = request.user
            question.question_type = '3'
            question.question_source = '2'
            question.file_linenum = -1
            if obj_type == 'file':
                file = File.objects.get(id=obj_id)
                question.content_object = file
                question.file_id = file.id
            else:
                function = Function.objects.get(id=obj_id)
                question.content_object = function
                question.function_id = function.id
            question.save()
            return HttpResponse('{"status":"success","msg":"提问成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提问失败"}', content_type='application/json')


class NewAnswerView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户未登录"}), content_type='application/json')
        content = request.POST.get('content', '')
        question_id = request.POST.get('question_id', '')
        if int(question_id) > 0 and content:
            answer = Answer()
            question = Question.objects.get(id=question_id)
            answer.question_id = question.id
            answer.content =  content
            answer.user = request.user
            answer.save()
            return HttpResponse('{"status":"success","msg":"回答成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"回答失败，请重新回答"}', content_type='application/json')


class EvaluateOptionQuestion(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status":"fail","msg":"用户未登录"}), content_type='application/json')
        choices = request.POST.get('choices', '')
        question_id = request.POST.get('question_id', '')
        if int(question_id) > 0 and choices:
            exist_records = Answer.objects.filter(user_id=request.user.id, question_id=int(question_id))
            if exist_records:
                return HttpResponse('{"status":"success","msg":"你已经回答过这个问题"}', content_type='application/json')
            answer = Answer()
            question = Question.objects.get(id=question_id)
            question_standard_choices = QuestionStandardAnswers.objects.get(question_id=question_id).choice_position
            answer.question_id = question.id
            answer.content = choices
            answer.user = request.user
            if choices != question_standard_choices:
                answer.correct = False
                answer.save()
                return HttpResponse('{"status":"success","msg":"答案错误"}', content_type='application/json')
            answer.save()
            return HttpResponse('{"status":"success","msg":"答案正确"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"回答失败"}', content_type='application/json')


class NewQuestionCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户未登录"}), content_type='application/json')
        content = request.POST.get('content', '')
        question_id = request.POST.get('question_id', '')
        if int(question_id) > 0 and content:
            question_comment = QuestionComment()
            question = Question.objects.get(id=question_id)
            question_comment.question_id = question.id
            question_comment.content =  content
            question_comment.user = request.user
            question_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败，请重新回答"}', content_type='application/json')
