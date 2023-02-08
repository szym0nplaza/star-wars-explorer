from django.db import models


# Django is highly coupled with db by default
# so it's hard to separate domain and ORM layer like in SQLAlchemy
# For future suitable solution can be found here: https://www.cosmicpython.com/book/appendix_django.html


class Collection(models.Model):
    filename = models.CharField(max_length=255)
    edited = models.DateTimeField(auto_now_add=True)
    chunks = models.IntegerField(default=1)
