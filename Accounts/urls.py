from django.urls import path, re_path
from . import views


app_name = 'Accounts'


urlpatterns = [
    re_path(r'^Login/$', views.sign_in, name='Login'),
    path('Register', views.register, name='Register'),
    path('Logout', views.logout, name='Logout'),

    path('Vote', views.vote, name='Vote'),
    path('<str:pk>/Vote', views.vote, name='Vote'),
    path('Subscription expired', views.susbscribePagePlan,
         name='subscription-expired'),
    path('test', views.test, name='Test')
]
