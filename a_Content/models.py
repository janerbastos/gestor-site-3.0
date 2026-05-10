from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.text import slugify

import os

from a_Site.models import FactoryClassModel
from a_Site.services.imagem_service import ImagemService



class Content(models.Model):

    PRIVADO = 'Privado'
    PUBLICO = 'Publico'
    REVISAO = 'Revisao'

    CHOICE_WORKFLOW = (
        (PRIVADO, 'Privado'),
        (PUBLICO, 'Publico'),
        (REVISAO, 'Revisão')
    )


    url          = models.SlugField(max_length=255)
    titulo       = models.CharField(max_length=255)
    descricao    = models.TextField(default=None, null=True, blank=True)
    corpo        = models.TextField(default=None, null=True, blank=True)
    create_at    = models.DateTimeField('Data de criação', auto_now_add=True)
    update_at    = models.DateTimeField('Data de atualização', auto_now=True)
    public_at    = models.DateTimeField('Data de publicacção', null=True, blank=True, default=None)
    workflow     = models.CharField(max_length=20, default='Privado', choices=CHOICE_WORKFLOW)
    tipo         = models.CharField(max_length=20, choices=FactoryClassModel.get_class('tipo').CHOICE_CONTENTTYPE)
    site         = models.ForeignKey('a_Site.Site', on_delete=models.CASCADE, related_name='catalogs')
    show_in_menu = models.BooleanField(default=True)
    excluir_nav  = models.BooleanField(default=False)
    dono         = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    path         = models.CharField(max_length=255, db_index=True)
    parent       = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    tag          = models.CharField(max_length=100, null=True, blank=True)
    data         = models.JSONField(null=True, blank=True)


    def clean(self):
        if self.parent == self:
            raise ValidationError("Um conteúdo não pode ser pai de si mesmo.")


    def __str__(self):
        return f"{self.titulo} ({self.tipo})"


    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'corpo': self.corpo,
            'create_at': self.create_at.isoformat() if self.create_at else None,
            'update_at': self.update_at.isoformat() if self.update_at else None,
            'public_at': self.public_at.isoformat() if self.public_at else None,
            'workflow': self.workflow,
            'tipo': self.tipo,
            'site': self.site.titulo if self.site else None,
            'show_in_menu': self.show_in_menu,
            'excluir_nav': self.excluir_nav,
            'dono': self.dono.get_full_name if self.dono else None,
            'path': self.path,
            'parent_id': self.parent_id,
            'data': self.data or {}
        }
    
    
    def build_path(self):
        if self.parent:
            return f"{self.parent.path}{self.url}/"
        return f"{self.url}/"


    def update_descendants_path(self, old_path):
        descendants = Content.objects.filter(
            path__startswith=old_path,
            site=self.site
        )
        for item in descendants:
            new_path = item.path.replace(
                old_path,
                self.path,
                1
            )

            # Atualiza direto no banco
            Content.objects.filter(pk=item.pk).update(
                path=new_path
            )
    

    def dynamic_content_rule(self):

        rule = ContentRule.objects.filter(
            content_type=self.tipo,
            site=self.site,
            active=True
        ).first()

        result = False


        if rule:
            self.parent = Content.objects.filter(path=rule.path, site=self.site).first()
            self.path = f'{rule.path}{self.url}/'
            result = True

        return result


    def save(self, *args, **kwargs):

        if not self.url:
            self.url = slugify(self.titulo)

        # unicidade
        base_slug = self.url
        slug = base_slug
        counter = 1

        rule = None
        if not self.id:
            rule = self.dynamic_content_rule()

        if not rule:
            while Content.objects.filter(
                url=slug,
                site=self.site
            ).exclude(pk=self.pk).exists():
                
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.url = slug.lower()

            # path antigo completo
            old_path = None

            if self.pk:
                old = Content.objects.get(pk=self.pk)
                old_path = old.path

            # gera novo path
            self.path = self.build_path()

        # salva atual
        super().save(*args, **kwargs)

        if not rule:
            # atualiza filhos
            if old_path and old_path != self.path:
                self.update_descendants_path(old_path)

    
    class Meta:
        ordering = ['titulo']
        db_table = 'catalog_content'
        verbose_name = 'Catalago de conteúdo'
        verbose_name_plural = 'Catalagos de conteúdos'
        unique_together = (('site', 'url'),)


