from a_Content.views.manage_views import dashboard
from a_Content.views.page_view import create_pagina, update_pagina, delete_pagina, workflow_pagina
from a_Content.views.pasta_view import create_pasta, update_pasta, delete_pasta, workflow_pasta
from a_Content.views.noticia_view import create_noticia, update_noticia, delete_noticia, workflow_noticia
from a_Content.views.informe_view import create_informe, update_informe, delete_informe, workflow_informe
from a_Content.views.evento_view import create_evento, update_evento, delete_evento, workflow_evento
from a_Content.views.agenda_view import create_agenda, update_agenda, delete_agenda, workflow_agenda
from a_Content.views.servico_view import create_servico, update_servico, delete_servico, workflow_servico
from a_Content.views.link_view import create_link, update_link, delete_link, workflow_link
from a_Content.views.imagem_manage_view import imagem_manage_list, imagem_manage_upload, imagem_manage_set

__ALL__ = [
    'dashboard',
    'imagem_manage_list', 'imagem_manage_upload', 'imagem_manage_set',
    'create_pagina', 'update_pagina', 'delete_pagina', 'workflow_pagina'
    'create_pasta', 'update_pasta', 'delete_pasta', 'workflow_pasta',
    'create_noticia', 'update_noticia', 'delete_noticia', 'workflow_noticia',
    'create_informe', 'update_informe', 'delete_informe', 'workflow_informe',
    'create_evento', 'update_evento', 'delete_evento', 'workflow_evento',
    'create_agenda', 'update_agenda', 'delete_agenda', 'workflow_agenda',
    'create_servico', 'update_servico', 'delete_servico', 'workflow_servico',
    'create_link', 'update_link', 'delete_link', 'workflow_link',
    ]