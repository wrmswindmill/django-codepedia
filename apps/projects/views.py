from django.shortcuts import render
from django.views import View
from .forms import NewProjectForm, QuestionForm
from .models import Project, File, Function, Line, CallGraph, Annotation, Comment
from users.models import UserProfile
from suds.client import Client
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse, HttpResponse
from .tasks import import_project
from qa.models import Question
from utils.choose_question import choose_question_type_1


#新建工程页面
class NewProjectView(View):
    def get(self, request):
        project_form = NewProjectForm()
        return render(request, 'projects/new.html', {'project_form': project_form})

    def post(self,request):
        project_form = NewProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.save()
            project_form.save_m2m()
            project_id = project.id
            import_project.delay(project_id)
            all_projects = Project.objects.all()
            return render(request, 'projects/project_list.html', {'all_projects': all_projects})
        else:
            return render(request, 'projects/new.html', {'project_form': project_form})


#工程列表页
class ProjectListView(View):
    def get(self, request):
        all_projects = Project.objects.all()
        # 工程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == '':
                all_projects = all_projects.order_by('-created')
            elif sort == 'hot':
                all_projects = all_projects.order_by('-views')
        return render(request, 'projects/project_list.html', {'all_projects': all_projects,
                                                              'sort':sort,
                                                      })


#工程详情页
class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project.views +=1
        project.save()
        all_files = File.objects.filter(project_id = project.id)
        hot_blobs = File.objects.order_by('-views')[:5]


        #分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_files, 10,  request=request)
        files = p.page(page)

        return render(request, 'projects/detail.html', {'project': project,
                                                        'all_files': files,
                                                        'hot_blobs': hot_blobs,
                                                      })


#文件列表页
class FileListlView(View):
    def get(self, request):
        all_files = File.objects.all()
        hot_blobs = File.objects.order_by('-views')[:5]

        #分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_files, 10,  request=request)
        files = p.page(page)

        return render(request, 'projects/file_list.html', {
                                                        'all_files': files,
                                                        'hot_objs': hot_blobs,
                                                      })


#函数列表页
class FunctionListlView(View):
    def get(self, request):
        all_functions = Function.objects.all()
        hot_functions = Function.objects.all().order_by('-views')[:5]

        #分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_functions, 10,  request=request)
        functions = p.page(page)

        return render(request, 'projects/function_list.html', {
                                                        'all_functions': functions,
                                                        'hot_objs': hot_functions,
                                                      })


#获取工程树形结构
def tree_method(request, project_id):
    project = Project.objects.get(id=project_id)
    client = Client('http://localhost:7777/pro?wsdl')
    response = client.service.getTree(project.path)
    response = json.loads(response)
    return JsonResponse(response)


#获取文件的方法
def find_function(request, project_id, file_id):
    file = File.objects.get(id=file_id)
    functions = file.function_set.all()
    all_functions = {'text': 'Functions', 'children': [], 'state': {'opened': 'true', 'selected': 'true'}}
    i = 0
    project_id =str(project_id)
    file_id = str(file_id)

    for function in functions:
        url = "/projects/%s/files/%s/functions/%s"%(project_id, file_id, function.id)
        all_functions['children'].append({'text': function.name, 'id': function.id, 'icon': 'glyphicon glyphicon-leaf',
                                           "a_attr": {"href": url}})
        i+=1
    return JsonResponse(all_functions)


#指定路径下的文件列表
class ProjectPathFileView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        path = request.GET.get('relpath', '')
        path = '/'+'/'.join(path.split('/')[1:])
        path_files = File.objects.filter(project_id=project_id, relpath__icontains=path)
        hot_blobs = File.objects.order_by('-views')[:5]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(path_files, 10,  request=request)
        files = p.page(page)
        return render(request, 'projects/path.html', {'project': project,
                                                        'all_files': files,
                                                        'hot_blobs': hot_blobs,
                                                      })


#指定文件下的文件详情
class PathFileView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        path = request.GET.get('path','')
        file = File.objects.get(path=path)
        lines = Line.objects.filter(file_id=file.id)
        questions = file.questions.all()
        return render(request, 'projects/file.html', {'project': project,
                                                      'file': file,
                                                      'lines': lines,
                                                      'all_questions': questions,
                                                      })


#文件详情页
class FileDetailView(View):
    def get(self, request, project_id, file_id):
        project = Project.objects.get(id=project_id)
        file = File.objects.get(id=file_id)
        file.views += 1
        file.save()
        lines = Line.objects.filter(file_id=file_id)
        questions = choose_question_type_1('file', file.id)
        hot_quetions = file.questions.order_by('vote_up')[:5]
        question_form = QuestionForm()
        return render(request, 'projects/file.html', {'project': project,
                                                      'file': file,
                                                      'lines': lines,
                                                      'all_questions': questions,
                                                      'question_form': question_form,
                                                      'hot_quetions': hot_quetions,
                                                      })


#函数详情页
class FunctionDetailView(View):
    def get(self, request, project_id, file_id, function_id):
        project = Project.objects.get(id=project_id)
        file = File.objects.get(id=file_id)
        function = Function.objects.get(id=function_id)
        function.views +=1
        function.save()
        lines = Line.objects.filter(function_id=function.id)
        questions = choose_question_type_1('function', function.id)
        hot_quetions = Question.objects.filter(function_id=function_id).order_by('vote_up')[:5]
        question_form = QuestionForm()
        return render(request, 'projects/function.html', {'project': project,
                                                      'file': file,
                                                      'function': function,
                                                      'lines': lines,
                                                      'all_questions': questions,
                                                      'question_form':question_form,
                                                      'hot_quetions': hot_quetions,
                                                    })


#函数调用关系
def callee_tree(request, project_id, file_id, function_id):
    function = Function.objects.get(id=function_id)
    # 函数本身处于caller处
    caller_functions = function.caller.all()
    callee_trees = {'text': 'Callee', 'children': [],  'state': {'opened': 'true', 'selected': 'true'}}
    for caller in caller_functions:
        callee = caller.callee_function
        url = "/projects/%s/files/%s/functions/%s" % (project_id, file_id, callee.id)
        callee_trees['children'].append({'text': callee.name,
                                        'id': callee.id,
                                        'icon': 'glyphicon glyphicon-leaf',
                                        "a_attr": {"href": url}
                                        })
    return JsonResponse(callee_trees)


def caller_tree(request, project_id, file_id, function_id):
    function = Function.objects.get(id=function_id)
    # 函数本身处于callee处
    callee_functions = function.callee.all()
    caller_trees = {'text': 'Caller', 'children': [],  'state': {'opened': 'true', 'selected': 'true'}}
    for callee in callee_functions:
        caller = callee.caller_function
        url = "/projects/%s/files/%s/functions/%s" % (project_id, file_id, caller.id)
        caller_trees['children'].append({'text': caller.name,
                                        'id': caller.id,
                                        'icon': 'glyphicon glyphicon-leaf',
                                        "a_attr": {"href": url}
                                        })
    return JsonResponse(caller_trees)


