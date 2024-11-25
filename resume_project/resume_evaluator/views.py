from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from .models import ResumeEvaluation, EvaluationSuggestion
from .forms import ResumeEvaluationForm
from .utils import ResumeAnalyzer
from django.urls import reverse

class ResumeEvaluationView(CreateView):
    model = ResumeEvaluation
    form_class = ResumeEvaluationForm
    template_name = 'resume_evaluator/evaluation_form.html'
    
    def get_success_url(self):
        return reverse('evaluation-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        try:
            evaluation = form.save(commit=False)
            
            analyzer = ResumeAnalyzer()
            result = analyzer.analyze_resume(
                self.request.FILES['resume'],
                form.cleaned_data['job_description']
            )
            
            evaluation.jd_match = result['JD Match']
            evaluation.profile_summary = result['Profile Summary']
            evaluation.save()
            
            for suggestion in result['Suggestions']:
                EvaluationSuggestion.objects.create(
                    evaluation=evaluation,
                    suggestion=suggestion
                )
            
            messages.success(self.request, 'Resume evaluated successfully!')
            return super().form_valid(form)
            
        except Exception as e:
            messages.error(self.request, f'Error evaluating resume: {str(e)}')
            return super().form_invalid(form)

class EvaluationListView(ListView):
    model = ResumeEvaluation
    template_name = 'resume_evaluator/evaluation_list.html'
    context_object_name = 'evaluations'
    ordering = ['-created_at']

class EvaluationDetailView(DetailView):
    model = ResumeEvaluation
    template_name = 'resume_evaluator/evaluation_detail.html'
    context_object_name = 'evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.suggestions.all()
        return context