from django.conf import settings as original_settings
from projects.models import Project, File, Function


def settings(request):
    return {'settings': original_settings}


def ip_address(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def get_web_stat(request):
    project_nums = Project.objects.all().count()
    file_nums = File.objects.all().count()
    function_nums = Function.objects.all().count()
    nums = {'project_nums': project_nums, 'file_nums': file_nums, 'function_nums': function_nums}

    return {'nums':nums}


def get_hot_projects(request):
    hot_projects = Project.objects.all()[:5]
    return {'hot_projects': hot_projects}