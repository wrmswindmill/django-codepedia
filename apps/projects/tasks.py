from .models import Project, Function, File, Line, CallGraph
import ast
from suds.client import Client
from CodePedia.celery import app


@app.task
def import_project(obj_id):
    project = Project.objects.get(id=obj_id)
    project_path = project.path
    project_id = project.id
    client = Client('http://localhost:7778/pro?wsdl')
    response = client.service.getMethodAndCallGraph(project_path)
    response = ast.literal_eval(response)
    blobs = response['files']
    print(blobs[0]['code'])
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
        print(file.code)
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
        callee_function = Function.objects.get(project_id=project_id, function_index=callee['index'])
        for caller in callee['caller_indexs']:
            caller_function = Function.objects.get(project_id=project_id, function_index=caller)
            callgraph = CallGraph()
            callgraph.callee_function = callee_function
            callgraph.caller_function = caller_function
            callgraph.project_id = project_id
            callgraph.save()