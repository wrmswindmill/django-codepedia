from projects.models import File, Function
from qa.models import Question, Answer


def create_question_tree(request, obj):
    all_questions = obj.questions.all()
    question_tree = {}

    # for question in all_questions:
    #     if