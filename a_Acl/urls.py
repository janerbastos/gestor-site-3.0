from django.urls import path
from a_Acl.views import (
    create_role, delete_role, edit_role, list_roles,
    manage_role_permissions, manage_site_user, list_users,
    manage_user_roles, remove_user_site)

app_name = 'acl'

urlpatterns = [

    path('create-role/', create_role, name='create-role'),
    path('roles/', list_roles, name='list-roles'),
    path('role/<int:rid>/permissions/', manage_role_permissions, name='manage-role-permissions'),
    path('edit-role/<int:rid>/edit/', edit_role, name='edit-role'),
    path('delete-role/<int:rid>/delete/', delete_role, name='delete-role'),
    path('autorizar-usuario/<path:url>/user/', manage_site_user, name='manage-site-user'),
    path('autorizar-usuario/<path:url>/permissoes/', list_users, name='list-users'),
    path('equipe/<path:url>/member/<int:member_id>/roles/', manage_user_roles, name='manage-user-roles'),
    path('retirar-equipe/<path:url>/<int:oid>/roles', remove_user_site, name='remove-user-site')
]