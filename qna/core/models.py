from django.db import models

from user.models import User


class Question(models.Model):
  title = models.CharField(max_length=200)
  body = models.TextField()
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  asked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  
  def __str__(self):
        return self.title
  
  
class Answer(models.Model):
  question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
  
  body = models.TextField()
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  
  def __str__(self):
        return f'Answer to "{self.question.title[:30]}..."'