from django import template
from projects.models import Annotation
from qa.models import Answer, QuestionStandardAnswers
from users.models import UserProfile
register = template.Library()


@register.assignment_tag()
def user_annotation_count(user, line):
    user = UserProfile.objects.get(id = user)
    annos = Annotation.objects.filter(content_type_id=20, object_id=line, user_id = user.id).first()
    count = Annotation.objects.filter(content_type_id=20, object_id=line, user_id = user.id).count()
    return {'annos':annos, 'count':count}


@register.simple_tag()
def get_model_name(obj):
    model_name = obj._meta.model_name
    return model_name


@register.simple_tag()
def set_space(obj):
    space_num = len(obj) - len(obj.lstrip())
    space = ' ' * space_num
    return space

@register.simple_tag()
def num_to_str(obj):
    ch = chr(int(obj)+64)
    return ch

@register.assignment_tag()
def evaluate_user_answer(request, question_id):
    answers = Answer.objects.filter(question_id=question_id, user_id=request.user.id).first()
    right_answers = QuestionStandardAnswers.objects.filter(question_id=question_id).first().choice_position
    correct = False
    have_answered = False
    user_answer = ''
    if answers:
        have_answered =  True
        user_answer = ''
        for answer in answers.content:
            user_answer += chr(int(answer)+64)
            user_answer += ' '
        if answers.content == right_answers:
            correct = True
    return {'user_answer':user_answer,'have_answered':have_answered,"correct":correct}

@register.assignment_tag()
def standard_answer(question_id):
    answers = QuestionStandardAnswers.objects.filter(question_id=question_id).first()
    standard_answers = ''
    for answer in answers.choice_position:
        standard_answers += chr(int(answer) + 64)
        standard_answers += ' '
    return {'standard_answers': standard_answers}



