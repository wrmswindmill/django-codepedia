from django import forms
from .models import Project
from qa.models import Question


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'path', 'rel_path', 'github', 'ossean', 'language', 'tags']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']