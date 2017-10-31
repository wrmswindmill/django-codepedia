from django import template
from projects.models import Annotation
from qa.models import Answer, QuestionStandardAnswers, Question
from operations.models import UserVote
from django.contrib.contenttypes.models import ContentType

from users.models import UserProfile
register = template.Library()


# @register.assignment_tag(takes_context=True)
@register.simple_tag()
def user_annotation_count(request, line):
    user = request.user
    annos = Annotation.objects.filter(object_id=line, user_id = request.user.id).first()
    has_anno = Annotation.objects.filter(object_id=line, user_id = request.user.id)
    return {'annos':annos, 'has_anno':has_anno}


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


@register.simple_tag()
def set_index_initial():
    index = 1
    return index


@register.assignment_tag()
def get_line_question(obj, line, index):
    model = obj._meta.model_name
    has_question = False
    if model == 'file':
        question = Question.objects.filter(file_id=obj.id, file_linenum=line.file_linenum, question_info=index).first()
    else:
        question = Question.objects.filter(function_id=obj.id, function_linenum=line.function_linenum, question_info=index).first()
    if question:
        has_question = True
        if index == 3:
            index = 1
        else:
            index = index + 1
    return {'question': question, 'has_question': has_question, 'index': index}


@register.assignment_tag()
def judge_user_vote(request, vote_type, vote_id):
    ctype_id = ContentType.objects.get(model=vote_type).id
    exist_record = UserVote.objects.filter(user_id = request.user.id, vote_type_id=ctype_id, vote_id=vote_id).first()
    if  exist_record:
        return exist_record.vote_value
    else:
        return 0



