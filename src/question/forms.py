# -*- coding: utf-8 -*-
from django import forms

from haystack.forms import SearchForm
from models import Comments, Question
from taggit.forms import TagWidget


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'style': 'height: 150px'}),
        }


class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': u'Вопрос', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'placeholder': u'Теги к вопросу', 'class': 'form-control'}),
        }

class NotesSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()