from .models import Project, Function, File, Line, CallGraph
import ast
from CodePedia.celery import app
from suds.client import Client
from .models import File, Function
from qa.models import Question


# 导入工程
@app.task
def import_project(obj_id):
    project = Project.objects.get(id=obj_id)
    project_path = project.path
    project_id = project.id
    client = Client('http://localhost:7778/pro?wsdl', cache=None, timeout=50000)
    response = client.service.getMethodAndCallGraph(project_path)
    response = ast.literal_eval(response)
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
        project.files += 1
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
        project.functions += 1
        function.save()
        for index, line in enumerate(method['lineNum']):
            codeline = Line.objects.get(project_id=project_id, file_id=file.id, file_linenum=line)
            codeline.function_id = function.id
            codeline.function_linenum = index + 1
            codeline.save()

    for callee in callees:
        callee_function = Function.objects.filter(project_id=project_id, function_index=callee['index']).first()
        for caller in callee['caller_indexs']:
            caller_function = Function.objects.filter(project_id=project_id, function_index=caller).first()
            callgraph = CallGraph()
            callgraph.callee_function_id = callee_function.id
            callgraph.caller_function_id = caller_function.id
            callgraph.project_id = project_id
            callgraph.save()


# 定时添加问题
@app.task()
def add_question(obj_id):
    unquestion_files = File.objects.filter(has_question=0)
    unquestion_functions = Function.objects.filter(has_question=0)
    for file in unquestion_files:
        Question.objects.create(content='这个代码片段实现的主要功能是什么，你是如何理解这段代码的?',
                                function_content='这个代码片段实现的主要功能是什么，你是如何理解这段代码的?',
                                object_id=file.id,
                                user_id=1,
                                question_type=3,
                                question_level='jd',
                                vote_up=0,
                                vote_down=0,
                                question_source=1,
                                content_type_id=17,
                                file_id=file.id,
                                file_linenum=0,
                                )
        file.has_question = 1
        file.save()
    for function in unquestion_functions:
        Question.objects.create(content='这个代码片段实现的主要功能是什么，你是如何理解这段代码的?',
                                function_content='这个代码片段实现的主要功能是什么，你是如何理解这段代码的?',
                                object_id=function.id,
                                user_id=1,
                                question_type=3,
                                question_level='jd',
                                vote_up=0,
                                vote_down=0,
                                question_source=1,
                                content_type_id=18,
                                file_id=function.file_id,
                                file_linenum=0,
                                function_id=function.id,
                                function_linenum=0,
                                )
        function.has_question = 1
        function.save()


