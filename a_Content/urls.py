from django.urls import path
from a_Content.views import (
    dashboard, 
    create_pagina, update_pagina, delete_pagina, workflow_pagina,
    create_pasta, update_pasta, delete_pasta, workflow_pasta,
    create_noticia, update_noticia, delete_noticia, workflow_noticia,
    imagem_manage_list, imagem_manage_upload, imagem_manage_set
)

app_name = 'content'

urlpatterns = [
    path('site/<slug:url>/catalogo/', dashboard, name='dashboard'),
    path('site/<slug:url>/catalogo/@@<path:path_url>/', dashboard, name='dashboard'),

    # Pagina
    path('site/<slug:url>/create-pagina/', create_pagina, name='create-atpagina'),
    path('site/<slug:url>/update-pagina/', update_pagina, name='update-atpagina'),
    path('site/<slug:url>/delete-pagina/', delete_pagina, name='delete-atpagina'),
    path('site/<slug:url>/workflow-pagina/', workflow_pagina, name='workflow-atpagina'),

    # Pasta
    path('site/<slug:url>/create-pasta/', create_pasta, name='create-atpasta'),
    path('site/<slug:url>/update-pasta/', update_pasta, name='update-atpasta'),
    path('site/<slug:url>/delete-pasta/', delete_pasta, name='delete-atpasta'),
    path('site/<slug:url>/workflow-pasta/', workflow_pasta, name='workflow-atpasta'),

    # Noticia
    path('site/<slug:url>/create-noticia/', create_noticia, name='create-atnoticia'),
    path('site/<slug:url>/update-noticia/', update_noticia, name='update-atnoticia'),
    path('site/<slug:url>/delete-noticia/', delete_noticia, name='delete-atnoticia'),
    path('site/<slug:url>/workflow-noticia/', workflow_noticia, name='workflow-atnoticia'),

    # Imagem Manager
    path('site/<slug:url>/imagem-manager-list/', imagem_manage_list, name='imagem-manage-list'),
    path('site/<slug:url>/imagem-manager-upload/', imagem_manage_upload, name='imagem-manage-upload'),
    path('site/<slug:url>/<int:oid>/imagem-manager-set/', imagem_manage_set, name='imagem-manage-set'),
]
