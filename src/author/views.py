# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, redirect
from django.template.loader import get_template
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.contrib import auth
from author.models import User
#from author.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

def register(request):
    args = {}
    args.update(csrf(request))
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            email    = form.clean_email()
            password = form.cleaned_password()

            User.objects.create_user(username, password, email)
            return HttpResponseRedirect('/auth/login/')
    else:
	    return render(request, 'forms/register.html', {'form': form})

def login(request):
	args={}	
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/new/')
		else:
			args['login_error'] = "Пользователь не найден"	
			return render_to_response('forms/login.html', args)
	else:
		return render_to_response('forms/login.html', args)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
