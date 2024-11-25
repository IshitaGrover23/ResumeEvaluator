from django.db import models
from django.core.validators import FileExtensionValidator

class ResumeEvaluation(models.Model):
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    job_description = models.TextField()
    jd_match = models.CharField(max_length=10)
    profile_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation {self.id} - Match: {self.jd_match}"

class EvaluationSuggestion(models.Model):
    evaluation = models.ForeignKey(ResumeEvaluation, on_delete=models.CASCADE, related_name='suggestions')
    suggestion = models.TextField()

    def __str__(self):
        return f"Suggestion for evaluation {self.evaluation.id}"