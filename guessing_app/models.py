from django.db import models

# Create your models here.
class Categorie(models.Model):
    category = models.CharField(verbose_name="Category name", max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.category

class FullQuiz(models.Model):
    category = models.ManyToManyField(Categorie)
    question = models.CharField(max_length=255)
    points = models.IntegerField()
    system_answer = models.CharField(max_length=50)

    def __str__(self):
        return self.question
    
class QuizAnswer(models.Model):
    question = models.ForeignKey(FullQuiz, on_delete=models.CASCADE, primary_key=True)
    user_answer = models.CharField(max_length=50, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user_answer
    
class History(models.Model):
    username = models.CharField(max_length=50, default='Unknown')
    category = models.CharField(max_length=255, default='Unknown')
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username