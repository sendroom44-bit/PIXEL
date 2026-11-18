from django.urls import path
from .extra_views import pixel_puzzle, pixel_adventure, pixel_documents, pixel_updates

urlpatterns = [
    path('real-puzzle/', pixel_puzzle, name='pixel_puzzle'),
    path('adventure/', pixel_adventure, name='pixel_adventure'),
    path('documents/', pixel_documents, name='pixel_documents'),
    path('updates/', pixel_updates, name='pixel_updates'),
]
