from django.urls import path
from .extra_views import (
    pixel_puzzle, pixel_adventure, pixel_documents, pixel_updates,
    pixel_snowrunner, pixel_railway, pixel_bus, pixel_workshop, pixel_bridge,
)

urlpatterns = [
    path('real-puzzle/', pixel_puzzle, name='pixel_puzzle'),
    path('adventure/', pixel_adventure, name='pixel_adventure'),
    path('documents/', pixel_documents, name='pixel_documents'),
    path('updates/', pixel_updates, name='pixel_updates'),
    path('snowrunner/', pixel_snowrunner, name='pixel_snowrunner'),
    path('railway/', pixel_railway, name='pixel_railway'),
    path('bus-simulator/', pixel_bus, name='pixel_bus'),
    path('workshop/', pixel_workshop, name='pixel_workshop'),
    path('bridge-builder/', pixel_bridge, name='pixel_bridge'),
]
