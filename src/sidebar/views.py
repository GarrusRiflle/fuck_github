import random
from author.models import User
from question.models import Question
from sidebar.models import TopUsers, TopTags


def include_top_users(request):
    users = TopUsers.objects.all()
    return {'top_users': users}


def include_top_tags(request):
    tags = []
    for tag in TopTags.objects.all():
        tags.append({'tag': tag.tag, 'size': tag.size, 'slug': tag.slug})
    return {'top_tags': tags}

def include_user(request):
    return {'USER': request.user}