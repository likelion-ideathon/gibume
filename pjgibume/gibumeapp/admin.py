from django.contrib import admin

from .models import Perfume
from .models import Comment
from .models import User

admin.site.register(Perfume)
admin.site.register(Comment)
admin.site.register(User)

