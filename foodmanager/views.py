from django.shortcuts import render
from django.http import HttpResponse

import bot

# Create your views here.
def start_bot(request):
    bot.main()
    return HttpResponse("Бот запущен")