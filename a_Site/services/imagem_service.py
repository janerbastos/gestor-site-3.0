from datetime import date
import uuid, os

from django.template.defaultfilters import slugify


class ImagemService:


    @classmethod
    def content_file_imagem(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = str(uuid.uuid4())
        filename = filename + '.' + ext
        return os.path.join('file/site/%s/imagens/%s' % (instance.site.url, date.today().year), filename)

    @classmethod
    def content_file_documento(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = str(uuid.uuid4())
        filename = filename + '.' + ext
        return os.path.join('file/site/%s/documentos/%s' % (instance.site.url, date.today().year), filename)

    @classmethod
    def content_file_imagem_site(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = str(uuid.uuid4())
        filename = filename + '.' + ext
        return os.path.join('file/site/%s/imagens/configure' % (instance.url), filename)
    
    @classmethod
    def content_file_generico(cls, instance, filename):

        ext = filename.split('.')[-1].lower()
        filename = f'{uuid.uuid4()}.{ext}'
        pasta = ('documentos'if instance.tipo_geral == 'documento' else 'imagens')

        # estrutura final
        return os.path.join(
            'file',
            'site',
            instance.site.url,
            pasta,
            str(date.today().year),
            filename
        )