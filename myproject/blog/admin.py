from django.contrib import admin


from .models import User, Tag, Comment, Blogs, Category

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Blogs)
admin.site.register(Category)