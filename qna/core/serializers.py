from rest_framework import serializers

from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
  answered_by = serializers.StringRelatedField(read_only=True)
  
  class Meta:
    model = Answer
    fields = ['question', 'body', 'created_at', 'answered_by']


class QuestionSerializer(serializers.ModelSerializer):
  asked_by = serializers.StringRelatedField(read_only=True)
  answers = AnswerSerializer(many=True, read_only=True)
  
  class Meta:
    model = Question
    fields = ['id', 'title', 'body', 'created_at', 'asked_by', 'answers']
    
