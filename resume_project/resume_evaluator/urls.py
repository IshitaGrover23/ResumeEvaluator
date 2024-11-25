from django.urls import path
from .views import ResumeEvaluationView, EvaluationListView, EvaluationDetailView

urlpatterns = [
    path('', ResumeEvaluationView.as_view(), name='evaluation-create'),
    path('evaluations/', EvaluationListView.as_view(), name='evaluation-list'),
    path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation-detail'),
]