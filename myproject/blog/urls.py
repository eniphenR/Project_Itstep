
from django.urls import path
from . import views
app_name = 'blog_page'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('blog-single',views.blog_single,name='blog-single'),

]