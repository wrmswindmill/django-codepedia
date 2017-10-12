from django.shortcuts import render
from django.views import View
from django.contrib.contenttypes.models import ContentType

from projects.models import File, Function, Line, Annotation, Comment
from qa.models import Question, Answer
from utils.mixin_utils import LoginRequiredMixin
from .models import UserVote
import json


from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
# Create your views here.


class UserVoteView(View):
    def post(self, request):
        vote_id = request.POST.get('vote_id', 0)
        vote_type = request.POST.get('vote_type', '')
        vote_value = request.POST.get('vote_value', 0)
        # 判断用户是否登陆
        if not request.user.is_authenticated():
            # return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            return HttpResponse(json.dumps({"status":"fail","msg":"用户未登录"}), content_type='application/json')
        model = ContentType.objects.get(model=vote_type)
        exist_records = UserVote.objects.filter(user=request.user, vote_id=int(vote_id), vote_type=model.id)
        if exist_records:
            # 记录已经存在，则取消用户点赞或点踩
            value = exist_records.first().vote_value
            exist_records.delete()
            if value == 1:
                if vote_type == 'file':
                    a = File.objects.get(id=int(vote_id))
                    a.vote_up -=1
                    a.save()
                elif vote_type == 'function':
                    a = Function.objects.get(id=int(vote_id))
                    a.vote_up -= 1
                    a.save()
                elif vote_type == 'annotation':
                    a = Annotation.objects.get(id=int(vote_id))
                    a.vote_up -= 1
                    a.save()
                elif vote_type == 'question':
                    a = Question.objects.get(id=int(vote_id))
                    a.vote_up -= 1
                    a.save()
                elif vote_type == 'answer':
                    a = Answer.objects.get(id=int(vote_id))
                    a.vote_up -= 1
                    a.save()
                return HttpResponse('{"status":"success", "info":"cancel","value":"-1","msg": "取消成功"}', content_type='application/json')
            else:
                if vote_type == 'file':
                    a = File.objects.get(id=int(vote_id))
                    a.vote_down -= 1
                    a.save()
                elif vote_type == 'function':
                    a = Function.objects.get(id=int(vote_id))
                    a.vote_down -= 1
                    a.save()
                elif vote_type == 'annotation':
                    a = Annotation.objects.get(id=int(vote_id))
                    a.vote_down -= 1
                    a.save()
                elif vote_type == 'question':
                    a = Question.objects.get(id=int(vote_id))
                    a.vote_down -= 1
                    a.save()
                elif vote_type == 'answer':
                    a = Answer.objects.get(id=int(vote_id))
                    a.vote_down -= 1
                    a.save()
                return HttpResponse('{"status":"success", "info":"cancel","value":"1","msg": "取消成功"}',
                                    content_type='application/json')
        else:
            user_vote = UserVote()
            if int(vote_id) > 0 and vote_type is not '':
                user_vote.user = request.user
                user_vote.vote_type_id = model.id
                user_vote.vote_id = int(vote_id)
                user_vote.vote_value = int(vote_value)
                user_vote.save()
                if int(vote_value) ==1:
                    if vote_type == 'file':
                        a = File.objects.get(id=int(vote_id))
                        a.vote_up +=1
                        a.save()
                    elif vote_type == 'function':
                        a = Function.objects.get(id=int(vote_id))
                        a.vote_up += 1
                        a.save()
                    elif vote_type == 'annotation':
                        a = Annotation.objects.get(id=int(vote_id))
                        a.vote_up += 1
                        a.save()
                    elif vote_type == 'question':
                        a = Question.objects.get(id=int(vote_id))
                        a.vote_up += 1
                        a.save()
                    elif vote_type == 'answer':
                        a = Answer.objects.get(id=int(vote_id))
                        a.vote_up += 1
                        a.save()
                    return HttpResponse('{"status":"success","msg":"点赞成功"}', content_type='application/json')
                else:
                    if vote_type == 'file':
                        a = File.objects.get(id=int(vote_id))
                        a.vote_down +=1
                        a.save()
                    elif vote_type == 'function':
                        a = Function.objects.get(id=int(vote_id))
                        a.vote_down += 1
                        a.save()
                    elif vote_type == 'annotation':
                        a = Annotation.objects.get(id=int(vote_id))
                        a.vote_down += 1
                        a.save()
                    elif vote_type == 'question':
                        a = Question.objects.get(id=int(vote_id))
                        a.vote_down += 1
                        a.save()
                    elif vote_type == 'answer':
                        a = Answer.objects.get(id=int(vote_id))
                        a.vote_down += 1
                        a.save()
                    return HttpResponse('{"status":"success","msg":"点踩成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"失败"}', content_type='application/json')


class UserAnnotationView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status":"fail","msg":"用户未登录"}), content_type='application/json')
        content = request.POST.get('content', '')
        line_id = request.POST.get('line_id', '')
        if int(line_id) > 0 and content:
            annotation = Annotation()
            line = Line.objects.get(id=line_id)
            file = File.objects.get(id=line.file_id)

            annotation.line_id = line.id
            annotation.file_id = line.file.id
            annotation.content_object = line
            if line.function is not None:
                annotation.function_id = line.function.id
            annotation.project_id = line.project.id
            annotation.content = content
            annotation.user = request.user
            annotation.save()
            file.anno_nums +=1
            file.save()
            if line.function_id:
                function = Function.objects.get(id=line.function_id)
                function.anno_nums +=1
                function.save()
            return HttpResponse('{"status":"success","msg":"注释成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"注释失败"}', content_type='application/json')


class UserCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status":"fail","msg":"用户未登录"}), content_type='application/json')
        content = request.POST.get('content', '')
        annotation_id = request.POST.get('annotation_id', '')
        if int(annotation_id) > 0 and content:
            comment = Comment()
            annotation = Annotation.objects.get(id=annotation_id)
            comment.annotation_id = annotation.id
            comment.file_id = annotation.file.id
            if annotation.function is not None:
                comment.function_id = annotation.function.id
            comment.project_id = annotation.project.id
            comment.content = content
            comment.user = request.user
            comment.save()
            return HttpResponse('{"status":"success","msg":"注释成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"注释失败"}', content_type='application/json')

