# -*- coding: utf-8 -*-
from django import forms
from author.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': u'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password1')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': u'Имя пользователя', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': u'Электропочта', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': u'Пароль', 'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']

        if password and password1 and password != password1:
            raise forms.ValidationError(u"Пароли должны совпадать")
        return self.cleaned_data

class UploadFileForm(forms.Form):
    image = forms.ImageField()