from rest_framework.routers import DefaultRouter
from .views import AnswerViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = router.urls