
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.gotoDashboard,name='dashboard'),
    path('dashboard/admin', views.gotoDashboard, name='dashboard_admin'),
    path('users/edit',views.editUser, name='user_edit'),
    path('users/edit/<int:user_id>',views.editUserByAdmin, name="admin_user_edit"),
    path('users/edit/update',views.updateUser, name="update_data"), #tipo: password, datagral, descrip
    path('users/remove/<int:user_id>',views.removeUserByAdmin, name='admin_user_remove'),
    path('users/new',views.newUser, name="user_new"),
]