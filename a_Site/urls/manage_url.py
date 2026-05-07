from django.urls import path
from a_Site.views import (
    dashboard, create_site, edit_site,
    delete_site, open_site, edit_site_midia,
    edit_site_redesocial_link, edit_site_codigo_script,
    edit_site_contenttype, edit_site_endereco, list_tag,
    create_tag, edit_tag, delete_tag)

app_name = 'site'

urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
    path('create-site/', create_site, name='create-site'),
    path('open-site/<slug:url>/open/', open_site, name='open-site'),
    path('edit-site/<slug:url>/edit/', edit_site, name='edit-site'),
    path('delete-site/<slug:url>/delete/', delete_site, name='delete-site'),

    # configurações
    path('edit-site-midia/<slug:url>/midia/', edit_site_midia, name='edit-site-midia'),
    path('edit-site-redesocial/<slug:url>/links/', edit_site_redesocial_link, name='edit-site-redesocial-link'),
    path('edit-site/<slug:url>/codigo-script/', edit_site_codigo_script, name='edit-site-codigo-script'),
    path('edit-site/<slug:url>/content-type/', edit_site_contenttype, name='edit-site-content-type'),
    path('edit-site/<slug:url>/endereco/', edit_site_endereco, name='edit-site-endereco'),

    # tags
    path('site/<slug:url>/tags/', list_tag, name='list-tag'),
    path('site/<slug:url>/tag/create/', create_tag, name='create-tag'),
    path('site/<slug:url>/<slug:slug>/edit-tag/', edit_tag, name='edit-tag'),
    path('site/<slug:url>/<slug:slug>/delete-tag/', delete_tag, name='delete-tag'),

]