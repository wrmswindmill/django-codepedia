from django.conf.urls import url, include
from .views import RegisterView,LoginView,ActiveView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
]
