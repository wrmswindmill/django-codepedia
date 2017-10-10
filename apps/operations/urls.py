from django.conf.urls import url
from .views import UserVoteView, UserAnnotationView, UserCommentView
urlpatterns = [
    #新建工程
    url(r'^add_vote/$', UserVoteView.as_view(), name='add_vote'),
    # 添加注释
    url(r'^new_annotation/(?P<line_id>\d+)/$', UserAnnotationView.as_view(), name='new_annotation'),
    # 添加评论
    url(r'^new_comment/(?P<annotation_id>\d+)/$', UserCommentView.as_view(), name='new_comment'),
    ]