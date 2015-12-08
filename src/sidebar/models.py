from django.db import models


class TopUsers(models.Model):
    class Meta:
        db_table = 'top_users'

    username = models.CharField(max_length=30, null=True)
    rating = models.IntegerField(default=0)

class TopTags(models.Model):
    class Meta:
        db_table = 'top_tags'

    tag = models.CharField(max_length=30, null=True)
    slug = models.SlugField(null=True)
    size = models.IntegerField(default=20)
