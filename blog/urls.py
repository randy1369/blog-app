from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from  django.contrib.auth import views as auth_views



app_name = 'blog'

urlpatterns = [

    
    path('',views.blog_list, name='blog_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('posts_by_tag/<int:tag_id>/', views.posts_by_tag, name='posts_by_tag'),
    path('subcategory/<int:subcategory_id>/', views.posts_for_subcategory, name='subcategory_posts'),
    path('cat&tags/', views.blog_cattags, name='cattags'),
    path('search/', views.search, name='search'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('create/', views.blog_create, name='blog_create'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug>/update/', views.blog_update, name='blog_update'),
    path('<slug>/delete/', views.blog_delete, name='blog_delete'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 