class ContentRule(models.Model):

    ContentType = FactoryClassModel.get_class('tipo')

    CHOICE_CONTENTTYPE = (
        ('', ''),
        (ContentType.ATPAGINA,  'Páginas'),
        (ContentType.ATNOTICIA, 'Notícias'),
        (ContentType.ATINFORME, 'Informes'),
        (ContentType.ATLINK,    'Links'),
        (ContentType.ATIMAGEM,  'Imagens'),
        (ContentType.ATBANNER,  'Banners'),
        (ContentType.ATEVENTO,  'Eventos'),
        (ContentType.ATAGENDA,  'Agendas'),
        (ContentType.ATARQUIVO, 'Arquivo'),
        (ContentType.ATSERVICO, 'Serviço'),
    )

    site = models.ForeignKey('a_Site.Site', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=50, choices=CHOICE_CONTENTTYPE)
    path = models.CharField(max_length=255)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['content_type']
        db_table = 'catalog_role'
        verbose_name = 'Regra de conteúdo'
        verbose_name_plural = 'Regras de conteúdos'
        unique_together = (('site', 'content_type'),)


    def __str__(self):
        return f'{self.content_type} -> {self.path}'


class ArquivoMidia(models.Model):
    # =========================================================
    # Tipos gerais de mídia
    # =========================================================

    IMAGEM = 'imagem'
    DOCUMENTO = 'documento'
    VIDEO = 'video'
    AUDIO = 'audio'
    OUTRO = 'outro'

    CHOICES_TIPO = (
        (IMAGEM, 'Imagem'),
        (DOCUMENTO, 'Documento'),
        (VIDEO, 'Vídeo'),
        (AUDIO, 'Áudio'),
        (OUTRO, 'Outro'),
    )

    # =========================================================
    # Relacionamentos
    # =========================================================

    site = models.ForeignKey(
        'a_Site.Site',
        on_delete=models.CASCADE,
        related_name='arquivos'
    )
    dono = models.ForeignKey(
        'a_Account.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # =========================================================
    # Arquivo físico
    # =========================================================

    arquivo = models.FileField(
        upload_to=ImagemService.content_file_generico,
        max_length=500
    )

    # =========================================================
    # Metadados
    # =========================================================

    titulo = models.CharField(
        max_length=255,
        help_text='Nome amigável do arquivo'
    )

    slug = models.SlugField(
        max_length=255,
        blank=True
    )

    mimetype = models.CharField(
        max_length=100,
        editable=False,
        blank=True
    )

    extensao = models.CharField(
        max_length=10,
        editable=False,
        blank=True
    )

    tamanho = models.PositiveIntegerField(
        editable=False,
        default=0,
        help_text='Tamanho em bytes'
    )

    tipo_geral = models.CharField(
        max_length=20,
        choices=CHOICES_TIPO,
        default=OUTRO
    )

    # =========================================================
    # Auditoria
    # =========================================================

    create_at = models.DateTimeField(
        auto_now_add=True
    )

    update_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # Meta
    # =========================================================

    class Meta:
        db_table = 'catalog_midia'
        verbose_name = 'Arquivo de Mídia'
        verbose_name_plural = 'Arquivos de Mídia'
        ordering = ['-create_at']

    # =========================================================
    # Representação
    # =========================================================

    def __str__(self):

        return self.titulo

    # =========================================================
    # Save
    # =========================================================

    def save(self, *args, **kwargs):
        # slug automático

        if not self.slug:
            self.slug = slugify(self.titulo)

        # processamento arquivo
        if self.arquivo:
            self.extensao = (
                os.path.splitext(
                    self.arquivo.name
                )[1]
                .lower()
                .replace('.', '')
            )

            self.tamanho = self.arquivo.size
            self.tipo_geral = self.detect_tipo_geral()

        super().save(*args, **kwargs)

    # =========================================================
    # Detecta tipo da mídia
    # =========================================================

    def detect_tipo_geral(self):

        if self.extensao in [
            'jpg',
            'jpeg',
            'png',
            'gif',
            'webp',
            'svg'
        ]:

            return self.IMAGEM

        elif self.extensao in [
            'pdf',
            'doc',
            'docx',
            'xls',
            'xlsx',
            'ppt',
            'pptx',
            'txt'
        ]:

            return self.DOCUMENTO

        elif self.extensao in [
            'mp4',
            'avi',
            'mov',
            'mkv',
            'webm'
        ]:

            return self.VIDEO

        elif self.extensao in [
            'mp3',
            'wav',
            'ogg'
        ]:

            return self.AUDIO

        return self.OUTRO

    # =========================================================
    # JSON Reference
    # =========================================================

    def to_json_reference(self):

        """
        Estrutura pronta para persistência
        em JSONField.
        """

        return {

            'id': self.id,

            'url': self.arquivo.url,

            'titulo': self.titulo,

            'tipo': self.tipo_geral,

            'ext': self.extensao,

            'size': self.tamanho
        }


# Metodo fabrica
class FactoryClassModel:

    _class = {
        'content': Content,
        'midia' : ArquivoMidia,
        'role' : ContentRule
    }

    @classmethod
    def get_class(cls, value):
        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')