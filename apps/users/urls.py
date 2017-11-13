from django.conf.urls import url
from .views import RegisterView, LoginView, ActiveView, LogoutView, UserinfoView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),

]
