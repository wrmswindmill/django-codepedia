from django import template
from projects.models import Annotation
register = template.Library()


@register.assignment_tag()
# @register.simple_tag()
def user_annotation_count(request, line):
    annos = Annotation.objects.filter(content_type_id=20, object_id=line, user_id = request.user.id).first()
    count = Annotation.objects.filter(content_type_id=20, object_id=line, user_id = request.user.id).count()
    return {'annos':annos, 'count':count}


@register.simple_tag()
def get_model_name(obj):
    model_name = obj._meta.model_name
    return model_name

