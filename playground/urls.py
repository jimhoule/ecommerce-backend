from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('cache/', views.cache),
    path('hello/', views.say_hello),
    path('logging/', views.logging),
    path('mail/', views.send_email),
    path('notify/', views.notify),
]
