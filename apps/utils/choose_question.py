from projects.models import File, Function
from qa.models import Question, Answer


# 轮流题型 先出系统题在出用户题
# def choose_question_type_1(model, id):
#     if model== 'file':
#         all_questions_origin = Question.objects.filter(file_id=id)
#     else:
#         all_questions_origin = Question.objects.filter(function_id=id)
#     all_linenums_tuple = list(all_questions_origin.values_list('file_linenum').order_by('file_linenum').distinct())
#     # 取出所有包含问题的代码行号
#     all_linenums = [list(x)[0] for x in all_linenums_tuple]
#
#
#     index = 2
#     all_questions = []
#     for linenum in all_linenums:
#         if linenum == 0:
#             question = all_questions_origin.get(file_linenum=0)
#         elif linenum == -1:
#              continue
#         else:
#
#             if index > 3:
#                 index = 1
#             question = all_questions_origin.filter(file_linenum=linenum, question_info=index).first()
#
#             index += 1
#         all_questions.append(question)
#
#
#     for linenum in all_linenums:
#         if linenum == -1:
#             questions = all_questions_origin.filter(file_linenum=-1)
#             for question in questions:
#                 all_questions.append(question)
#     return all_questions


def choose_question_type_1(model, id):
    if model== 'file':
        all_questions_origin = Question.objects.filter(file_id=id)
    else:
        all_questions_origin = Question.objects.filter(function_id=id)
    all_linenums_tuple = list(all_questions_origin.values_list('file_linenum').order_by('file_linenum').distinct())
    # 取出所有包含问题的代码行号
    all_linenums = [list(x)[0] for x in all_linenums_tuple]
    # 问题数量
    count = 0
    # 问题的index
    index = 2
    # 所有问题的集合
    all_questions = {}
    for linenum in all_linenums:
        all_questions[linenum] = []
        if linenum == 0:
            try:
                sys_question = all_questions_origin.get(file_linenum=0)
                all_questions[linenum].append(sys_question)
                count += 1
            except:
                pass
        else:
            if index > 3:
                index = 1
            sys_question = all_questions_origin.filter(file_linenum=linenum, question_info=index).first()
            if sys_question is not None:
                all_questions[linenum].append(sys_question)
                count += 1
                index += 1
            user_questions = all_questions_origin.filter(file_linenum=linenum, question_source=2)
            for question in user_questions:
                all_questions[linenum].append(question)
                count += 1
    return {'question': all_questions, 'count': count}