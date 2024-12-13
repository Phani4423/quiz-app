from django.shortcuts import render, redirect
# Create your views here.
from django.http import JsonResponse
from .models import Question, UserAnswer
import random

# View to start quiz
def start_quiz(request):
    UserAnswer.objects.all().delete()  # Reset user answers
    return render(request, 'index.html')

# View to get a random question
def get_question(request):
    questions = Question.objects.exclude(id__in=UserAnswer.objects.values_list('question_id', flat=True))
    if questions.exists():
        question = random.choice(questions)
        return render(request, 'question.html', {'question': question})
    else:
        return redirect('result')
def submit_answer(request):
    question_id = int(request.POST['question_id'])
    selected_option = int(request.POST['selected_option'])

    question = Question.objects.get(id=question_id)
    is_correct = question.correct_option == selected_option

    UserAnswer.objects.create(
        question=question,
        selected_option=selected_option,
        is_correct=is_correct
    )

    return redirect('get_question')

# View to show results
def result(request):
    answers = UserAnswer.objects.all()
    correct_count = answers.filter(is_correct=True).count()
    total_count = answers.count()
    return render(request, 'result.html', {
        'answers': answers,
        'correct_count': correct_count,
        'total_count': total_count
    })