from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('signup',views.signup,name='signup'),
    path('signin',views.login,name='login'),
    path('verification',views.verification,name='verification'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('challenge',views.challenge,name='challenge'),
    path('challenges',views.allchallenges,name='challenges'),
    path('feed',views.feed,name='feed'),
    path('likes',views.likes,name='likes'),
    path('challenge/create',views.createchallenge,name='challengecreate'),
    path('posts',views.posts,name='posts'),
    path('posts-create',views.postscreate,name='postscreate'),
    path('settings',views.settings,name='settings'),
    path('profile-edit',views.profileedit,name='profileedit'),
    path('teachers',views.teachers,name='teacher'),
    path('teachers/add',views.teachersadd,name='teacheradd'),
    path('classes',views.Classes,name='classes'),
    path('classes/add',views.Classesadd,name='classesadd'),
    path('students',views.students,name='students'),
    path('users-add',views.usersadd,name='usersadd'),
    path('students/add',views.studentsadd,name='studentsadd'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='index.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),
            
]
