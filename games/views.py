
from django.shortcuts import render, get_object_or_404
from .models import Game, Article


def home(request):
    games = Game.objects.filter(is_visible=True)
    return render(request, 'games/home.html', {'games': games})


def mahjong(request):
    return render(request, 'games/mahjong.html')


def football(request):
    return render(request, 'games/football.html')


def basketball(request):
    return render(request, 'games/basketball.html')


def tictactoe(request):
    return render(request, 'games/tictactoe.html')


def simpsons(request):
    return render(request, 'games/simpsons.html')


def chess(request):
    return render(request, 'games/chess.html')


def breakout(request):
    return render(request, 'games/breakout.html')


def prison_pacman(request):
    return render(request, 'games/prison_pacman.html')


def prison_pacman2(request):
    return render(request, 'games/prison_pacman2.html')


def paint(request):
    return render(request, 'games/paint.html')


def city_simulator(request):
    return render(request, 'games/city_simulator.html')


def christmas_tower(request):
    return render(request, 'games/christmas_tower.html')


def santa_delivery(request):
    return render(request, 'games/santa_delivery.html')


def match3(request):
    return render(request, 'games/match3.html')


def chernobyl_fishing(request):
    return render(request, 'games/chernobyl_fishing.html')


def christmas_circuit(request):
    return render(request, 'games/christmas_circuit.html')

def articles(request):
    articles_list = Article.objects.filter(is_published=True)
    return render(request, 'games/articles.html', {
        'articles': articles_list
    })


def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )
    return render(request, 'games/article_detail.html', {
        'article': article
    })
