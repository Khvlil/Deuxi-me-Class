from django.urls import path, re_path
from . import views


app_name = 'Lessons'

urlpatterns = [
    #------------------ Illustrator

    path('illustrator', views.illustrator, name='illustrator'),
    path('<str:pk>/illustrator', views.illustrator, name='illustrator'),

    #------------------ Photoshop

    path('photoshop', views.photoshop, name='photoshop'),
    path('<str:pk>/photoshop', views.photoshop, name='photoshop'),

    #------------------ Premier-pro

    path('premier-pro', views.premier_pro, name='premier-pro'),
    path('<str:pk>/premier-pro', views.premier_pro, name='premier-pro'),

    # ------------------ 3ds Max

    path('3ds-max', views.tds_max, name='3ds-max'),
    path('<str:pk>/3ds-max', views.tds_max, name='3ds-max'),

    # -------------- Code Categorie ---------------------------
    path('coding', views.code, name='coding'),
    path('<str:pk>/coding', views.code, name='coding'),

    path('algorithms', views.algo, name='algorithms'),
    path('<str:pk>/algorithms', views.algo, name='algorithms'),

    path('math-informatique', views.math, name='math-informatique'),
    path('<str:pk>/math-informatique', views.math, name='math-informatique'),


    # -------------- Language Categorie -----------------
    path('french', views.french, name='french'),
    path('<str:pk>/french', views.french, name='french'),

    path('english', views.english, name='english'),
    path('<str:pk>/english', views.english, name='english'),

]
