# _*_ encoding:utf-8 _*_

from django.contrib import admin
import xadmin
from .models import Project, Language, File, Function, Line, CallGraph, Annotation, Comment


class ProjectAdmin(object):
    list_display = ['name', 'path', 'rel_path', 'github', 'ossean', 'language', 'tags']
    search_field = ['name', 'path', 'rel_path', 'github', 'ossean', 'language', 'tags']
    list_filter = ['name', 'path', 'rel_path', 'github', 'ossean', 'language', 'tags']


class FileAdmin(object):
    list_display = ['name', 'project', 'path', 'relpath', 'views', 'anno_nums', 'summary', 'note', 'has_summary']
    search_field = ['name', 'project', 'path', 'relpath', 'views', 'anno_nums', 'summary', 'note', 'has_summary']
    list_filter = ['name', 'project', 'path', 'relpath', 'views', 'anno_nums', 'summary', 'note', 'has_summary']


class FunctionAdmin(object):
    list_display = ['name', 'project', 'file', 'path', 'views', 'anno_nums', 'summary', 'note', 'has_summary']
    search_field = ['name', 'project', 'file',  'path', 'views', 'anno_nums', 'summary', 'note', 'has_summary']
    list_filter = ['name', 'project', 'file', 'path', 'views', 'anno_nums', 'summary', 'note', 'has_summary']


class LineAdmin(object):
    list_display = ['project', 'file', 'function']
    search_field = ['project', 'file', 'function']
    list_filter = ['project', 'file', 'function']


class LanguageAdmin(object):
    list_display = ['name']
    search_field =['name']
    list_filter = ['name']


class CallGraphAdmin(object):
    list_display = ['project', 'callee_function', 'caller_function']
    search_field = ['project', 'callee_function', 'caller_function']
    list_filter = ['project', 'callee_function', 'caller_function']


class AnnotationAdmin(object):
    list_display = ['user', 'object_id', 'content_type', 'project', 'file', 'function']
    search_field = ['user', 'object_id', 'content_type', 'project', 'file', 'function']
    list_filter = ['user', 'object_id', 'content_type', 'project', 'file', 'function']


class CommentAdmin(object):
    list_display = ['user', 'annotation', 'project', 'file', 'function']
    search_field = ['user', 'annotation', 'project', 'file', 'function']
    list_filter = ['user', 'annotation', 'project', 'file', 'function']

xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(File, FileAdmin)
xadmin.site.register(Function, FunctionAdmin)
xadmin.site.register(Line, LineAdmin)
xadmin.site.register(CallGraph, CallGraphAdmin)
xadmin.site.register(Language, LanguageAdmin)
xadmin.site.register(Annotation, AnnotationAdmin)
xadmin.site.register(Comment, CommentAdmin)