from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Movie)
admin.site.register(User)
admin.site.register(MovieUserScore)
admin.site.register(MovieUserComment)

