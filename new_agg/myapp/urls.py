from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.articles_list, name='articles_list'),
    re_path(r'^feeds/new',views.new_feed,name='feed_new'),
    re_path(r'^feeds/',views.feeds_list,name='feeds_list'),
    
]
