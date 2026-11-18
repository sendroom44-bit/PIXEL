from django.shortcuts import render

def pixel_puzzle(request):
    return render(request, 'games/pixel_puzzle.html')

def pixel_adventure(request):
    return render(request, 'games/pixel_adventure.html')

def pixel_documents(request):
    return render(request, 'games/pixel_documents.html')

def pixel_updates(request):
    return render(request, 'games/pixel_updates.html')

def pixel_snowrunner(request):
    return render(request, 'games/transport_games.html', {'game_mode': 'snow', 'title': 'PIXEL SnowRunner', 'subtitle': 'БЕЗДОРОЖЬЕ И ДОСТАВКА', 'intro': 'Провези груз через сложную трассу, управляй скоростью и выбирай траекторию.'})

def pixel_railway(request):
    return render(request, 'games/transport_games.html', {'game_mode': 'railway', 'title': 'PIXEL Railway', 'subtitle': 'ЖЕЛЕЗНАЯ ДОРОГА', 'intro': 'Веди поезд по маршруту, регулируй тягу и обслуживай станции.'})

def pixel_bus(request):
    return render(request, 'games/transport_games.html', {'game_mode': 'bus', 'title': 'PIXEL Bus Simulator', 'subtitle': 'ГОРОДСКОЙ МАРШРУТ', 'intro': 'Управляй автобусом, собирай пассажиров на остановках и выполняй рейсы.'})

def pixel_workshop(request):
    return render(request, 'games/transport_games.html', {'game_mode': 'workshop', 'title': 'PIXEL Автомастерская', 'subtitle': 'РЕМОНТ И ПОКРАСКА', 'intro': 'Собери автомобиль из деталей, выбери цвет и выполни заказ.'})

def pixel_bridge(request):
    return render(request, 'games/transport_games.html', {'game_mode': 'bridge', 'title': 'PIXEL Bridge Builder', 'subtitle': 'ИНЖЕНЕРНАЯ МАСТЕРСКАЯ', 'intro': 'Построй мост между берегами и проверь, выдержит ли он грузовик.'})
