import random

from django.core.management.base import BaseCommand

from author.models import User
from question.models import Question
from sidebar.models import TopUsers, TopTags


class Command(BaseCommand):
    help = 'Updates ratings for sidebar'

    def handle(self, *args, **options):

        TopUsers.objects.all().delete()
        TopTags.objects.all().delete()

        users = User.objects.order_by('-rating')[:10]
        for user in users:
            u = TopUsers()
            u.username = user.username
            u.rating = user.rating
            u.save()

        tags = Question.tags.most_common()[:15]
        for tag in tags:
            t = TopTags()
            t.tag = tag.name
            t.slug = tag.slug
            t.size = random.randint(16,30)
            t.save()

        self.stdout.write('Successfully updated ratings')
