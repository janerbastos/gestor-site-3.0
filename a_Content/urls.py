from django.urls import path
from a_Content.views import (
    dashboard, 
    imagem_manage_list, imagem_manage_upload, imagem_manage_set,
    doc_manage_list, doc_manage_upload, doc_manage_set,
    create_pagina, update_pagina, delete_pagina, workflow_pagina,
    create_pasta, update_pasta, delete_pasta, workflow_pasta,
    create_noticia, update_noticia, delete_noticia, workflow_noticia,
    create_informe, update_informe, delete_informe, workflow_informe,
    create_evento, update_evento, delete_evento, workflow_evento,
    create_agenda, update_agenda, delete_agenda, workflow_agenda,
    create_servico, update_servico, delete_servico, workflow_servico,
    create_link, update_link, delete_link, workflow_link,
    create_banner, update_banner, delete_banner, workflow_banner,
    create_arquivo, update_arquivo, delete_arquivo, workflow_arquivo,
    create_viewer, update_viewer, delete_viewer, workflow_viewer,
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

    # Informe
    path('site/<slug:url>/create-informe/', create_informe, name='create-atinforme'),
    path('site/<slug:url>/update-informe/', update_informe, name='update-atinforme'),
    path('site/<slug:url>/delete-informe/', delete_informe, name='delete-atinforme'),
    path('site/<slug:url>/workflow-informe/', workflow_informe, name='workflow-atinforme'),

    # Evento
    path('site/<slug:url>/create-evento/', create_evento, name='create-atevento'),
    path('site/<slug:url>/update-evento/', update_evento, name='update-atevento'),
    path('site/<slug:url>/delete-evento/', delete_evento, name='delete-atevento'),
    path('site/<slug:url>/workflow-evento/', workflow_evento, name='workflow-atevento'),

    # Agenda
    path('site/<slug:url>/create-agenda/', create_agenda, name='create-atagenda'),
    path('site/<slug:url>/update-agenda/', update_agenda, name='update-atagenda'),
    path('site/<slug:url>/delete-agenda/', delete_agenda, name='delete-atagenda'),
    path('site/<slug:url>/workflow-agenda/', workflow_agenda, name='workflow-atagenda'),

    # Servico
    path('site/<slug:url>/create-servico/', create_servico, name='create-atservico'),
    path('site/<slug:url>/update-servico/', update_servico, name='update-atservico'),
    path('site/<slug:url>/delete-servico/', delete_servico, name='delete-atservico'),
    path('site/<slug:url>/workflow-servico/', workflow_servico, name='workflow-atservico'),

    # Link
    path('site/<slug:url>/create-link/', create_link, name='create-atlink'),
    path('site/<slug:url>/update-link/', update_link, name='update-atlink'),
    path('site/<slug:url>/delete-link/', delete_link, name='delete-atlink'),
    path('site/<slug:url>/workflow-link/', workflow_link, name='workflow-atlink'),

    # Banner
    path('site/<slug:url>/create-banner/', create_banner, name='create-atbanner'),
    path('site/<slug:url>/update-banner/', update_banner, name='update-atbanner'),
    path('site/<slug:url>/delete-banner/', delete_banner, name='delete-atbanner'),
    path('site/<slug:url>/workflow-banner/', workflow_banner, name='workflow-atbanner'),

    # Arquivo
    path('site/<slug:url>/create-arquivo/', create_arquivo, name='create-atarquivo'),
    path('site/<slug:url>/update-arquivo/', update_arquivo, name='update-atarquivo'),
    path('site/<slug:url>/delete-arquivo/', delete_arquivo, name='delete-atarquivo'),
    path('site/<slug:url>/workflow-arquivo/', workflow_arquivo, name='workflow-atarquivo'),

    # Visão
    path('site/<slug:url>/create-viewer/', create_viewer, name='create-atviewer'),
    path('site/<slug:url>/update-viewer/', update_viewer, name='update-atviewer'),
    path('site/<slug:url>/delete-viewer/', delete_viewer, name='delete-atviewer'),
    path('site/<slug:url>/workflow-viewer/', workflow_viewer, name='workflow-atviewer'),

    # Imagem Manager
    path('site/<slug:url>/imagem-manager-list/', imagem_manage_list, name='imagem-manage-list'),
    path('site/<slug:url>/imagem-manager-upload/', imagem_manage_upload, name='imagem-manage-upload'),
    path('site/<slug:url>/<int:oid>/imagem-manager-set/', imagem_manage_set, name='imagem-manage-set'),
    

    # Doc Manager
    path('site/<slug:url>/doc-manager-list/', doc_manage_list, name='doc-manage-list'),
    path('site/<slug:url>/doc-manager-upload/', doc_manage_upload, name='doc-manage-upload'),
    path('site/<slug:url>/<int:oid>/doc-manager-set/', doc_manage_set, name='doc-manage-set'),
]
