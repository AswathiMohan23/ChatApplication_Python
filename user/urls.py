from django.urls import path
from .import views
urlpatterns=[
    path('register',views.UserRegistration.as_view()),
    path('login',views.UserLogin.as_view()),
    # path('userLogin', views.login_user),

]