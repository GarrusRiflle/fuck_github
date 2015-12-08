from django.db import models
from taggit.managers import TaggableManager
from author.models import User


class QuestionQuerySet(models.QuerySet):
    def top_questions(self):
        return self.all().order_by('-rate')

    def new_questions(self):
        return self.all().order_by('-id')

    def tag_questions(self):
        return self.filter(tags__slug=self.kwargs.get('slug'))

    def usr_questions(self, id):
        return self.filter(author__id=id)

    def answer_set(self):
        return Comments.objects.get(question=self)

class Question(models.Model):
    class Meta:
        db_table = 'question'

    title = models.CharField(max_length=200)
    text = models.TextField()
    rate = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    tags = TaggableManager(verbose_name=u'Tags')

    objects = QuestionQuerySet.as_manager()


class Comments(models.Model):
    class Meta:
        db_table = 'comments'

    text = models.TextField()
    rate = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
