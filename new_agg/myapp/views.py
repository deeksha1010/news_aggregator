from django.shortcuts import render, redirect
from .models import Article, Feed
from .forms import FeedForm
import datetime

def articles_list(request):
    articles = Article.objects.all()
    print("Rendering articles:", articles)
    return render(request, 'myapp/articles_list.html', {'articles': articles})

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'myapp/feeds_list.html', {'feeds': feeds})

def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            existing_feed = Feed.objects.filter(url=feed.url)
            if not existing_feed.exists():
                feed.save()
                Feed.update_feed_from_url(feed.id)
            return redirect('feeds_list')  # Redirect to feeds page after saving
    else:
        form = FeedForm()
    return render(request, 'myapp/new_feed.html', {'form': form})
