# podcasts/views.py

from django.views.generic import ListView

from .models import Post


class HomePageView(ListView):
    template_name = "news/homepage.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Post.objects.filter().order_by("-pub_date")[:5]
        context['foxnews']= Post.objects.filter(media_house_name='Fox News')[:5]
        context['cnnnews'] = Post.objects.filter(media_house_name='CNN.com - RSS Channel - Regions - Africa')[:5]
        context['cnbcnews'] = Post.objects.filter(media_house_name='U.S. News')[:5]
        context['msnbcnews'] = Post.objects.filter(media_house_name='MSNBC Top Stories')[:5]
        context['nprnews'] = Post.objects.filter(media_house_name__endswith='NPR')[:5]
        return context

