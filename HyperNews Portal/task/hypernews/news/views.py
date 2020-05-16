from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import json
import datetime
import random


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news_json = json.load(news_file)
        news_context = {}
        for news in news_json:
            if news['link'] == int(news_id):
                news_context = news
                break
        return render(request, 'news.html', context={'news': news_context})


class MainNewsView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news_json = json.load(news_file)
        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            news_json = [news for news in news_json if query.lower() in news['title'].lower()]
        for news in news_json:
            news['created'] = news['created'][:10]
        return render(request, 'news_main.html', context={'news': news_json})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def post(self, request, *args, **kwargs):
        new_news = {}
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news_json = json.load(news_file)
        link_list = [news['link'] for news in news_json]
        new_news['title'] = request.POST.get('title')
        new_news['text'] = request.POST.get('text')
        new_news['created'] = datetime.datetime.now().isoformat(' ', timespec='seconds')
        link = random.randint(1, 1000000000)
        while link in link_list:
            link = random.randint(1, 1000000000)
        new_news['link'] = link
        news_json.append(new_news)
        with open(settings.NEWS_JSON_PATH, 'w') as news_file:
            json.dump(news_json, news_file)
        return redirect('/news/')
