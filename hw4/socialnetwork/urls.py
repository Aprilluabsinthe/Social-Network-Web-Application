from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.globalstream_action, name='home'),
    path('globalstream', views.globalstream_action, name='globalstream'),
    path('followerstream', views.followerstream_action, name='followerstream'),
    path('logout', views.logout_action, name='logout'),
    path('profile', views.profile_action, name='profile'),
    path('delete/<int:id>', views.delete_action, name='delete'),
    path('edit/<int:id>', views.edit_action, name='edit'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
]

