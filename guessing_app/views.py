from django.shortcuts import render
from django.template import loader
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    categories = Categorie.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'home.html', context)

class QuestionsList(generic.ListView):
    model = FullQuiz
    template_name = 'questions.html'
    context_object_name = 'questions'

def category_questions(request, category):
    category_name = Categorie.objects.get(category=category)
    context = {
        'category_name' : category_name
    }
    return render(request, 'categoryquiz.html', context)

def question_detail(request, category, id):
    category_name = Categorie.objects.get(category=category)

    set  = category_name.fullquiz_set.all()
    question = set.get(id=id)
    context = {
        'question' : question,
    }
    return render(request, 'question_detail.html', context)

def game(request, category):
    category_selected = Categorie.objects.get(category=category)
    questions_to_user = category_selected.fullquiz_set.all()
    

    
    context = {
        'questions_to_user' : questions_to_user,
    }
    return render(request, 'game.html', context)

def submitted(request, category):
    category_selected = Categorie.objects.get(category=category)
    questions = category_selected.fullquiz_set.all()
    
    
    try:
        total_score = 0
        for question in questions:

            if request.method == 'POST':
                answer = request.POST[question.question]
                if answer[:len(question.system_answer)].lower() == question.system_answer.lower():
                    score = question.points
                else:
                    score = 0
                total_score += score
                
                to_db = question.quizanswer_set.create(user_answer=answer, score=score)
                to_db.save()
                
        result_data = QuizAnswer.objects.all()
        return render(request, 'results.html', {'result_data' : result_data, 'total_score' : total_score})
    except IntegrityError as e:
        ram_data = QuizAnswer.objects.all()
        ram_data.delete()

        total_score = 0
        for question in questions:

            if request.method == 'POST':
                answer = request.POST[question.question]
                if answer[:len(question.system_answer)].lower() == question.system_answer.lower():
                    score = question.points
                else:
                    score = 0
                total_score += score
                
                to_db = question.quizanswer_set.create(user_answer=answer, score=score)
                to_db.save()
                
        result_data = QuizAnswer.objects.all()
        return render(request, 'results.html', {'result_data' : result_data, 'total_score' : total_score})

        return HttpResponseRedirect(reverse('guessing_app:game', args=(category,)))


def complete(request, category):
    add_to_history = QuizAnswer.objects.all()
    for i in add_to_history:
        categories = i.question.category.all()
        
        if len(categories) > 0:
            categories_append = ''
            for history_category in categories:
                categories_append += history_category.category + ", "
        else:
            categories_append = 'Unknown'
        
        history = History(category=categories_append ,question=i.question, answer=i.user_answer, score=i.score)
        history.save()
        history_list = History.objects.all()
        if len(history_list) > 20:
            x = len(history_list) - 20
            for delete_history in history_list[0:x]:
                delete_history.delete()
    ram_data = QuizAnswer.objects.all()
    ram_data.delete()
    return redirect('guessing_app:history')

class HistoryListView(generic.ListView):
    model = History
    template_name = 'history.html'
    context_object_name = 'histories'
