from django.conf.urls import url
from .views import UserVoteView, UserAnnotationView, UserCommentView, JudgeUserAnnotateView, UpdateAnnotationView
urlpatterns = [
    #新建工程
    url(r'^add_vote/$', UserVoteView.as_view(), name='add_vote'),
    # 添加注释
    url(r'^new_annotation/$', UserAnnotationView.as_view(), name='new_annotation'),
    # 修改注释
    url(r'^edit_annotation/$', UpdateAnnotationView.as_view(), name='edit_annotation'),
    # 添加评论
    url(r'^new_comment/$', UserCommentView.as_view(), name='new_comment'),
    # 检测用户是否已经注释过
    url(r'^judge_user_annotation', JudgeUserAnnotateView.as_view(), name='judge_user_annotation')
    ]