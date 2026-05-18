"""Footbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import home, create_e, delete_event, buy_ticket, event_calendar_json

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_e, name="create_e"),
    path("delete/<int:event_id>/", delete_event, name="delete_event"),
    path("buy/<int:event_id>/", buy_ticket, name="buy_ticket"),
    path("api/calendar-events/", event_calendar_json, name="calendar_json"),
]
