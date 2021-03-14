from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.home_action, name='home'),
    path('globalstream', views.home_action, name='globalstream'),
    path('followerstream', views.followerstream_action, name='followerstream'),
    path('profile/<int:userid>', views.get_profile, name='profile'),
    path('profile_others', views.profile_others, name='profile_others'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('makepost', views.makepost, name='makepost'),
    path('makecomment', views.makecomment, name='makecomment'),
    path('delete-post/<int:post_id>', views.delete_action_post, name='delete-post'),
    path('delete-comment/<int:id>', views.delete_action_comment, name='delete-comment'),
    path('add-profile', views.add_profile, name='add-profile'),
    path('delete-profile/<int:id>', views.delete_profile, name='delete-profile'),
    path('edit-profile/<int:id>', views.edit_profile, name='edit-profile'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('get-profile/<int:id>', views.get_profile, name='get-profile'),
    path('edit-profile/<int:id>', views.edit_profile, name='edit-profile'),
    path('personalinfo/<int:id>', views.get_bio, name='personalinfo'),
    path('changefollow/<int:id>', views.changefollow, name='changefollow'),
    path('get-friend/<int:id>', views.get_friend, name='get-friend'),
]
