from django.contrib import admin
from .models import User, Asset,Comment,Like,Rating


admin.site.register([User, Asset,Comment,Like,Rating])

# Register your models here.
