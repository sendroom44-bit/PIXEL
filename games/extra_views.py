from django.shortcuts import render

def pixel_puzzle(request):
    return render(request, 'games/pixel_puzzle.html')

def pixel_adventure(request):
    return render(request, 'games/pixel_adventure.html')

def pixel_documents(request):
    return render(request, 'games/pixel_documents.html')

def pixel_updates(request):
    return render(request, 'games/pixel_updates.html')
