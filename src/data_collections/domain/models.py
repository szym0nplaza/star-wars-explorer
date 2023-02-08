from django.db import models
from datetime import datetime


# Django is highly coupled with db by default
# so it's hard to separate domain and ORM layer like in SQLAlchemy
# For future suitable solution can be found here: https://www.cosmicpython.com/book/appendix_django.html


class Collection(models.Model):
    filename = models.CharField(max_length=255)
    edited = models.DateTimeField(auto_now_add=True)
    chunks = models.IntegerField(default=1)

    def update_record(self):
        self.chunks += 1
        self.edited = datetime.now()
        self.save()
        return self.chunks
    

class Planets(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    verbose_name = models.CharField(max_length=255)