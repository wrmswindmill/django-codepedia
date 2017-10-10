import xadmin
from .models import UserMessage, UserVote
# Register your models here.

class UserVoteAdmin(object):
    list_display = ['user', 'vote_type', 'vote_id', 'vote_value']
    search_field = ['user', 'vote_type', 'vote_id', 'vote_value']
    list_filter = ['user', 'vote_type', 'vote_id', 'vote_value']

xadmin.site.register(UserVote, UserVoteAdmin)