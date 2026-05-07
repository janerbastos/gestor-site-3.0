from a_Site.views.site_view import dashboard, create_site, edit_site, delete_site, open_site
from a_Site.views.site_configure_view import (
    edit_site_midia, edit_site_redesocial_link,
    edit_site_codigo_script, edit_site_contenttype,
    edit_site_endereco)
from a_Site.views.tag_view import list_tag, create_tag, edit_tag, delete_tag
from a_Site.views.portais_view import index

__ALL__ = [
    'dashboard', 'create_site', 'edit_site', 'delete_site',
    'open_site', 'edit_site_midia', 'edit_site_redesocial_link',
    'edit_site_codigo_script', 'edit_site_contenttype', 'edit_site_endereco',
    'list_tag', 'create_tag', 'edit_tag', 'delete_tag', index]