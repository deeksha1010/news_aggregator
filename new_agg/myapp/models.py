import requests
import feedparser
from django.db import models
from django.utils.dateparse import parse_datetime

class Feed(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @staticmethod
    def update_feed_from_url(feed_id):
        try:
            feed = Feed.objects.get(id=feed_id)
            response = requests.get(feed.url)
            
            if response.status_code == 200:
                feed_data = feedparser.parse(response.content)
                
                # Debugging
                print("Feed data:", feed_data)
                print("Feed entries:", feed_data.entries)

                feed_title = feed_data.feed.get('title', None)
                if feed_title:
                    feed.title = feed_title
                    feed.save()
                    Feed.create_articles_from_feed(feed, feed_data)
                else:
                    print("Title element not found in the XML document.")
            else:
                print(f"Failed to retrieve XML document. HTTP status code: {response.status_code}")
        except Exception as e:
            print(f"Error updating feed: {e}")

    @staticmethod
    def create_articles_from_feed(feed, feed_data):
        print("Creating articles...")
        for entry in feed_data.entries:
            title = entry.get('title', 'No title')
            url = entry.get('link', 'No URL')
            description = entry.get('description', 'No description')
            publication_date = parse_datetime(entry.get('published', ''))

            print(f"Article - Title: {title}, URL: {url}, Description: {description}, Date: {publication_date}")

        Article.objects.create(
            feed=feed,
            title=title,
            url=url,
            description=description,
            publication_date=publication_date
        )


class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    publication_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
