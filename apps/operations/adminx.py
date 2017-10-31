import xadmin
from .models import UserMessage, UserVote
# Register your models here.
from djcelery.admin import IntervalSchedule, CrontabSchedule
from djcelery.models import *

class UserVoteAdmin(object):
    list_display = ['user', 'vote_type', 'vote_id', 'vote_value']
    search_field = ['user', 'vote_type', 'vote_id', 'vote_value']
    list_filter = ['user', 'vote_type', 'vote_id', 'vote_value']


class PeriodicTaskAdmin(object):
    pass

class TaskAdmin(object):
    list_display = ['state', 'name', 'args', 'expires']

class WorkerAdmin(object):
    pass

xadmin.site.register(UserVote, UserVoteAdmin)
xadmin.site.register(IntervalSchedule)
xadmin.site.register(CrontabSchedule)
xadmin.site.register(PeriodicTask, PeriodicTaskAdmin)
xadmin.site.register(TaskState, TaskAdmin)
xadmin.site.register(WorkerState, WorkerAdmin)