from django.shortcuts import render_to_response, render, redirect
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.contrib import auth
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt

from taggit.models import Tag

from question.models import Question, Comments
from question.forms import CommentForm, QuestionAddForm

class NewQuestionsListView(ListView):
	model = Question
	template_name = 'new_questions.html'
	context_object_name = 'questions'
	paginate_by = 10

	def get_queryset(self):
		return Question.objects.all().order_by('-id')

class TopQuestionsListView(ListView):
	model = Question
	template_name = 'top_questions.html'
	context_object_name = 'questions'
	paginate_by = 10

	def get_queryset(self):
		return Question.objects.all().order_by('-rate')

class TagQuestionsListView(ListView):
    model = Question
    template_name = 'tag_questions.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('slug'))

def new_questions(request):
    querySet = Question.objects.new_questions()
    return render_to_response('new_questions.html', {'questions': querySet, 'username': auth.get_user(request).username})

def top_questions(request):
    querySet = Question.objects.top_questions()
    return render_to_response('top_questions.html', {'questions': querySet, 'username': auth.get_user(request).username})

def tag_questions(request, tag):
    querySet = Question.objects.tag_questions(tag)
    return render_to_response('tag_questions.html', {'questions': querySet,
                                                     'username': auth.get_user(request).username,
                                                     'tag': tag})

def question(request, question_id=1):
	comment_form = CommentForm
	args = {}
	args.update(csrf(request))
	args['question'] = Question.objects.get(id=question_id)
	args['comments'] = Comments.objects.filter(question=question_id)
	args['form'] 	 = comment_form
	args['username'] = auth.get_user(request).username
	return render_to_response('question_page.html', args)

def addrate(request, question_id):
	try:
		question = Question.objects.get(id=question_id)
		question.rate += 1
		question.save()
	except ObjectDoesNotExist:
		raise Http404
	return HttpResponseRedirect("/new/")

def cutrate(request, question_id):
	try:
		question = Question.objects.get(id=question_id)
		question.rate -= 1
		question.save()
	except ObjectDoesNotExist:
		raise Http404
	return HttpResponseRedirect("/new/")

def addcomment(request, question_id):
    if request.POST:
        comment_text = request.POST.get('comment')
        comment = Comments.objects.create(text = comment_text)
        comment.question_id = question_id

        question = Question.objects.get(id = question_id)
        question.num_comments += 1;

        question.save()
        comment.save()

    return redirect('/question/%s/' % question_id)

@csrf_exempt
def addquestion(request):
    form = QuestionAddForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        question = Question(
            title = form.cleaned_data['title'],
            text = form.cleaned_data['text'],
            tags = form.cleaned_data['tags'],
        )

        question.author_id = request.user.id
        question.save()
        return redirect('/question/%s/' % question.id)

    return render_to_response('forms/add_question.html', {'form': QuestionAddForm})

