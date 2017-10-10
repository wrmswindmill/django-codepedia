from django.conf.urls import url
from .views import NewProjectView, ProjectListView, ProjectDetailView, tree_method, ProjectPathFileView, FileDetailView, PathFileView
from .views import find_function, FunctionDetailView, callee_tree, caller_tree, FileListlView
urlpatterns = [
    #新建工程
    url(r'^new/$', NewProjectView.as_view(), name='new_project'),
    #工程列表
    url(r'^$', ProjectListView.as_view(), name='project_list'),
    #工程详情
    url(r'^(?P<project_id>\d+)/$', ProjectDetailView.as_view(), name='project_detail'),
    # 访问webservice获取文件路径结构
    url(r'^tree_method/(?P<project_id>\d+)/$', tree_method, name='project_tree'),
    # 访问api获取文件下到所有方法
    url(r'^(?P<project_id>\d+)/files/(?P<file_id>\d+)/find_function/$', find_function , name='file_function'),
    #指定文件夹下的所有文件
    url(r'^detail/(?P<project_id>\d+)/path_find/$', ProjectPathFileView.as_view(), name='project_path_file'),
    #文件详情
    url(r'^(?P<project_id>\d+)/files/(?P<file_id>\d+)/$', FileDetailView.as_view(), name='file_detail'),
    #在文件树里找到指定文件
    url(r'^detail/(?P<project_id>\d+)/find_file/$', PathFileView.as_view(), name='path_file'),
    # 具体函数
    url(r'^(?P<project_id>\d+)/files/(?P<file_id>\d+)/functions/(?P<function_id>\d+)/$', FunctionDetailView.as_view(), name='function_detail'),
    # 找到callee
    url(r'^(?P<project_id>\d+)/files/(?P<file_id>\d+)/functions/(?P<function_id>\d+)/callee_function/$', callee_tree, name='function_callee'),
    # 找到caller
    url(r'^(?P<project_id>\d+)/files/(?P<file_id>\d+)/functions/(?P<function_id>\d+)/caller_function/$', caller_tree, name='function_caller'),


]