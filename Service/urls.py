from django.urls import path, re_path
from . import views


app_name = 'Service'


urlpatterns = [
    path('', views.landinpage, name='landingpage'),
    path('S2ale/', views.home, name='Home'),
    path('<str:pk>/', views.home, name='Home'),

    path('Terms', views.website_terms, name='Policy'),

    path('<str:pk>/Categorie/Design', views.design, name='Design'),
    path('Categorie/Design', views.design, name='Design'),

    path("<str:pk>/Categorie/Coding", views.code, name='Coding'),
    path('Categorie/Coding', views.code, name='Coding'),


    path('<str:pk>/Categorie/Language', views.language, name='Language'),
    path('Categorie/Language', views.language, name='Language'),
]
