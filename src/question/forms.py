from django import forms
from models import Comments, Question
from taggit.forms import TagWidget

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ['text']

class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'tags': TagWidget(),
        }
