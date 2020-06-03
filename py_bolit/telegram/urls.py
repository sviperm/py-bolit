from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BotView

urlpatterns = [
    path('', csrf_exempt(BotView.as_view())),
]
