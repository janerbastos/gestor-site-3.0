from django.urls import path
from a_Account.views import (
    login, forgot_password, resetpassword_validate,
    reset_password, create_user, edit_user, delete_user,
    list_users
)

app_name = 'account'
handler403 = 'a_Acl.views.permission_view.access_denied'

urlpatterns = [
    path('login/', login, name='login'),
    path('create-user/', create_user, name='create-user'),
    path('users/', list_users, name='list-users'),
    path('edit-user/<int:uid>/edit/', edit_user, name='edit-user'),
    path('delete-user/<int:uid>/delete/', delete_user, name='delete-user'),
    path('forgout-password/', forgot_password, name='forgout-password'),
    path("resetpassword-validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword-validate",),
    path("reset-password/", reset_password, name="reset-password"),
]