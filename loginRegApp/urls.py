from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login/',views.login),
    path('success/', views.success),
    path('signup/', views.signup),
    path('register/', views.register),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('process_message', views.post_mess),
    path('add_comment/<int:id>', views.post_comment),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('edit/<int:id>', views.edit),
    path('addNote/', views.createNote),
    
]