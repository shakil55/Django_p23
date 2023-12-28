from django.urls import path,include
from . import views
from .views import UpdatePostView 
from .views import *
from allauth.account.views import SignupView
from django.urls import re_path

urlpatterns = [
#     blogs
    path("", views.blogs, name="blogs"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", views.edit_blog_post, name="edit_blog_post"),
    path("delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    path('category/<int:category_id>/', views.categories, name='categories'),
    path("approve_comment/<int:comment_id>/", views.approve_comment, name="approve_comment"),


    
    
#     profile
    path("profile/", views.Profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    
#    user authentication
    # path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("search/", views.search, name="search"),
    
    path('accounts/sign_up/', views.my_registration_view, name='account_signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path("accounts/profile/", views.Profile, name="profile"),
    
    # Corrected activation URL pattern
    # re_path(
    #     r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #     activate,
    #     name='activate'
    # ),
]