from django.db.models import QuerySet
from django.http import QueryDict


def checking_answers(questions: QuerySet, answers: QueryDict) -> tuple:
    """
    Проверяет ответы и возвращает статус прохождения,
    количество правильных ответов, и количество правильных ответов пользователя.
    """
    count_answers = 0
    count_correct_answers = 0
    count_correct_answers_user = 0

    for question, answer in zip(questions, answers.lists()):
        a = set(map(int, answer[1]))
        b = {pk.id for pk in question.correct_answer}
        points = len(b.intersection(a))
        count_correct_answers += len(b)
        count_correct_answers_user += points

        if len(a) - points >= 0:
            count_answers += points - (len(a) - points)

    if count_answers >= questions[0].test.points:
        return True, count_correct_answers, count_correct_answers_user
    return False, count_correct_answers, count_correct_answers_user
