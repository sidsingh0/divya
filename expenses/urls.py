from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('history/', views.history, name="history"),
    path('balance/', views.balance, name="balance"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('statistics/', views.statistics, name="statistics"),
]
