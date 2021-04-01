
from django.urls import path
from . import views

urlpatterns = [
    path('users/show/<int:id>',views.wallIndex,name="the_wall"),
    path('users/show/post_message', views.postMessage,name="post_message"),
    path('users/show/post_comment', views.postComment,name="post_comment"),
    path('users/show/delete_message',views.delMessage,name="delete_message"),
    path('users/show/delete_comment',views.delComment,name="delete_comment"),
    path('users/show/get_created_at',views.getMsgComCreatedAt),
]