from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Testcase)
admin.site.register(Submission)
