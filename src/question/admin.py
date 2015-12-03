from django.contrib import admin
from question.models import Question, Comments

admin.site.register(Question)
admin.site.register(Comments)