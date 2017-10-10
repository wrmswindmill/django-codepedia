from django.shortcuts import render
from django.views import View
from .forms import NewProjectForm, QuestionForm
from .models import Project, File, Function, Line, CallGraph, Annotation, Comment
from users.models import UserProfile
from suds.client import Client
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
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
            project_path = project.path
            project_id = project.id
            client = Client('http://localhost:7777/pro?wsdl')
            response = client.service.getMethodAndCallGraph(project_path)
            response = json.loads(response)
            blobs = response['files']
            methods = response['methods']
            callees = response['callees']
            # 导入文件
            for blob in blobs:
                file = File()
                file.project_id = project_id
                file.name = blob['path'].split('/')[-1]
                file.path = blob['path'].replace(project_path, '')
                file.relpath = "/".join(blob['path'].replace(project_path, '').split('/')[0:-1])
                if 'comment' in blob.keys():
                    file.note = blob['comment']
                file.code = blob['code']
                file.file_index = blob['id']
                file.save()
                project.files +=1
                project.save()
                for index, line in enumerate(blob['codeList']):
                    codeline = Line()
                    codeline.file_linenum = index + 1
                    codeline.file_id = file.id
                    codeline.project_id = project_id
                    codeline.code = line
                    codeline.save()
            # 导入函数
            for method in methods:
                function = Function()
                function.project_id = project_id
                file = File.objects.get(project_id=project_id, file_index=method['file_index'])
                function.file_id = file.id
                function.name = method['name']
                function.path = method['path'].replace(project_path, '')
                function.function_index = method['id']
                function.code = method['code']
                function.save()
                for index,line in enumerate(method['lineNum']):
                    codeline = Line.objects.get(project_id=project_id, file_id=file.id, file_linenum=line)
                    codeline.function_id = function.id
                    codeline.function_linenum = index+1
                    codeline.save()
                    project.functions += 1
                    project.save()

            for callee in callees:
                callee_function = Function.objects.get(project_id=project_id, function_index=callee['index'])
                for caller in callee['caller_indexs']:
                    caller_function = Function.objects.get(project_id=project_id, function_index=caller)
                    callgraph = CallGraph()
                    callgraph.callee_function = callee_function
                    callgraph.caller_function = caller_function
                    callgraph.project_id = project_id
                    callgraph.save()

            all_projects = Project.objects.all()
            return render(request, 'projects/project_list.html', {'all_projects': all_projects})
        else:
            return render(request, 'projects/new.html', {'project_form': project_form})


class ProjectListView(View):
    def get(self,request):
        all_projects = Project.objects.all()
        return render(request, 'projects/project_list.html', {'all_projects': all_projects,
                                                      })


class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
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


def tree_method(request, project_id):
    project = Project.objects.get(id=project_id)
    client = Client('http://localhost:7777/pro?wsdl')
    response = client.service.getTree(project.path)
    response = json.loads(response)
    return JsonResponse(response)


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


class FileDetailView(View):
    def get(self, request, project_id, file_id):
        project = Project.objects.get(id=project_id)
        file = File.objects.get(id=file_id)
        file.views +=1
        file.save()
        lines = Line.objects.filter(file_id=file_id)
        questions = file.questions.all()
        question_form = QuestionForm()
        return render(request, 'projects/file.html', {'project': project,
                                                      'file': file,
                                                      'lines': lines,
                                                      'all_questions': questions,
                                                      'question_form': question_form,
                                                      })


class FunctionDetailView(View):
    def get(self, request, project_id, file_id, function_id):
        project = Project.objects.get(id=project_id)
        file = File.objects.get(id=file_id)
        function = Function.objects.get(id=function_id)
        function.views +=1
        function.save()
        lines = Line.objects.filter(function_id=function_id)
        questions = function.questions.all()
        question_form = QuestionForm()
        return render(request, 'projects/function.html', {'project': project,
                                                      'file': file,
                                                      'function': function,
                                                      'lines': lines,
                                                      'all_questions': questions,
                                                      'question_form':question_form
                                                        })


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


