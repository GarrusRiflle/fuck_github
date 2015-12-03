# -*- coding: utf-8 -*-
from django import forms
from author.models import User

class UserCreationForm(forms.Form):
    username    = forms.CharField(label='username', max_length=50,
                                  widget=forms.TextInput(attrs={'placeholder': u'Имя нового пользователя',
                                                                'class': 'form-control'}))
    email       = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': u'Электропочта',
                                                                 'class': 'form-control'}))
    password    = forms.CharField(label='password', max_length=16,
                                  widget=forms.PasswordInput(attrs={'placeholder': u'Пароль',
                                                                'class': 'form-control'}))
    password1   = forms.CharField(label='password1', max_length=50,
                                  widget=forms.PasswordInput(attrs={'placeholder': u'Повторите пароль',
                                                                'class': 'form-control'}))
    #avatar      = forms.ImageField()

    # Проверка username
    def clean_username(self):
        try:
            user = self.cleaned_data['username']
            User.objects.get(username = user)
        except User.DoesNotExist:
            return user
        raise forms.ValidationError('This username is already taken')

    # Проверка e-mail
    def clean_email(self):
        if "email" in self:
            return self.normalize_email(self['email'])
        else:
            raise forms.ValidationError('E-mail wasn`t found')

    # Проверка паролей
    def clean_password(self):
        if "password" in self and "password1" in self and self["password"] != self["password1"]:
            raise forms.ValidationError("Passwords must be same")
        else:
            return self['password']
