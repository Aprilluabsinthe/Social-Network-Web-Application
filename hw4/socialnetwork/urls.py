from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.globalstream_action, name='home'),
    path('globalstream', views.globalstream_action, name='globalstream'),
    path('followerstream', views.followerstream_action, name='followerstream'),
    path('profile', views.profile_action, name='profile'),
    path('profile_others', views.profile_others, name='profile_others'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
]

