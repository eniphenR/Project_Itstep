from django.contrib import admin


from .models import User, Tag, Comment, Blogs

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Blogs)