from django.urls import path     
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.create_user),
    path('login',views.log_in),
    path('logoff',views.log_out),

    path('dashboard',views.dashboard),
    path('dashboard/posts/create',views.post_message),
    path('dashboard/posts/<int:id>',views.this_post),
    path('dashboard/posts/<int:id>/like',views.like_post_from_dashboard),
    path('dashboard/posts/<int:id>/unlike',views.unlike_post),
    path('dashboard/posts/<int:id>/edit',views.edit_post),
    path('dashboard/posts/<int:id>/destroy',views.delete_message),
    path('dashboard/posts/<int:id>/comment/new',views.post_comment),
    path('dashboard/posts/<int:id>/comment/destroy',views.delete_comment),
    path('dashboard/user/profile/<int:id>',views.profile),
    path('dashboard/user/profile/<int:id>/edit',views.edit_profile),
    path('dashboard/user/profile/<int:id>/destroy',views.delete_account),
    path('dashboard/user/profile/<int:id>/update',views.update_profile),
]

