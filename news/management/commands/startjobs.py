# Standard Library
import logging
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from news.models import Post

logger = logging.getLogger(__name__)


def save_new_posts(feed):
    """Saves new episodes to the database.
    Checks the episode GUID agaist the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.
    Args:
        feed: requires a feedparser object
    """
    post_title = feed.channel.title
    # post_image = feed.channel.image["href"]

    for item in feed.entries:

        if not Post.objects.filter(guid=item.guid).exists():
            post = Post(
                title=item.title,
                # description=item.description,
                # pub_date=parser.parse(item.published),
                link=item.link,
                # image=post_image,
                media_house_name=post_title,
                guid=item.guid,
            )
            post.save()


def fetch_cnn():
    """Fetches new episodes from RSS for the Real Python Podcast."""
    feeds = [
'http://rss.cnn.com/rss/edition_africa.rss']

    for _feed in feeds:
        item = feedparser.parse(_feed)
        save_new_posts(item)


def fetch_npr():
    """Fetches new episodes from RSS for the Real Python Podcast."""
    feeds = [
'https://feeds.npr.org/1002/rss.xml', 'https://feeds.npr.org/1001/rss.xml', 'https://feeds.npr.org/1039/rss.xml', 'https://feeds.npr.org/1032/rss.xml']

    for _feed in feeds:
        item = feedparser.parse(_feed)
        save_new_posts(item)




def fetch_cnbc():
    """Fetches new episodes from RSS for the Real Python Podcast."""
    _feed = feedparser.parse("https://www.cnbc.com/id/15837362/device/rss/rss.html")
    save_new_posts(_feed)

def fetch_msnbc():
    """Fetches new episodes from RSS for the Real Python Podcast."""
    _feed = feedparser.parse("https://www.msnbc.com/feed")
    save_new_posts(_feed)


def fetch_fox():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("http://feeds.foxnews.com/foxnews/latest")
    save_new_posts(_feed)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_cnn,
            trigger="interval",
            minutes=1,
            id="cnn",  # Each job MUST have a unique ID
            max_instances=1,
            # Replaces existing and stops duplicates on restart of the app.
            replace_existing=True,
        )
        logger.info("Added job: cnn")

        scheduler.add_job(
            fetch_cnbc,
            trigger="interval",
            minutes=1,
            id="cnbc",  # Each job MUST have a unique ID
            max_instances=1,
            # Replaces existing and stops duplicates on restart of the app.
            replace_existing=True,
        )
        logger.info("Added job: cnbc")

        scheduler.add_job(
            fetch_msnbc,
            trigger="interval",
            minutes=1,
            id="msnbc",  # Each job MUST have a unique ID
            max_instances=1,
            # Replaces existing and stops duplicates on restart of the app.
            replace_existing=True,
        )
        logger.info("Added job: msnbc")

        scheduler.add_job(
            fetch_npr,
            trigger="interval",
            minutes=1,
            id="npr",  # Each job MUST have a unique ID
            max_instances=1,
            # Replaces existing and stops duplicates on restart of the app.
            replace_existing=True,
        )
        logger.info("Added job: npr")


        scheduler.add_job(
            fetch_fox,
            trigger="interval",
            minutes=1,
            id="fox",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: fox")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
