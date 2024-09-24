from django.contrib import admin
from .models import Member
from website.models import Article
from .models import SubmissionCount
from .models import RegisteredEmail
from .models import User

admin.site.register(Member)
admin.site.register(Article)
admin.site.register(SubmissionCount)
admin.site.register(RegisteredEmail)
admin.site.register(User)

class SubmissionCountAdmin(admin.ModelAdmin):
    list_display = ('count', 'late_count', 'deadline')

#@admin.register(RegisteredEmail)
class RegisteredEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_registered')
    search_fields = ('email',)

