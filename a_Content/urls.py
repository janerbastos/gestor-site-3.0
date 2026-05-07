from django.urls import path
from a_Content.views import dashboard, create_pagina, update_pagina

app_name = 'content'

urlpatterns = [
    path('site/<slug:url>/catalogo/', dashboard, name='dashboard'),
    path('site/<slug:url>/catalogo/@@<path:path_url>/', dashboard, name='dashboard'),

    path('site/<slug:url>/create-pagina/', create_pagina, name='create-atpagina'),
    path('site/<slug:url>/update-pagina/', update_pagina, name='update-atpagina'),
]
