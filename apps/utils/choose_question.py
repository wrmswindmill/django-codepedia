from projects.models import File, Function
from qa.models import Question, Answer


# 轮流题型 先出系统题在出用户题
def choose_question_type_1(model, id):
    if model== 'file':
        all_questions_origin = Question.objects.filter(file_id=id)
    else:
        all_questions_origin = Question.objects.filter(function_id=id)
    all_linenums = []
    all_linenums_tuple = list(all_questions_origin.distinct().values_list('file_linenum'))
    for linenum in all_linenums_tuple:
        all_linenums.append(linenum[0])
    index = 1
    all_questions = []
    for linenum in all_linenums:
        if linenum == -1:
            continue
        if model == 'file':
            question = Question.objects.filter(file_id=id, file_linenum=linenum, question_info=index).first()
            index += 1
            if not question:
                question = Question.objects.filter(file_id=id, file_linenum=linenum).first()
        else:
            question = Question.objects.filter(function_id=id, file_linenum=linenum, question_info=index).first()
            index += 1
            if not question:
                question = Question.objects.filter(function_id=id, file_linenum=linenum).first()
        all_questions.append(question)
        if index == 3:
            index = 1
    for linenum in all_linenums:
        if linenum == -1 :
            if model == 'file':
                questions = Question.objects.filter(file_id=id, file_linenum=-1)
            else:
                questions = Question.objects.filter(function_id=id, file_linenum=-1)
            for question in questions:
                all_questions.append(question)
    return all_questions