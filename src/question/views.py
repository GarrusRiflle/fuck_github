# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.serializers import json
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView

from author.models import User
from sidebar.views import include_user
from taggit.models import Tag
from question.models import Question, Comments
from question.forms import CommentAddForm, QuestionAddForm, NotesSearchForm


class NewQuestionsListView(ListView):
    model = Question
    template_name = 'new_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.all().order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(NewQuestionsListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class TopQuestionsListView(ListView):
    model = Question
    template_name = 'top_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.all().order_by('-rate')

    def get_context_data(self, *args, **kwargs):
        context = super(TopQuestionsListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class TagQuestionsListView(ListView):
    model = Question
    template_name = 'tag_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(TagQuestionsListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

class UserQuestionsListView(ListView):
    model = Question
    template_name = 'user/user_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.filter(author_id = self.request.user.id).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(UserQuestionsListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


def question(request, question_id):
    comment_form = CommentAddForm
    args = {}
    args.update(csrf(request))
    args['question'] = Question.objects.get(id=question_id)
    args['comments'] = Comments.objects.filter(question=question_id)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username

    return render_to_response('question_page.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))


def addrate(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.rate += 1
        question.save()
    except ObjectDoesNotExist:
        raise Http404
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cutrate(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.rate -= 1
        question.save()
    except ObjectDoesNotExist:
        raise Http404
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def addcomment(request, question_id):
    args = {}
    args.update(csrf(request))
    args['form'] = CommentAddForm()
    args['username'] = auth.get_user(request).username

    if request.method == "POST":
        form = CommentAddForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = User.objects.get(pk=request.user.id)
            comment.question = Question.objects.get(pk=question_id)
            comment.save()

            question = Question.objects.get(id=question_id)
            question.num_comments += 1
            question.save()

            author = User.objects.get(pk=request.user.id)
            author.rating += 1
            author.save()

    return redirect('/question/%s/' % question_id)


def addquestion(request):
    args = {}
    args.update(csrf(request))

    if request.user.is_authenticated():
        args['username'] = auth.get_user(request).username
    else:
        args['login_error'] = u'Прежде чем задать вопрос, нужно авторизоваться'
        return render_to_response('forms/login.html', args)
    args['form'] = QuestionAddForm()

    if request.method == "POST":
        form = QuestionAddForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author_id = request.user.id
            question.save()
            form.save_m2m()

            author = User.objects.get(pk=request.user.id)
            author.rating += 5
            author.save()

            return redirect('/question/%s/' % question.id, args)

    return render_to_response('forms/add_question.html', args,
                              context_instance=RequestContext(request, processors=[include_user]))


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        question = get_object_or_404(Question, id=id)

        question.rate += 1
        question.save()
        message = 'You liked this'

    ctx = {'rate': question.rate, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')