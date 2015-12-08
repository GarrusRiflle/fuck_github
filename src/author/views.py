# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, redirect
from django.template.loader import get_template
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.context_processors import csrf
from django.contrib import auth
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt

from author.models import User
from author.forms import UserCreationForm, UploadFileForm
from question.models import Question, Comments
from sidebar.views import include_user


def register(request):
    args = {}
    args.update(csrf(request))

    form = UserCreationForm()
    args['form'] = form

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return render_to_response('forms/login.html',
                                      context_instance=RequestContext(request, processors=[include_user]))

    args['errors'] = form.errors
    return render_to_response('forms/register.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            args['login_error'] = u'Пользователь не существует'
            return render_to_response('forms/login.html', args,
                                      context_instance=RequestContext(request, processors=[include_user]))

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        if user.check_password(password):
            auth.login(request, user)
            return HttpResponseRedirect('/new/')
        else:
            args['login_error'] = u'Пароль введен неправильно'
            return render_to_response('forms/login.html', args,
                                      context_instance=RequestContext(request, processors=[include_user]))
    else:
        return render_to_response('forms/login.html', args,
                                  context_instance=RequestContext(request, processors=[include_user]))


def logout(request):
    auth.logout(request)
    if '/profile/' in request.path:
        return redirect('/new/', context_instance=RequestContext(request, processors=[include_user]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def profile(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = auth.get_user(request)
    args['username'] = user.username
    args['rating'] = user.rating
    args['questions_size'] = Question.objects.filter(author__id=user.pk).count()
    args['answers_size'] = Comments.objects.filter(author__id=user.pk).count()
    return render_to_response('user/user_profile.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))


def answers(request):
    args = {}
    user = auth.get_user(request)
    args['comments'] = Comments.objects.filter(author=user).order_by('-id')
    args['username'] = auth.get_user(request).username
    return render_to_response('user/user_answers.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))


def settings(request):
    args = {}
    args.update(csrf(request))
    user = auth.get_user(request)
    args['username'] = user.username
    args['email'] = user.email or ''
    args['form'] = UploadFileForm()

    if 'change-password' in request.POST:
        old_password = request.POST.get('old_password', '')
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        if user.check_password(old_password):
            args['password_error'] = u'Старый пароль введен неправильно'
            return render_to_response('user/user_settings.html', args,
                                      context_instance=RequestContext(request, processors=[include_user]))
        if password and password1 and password != password1:
            args['password_error'] = u'Пароли должны совпадать'
            return render_to_response('user/user_settings.html', args,
                                      context_instance=RequestContext(request, processors=[include_user]))
        else:
            u = User.objects.get(username__exact=user.username)
            u.set_password(password)
            u.save()
            args['password_success'] = u'Пароль был изменен'
    if 'change-email' in request.POST:
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError as e:
            args['email_error'] = u'Адрес введен неправильно'
        else:
            u = User.objects.get(username__exact=user.username)
            u.email = email
            u.save()
            args['email_success'] = u'Адрес был изменен'
        return render_to_response('user/user_settings.html', args,
                                  context_instance=RequestContext(request, processors=[include_user]))
    if 'change-photo' in request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=user.username)
            u.avatar = form.cleaned_data['image']
            u.save()
            return redirect('/'+user.username+'/', args,
                            context_instance=RequestContext(request, processors=[include_user]))
        else:
            args['photo_error'] = u'Файл не был загружен'

    return render_to_response('user/user_settings.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))