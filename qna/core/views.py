from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
  queryset = Question.objects.all() 
  serializer_class = QuestionSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]
  
  def perform_create(self, serializer):
    serializer.save(asked_by=self.request.user)

  
class AnswerViewSet(viewsets.ModelViewSet):
  queryset = Answer.objects.all()
  serializer_class = AnswerSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]
  
  def perform_create(self, serializer):
        serializer.save(answered_by=self.request.user)