from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from .services import ImagemService


class Site(models.Model):
    STATUS_SITE = True
    PRIVADO = 'Privado'
    PUBLICO = 'Publico'

    CHOICE_STATUS = (
        (not STATUS_SITE, 'Site Bloqueado'),
        (STATUS_SITE, 'Site Ativo'),
    )

    CHOICE_WORKFLOW = (
        (PRIVADO, 'Privado'),
        (PUBLICO, 'Publico'),
    )

    url = models.SlugField(max_length=150, unique=True)
    titulo = models.CharField('Título', max_length=150)
    descricao = models.TextField('Breve descrição', default=None, null=True, blank=True)
    create_at = models.DateTimeField('Data de criação', auto_now_add=True)
    update_at = models.DateTimeField('Data de atualização', auto_now=True)
    status = models.BooleanField(default=STATUS_SITE, choices=CHOICE_STATUS, blank=True, null=True)
    facebook_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    twitter_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    youtube_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    google_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    flicker_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    rss_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    logo = models.ImageField(
        'Logo do site',
        upload_to=ImagemService.content_file_imagem_site,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        default=None)
    banner_topo = models.ImageField(
        'Banner de destaque',
        upload_to=ImagemService.content_file_imagem_site,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        default=None)
    favicon = models.ImageField(
        'Favicon',
        upload_to=ImagemService.content_file_imagem_site,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        default=None)
    texto_rodape = models.TextField(default=None, blank=True, null=True)
    facebook_cod = models.TextField(null=True, blank=True, default=None)
    twitter_cod = models.TextField(null=True, blank=True, default=None)
    youtube_cod = models.TextField(null=True, blank=True, default=None)
    google_cod = models.TextField(null=True, blank=True, default=None)
    flicker_cod = models.TextField(null=True, blank=True, default=None)
    analytic_cod = models.TextField(null=True, blank=True, default=None)
    html_cod = models.TextField(null=True, blank=True, default=None)
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    telefone = models.CharField(max_length=255, null=True, blank=True, default=None)
    workflow = models.CharField(max_length=20, default=PRIVADO, choices=CHOICE_WORKFLOW)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='criados_por_mim')
    tipos_conteudo = models.ManyToManyField('ContentType', related_name='sites_vinculados',)

    def __str__(self):
        return self.titulo
    
    def get_configure_url(self):
        return '/%s/configure/' % self.url
    
    def get_absolute_url(self):
        return '/%s/' % self.url
    
    def get_map_site(self):
        return '/%s/@@map_site/' % self.url
    
    def to_json(self):
        content_type = list(self.tipos_conteudo.values_list("id", flat=True))
        return {
            'id': self.id,
            'url': self.url,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'create_at': str(self.create_at),
            'update_at': str(self.update_at),
            'status': self.status,
            'facebook_link': self.facebook_link,
            'twitter_link': self.twitter_link,
            'youtube_link': self.youtube_link,
            'google_link': self.google_link,
            'flicker_link': self.flicker_link,
            'rss_link': self.rss_link,
            'logo': str(self.logo),
            'banner_topo': str(self.banner_topo),
            'favicon': str(self.favicon),
            'texto_rodape': self.texto_rodape,
            'facebook_cod': self.facebook_cod,
            'twitter_cod': self.twitter_cod,
            'youtube_cod': self.youtube_cod,
            'google_cod': self.google_cod,
            'flicker_cod': self.flicker_cod,
            'analytic_cod': self.analytic_cod,
            'html_cod': self.html_cod,
            'email': self.email,
            'telefone': self.telefone,
            'workflow': self.workflow,
            'content_type': content_type
        }

    def show_status(self):
        return 'Ativo' if self.status else 'Bloquado'

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        
        # Garante a unicidade do slug
        base_slug = self.url
        slug = base_slug
        counter = 1
        while Site.objects.filter(url=slug).exclude(pk=self.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        self.url = slug
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'portalufopa_site'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


class ContentType(models.Model):

    ATPAGINA  = 'ATPagina'
    ATPASTA   = 'ATPasta'
    ATNOTICIA = 'ATNoticia'
    ATINFORME = 'ATInforme'
    ATLINK    = 'ATLink'
    ATIMAGEM  = 'ATImagem'
    ATBANNER  = 'ATBanner'
    ATEVENTO  = 'ATEvento'
    ATAGENDA  = 'ATAgenda'
    ATARQUIVO = 'ATArquivo'
    ATSERVICO = 'ATServico'
    ATVIEW    = 'ATView'

    CHOICE_CONTENTTYPE = (
        ('', ''),
        (ATPAGINA, 'Páginas'),
        (ATNOTICIA, 'Notícias'),
        (ATPASTA, 'Pasta'),
        (ATINFORME, 'Informes'),
        (ATLINK, 'Links'),
        (ATIMAGEM, 'Imagens'),
        (ATBANNER, 'Banners'),
        (ATEVENTO, 'Eventos'),
        (ATAGENDA, 'Agendas'),
        (ATARQUIVO, 'Arquivo'),
        (ATSERVICO, 'Serviço'),
        (ATVIEW, 'Visão')
    )

    tipo = models.SlugField(max_length=20, choices=CHOICE_CONTENTTYPE, unique=True)
    descricao = models.CharField(max_length=100)
    
    def __str__(self):
        return self.descricao
    
    def json(self):
        return {
            'id': self.id,
            'tipo' : self.tipo,
            'descricao' : self.descricao
        }
    
    class Meta:
        db_table = 'portalufopa_contenttype'
        verbose_name = 'Tipo de Conteúdo'
        verbose_name_plural = 'Tipos de conteúdos'


class Tag(models.Model):
    tag = models.SlugField(max_length=150)
    titulo = models.CharField(max_length=150)
    
    imagem = models.ImageField(
        upload_to=ImagemService.content_file_imagem,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
        )
    site = models.ForeignKey('Site', on_delete=models.CASCADE, related_name='tags')

    create_at = models.DateField('Data de criação', auto_now_add=True)
    update_at = models.DateField('Data de atualização', auto_now=True)
    status = models.BooleanField(default=True)

    def to_json(self):
        return {
            'id': self.id,
            'tag': self.tag,
            'titulo': self.titulo,
            'imagem': str(self.imagem),
            'status': self.status,
            'create_at': str(self.create_at),
            'update_at': str(self.update_at),
            'site_id': self.site_id
        }

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.tag:
            base_slug = slugify(self.titulo)
            slug = base_slug
            counter = 1
            # Garante a unicidade do slug
            while Tag.objects.filter(tag=slug).exclude(pk=self.pk).exists():
                # Se existir, adiciona um contador para torná-lo único
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.tag = slug
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'portalufopa_tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


# Metodo fabrica
class FactoryClassModel:

    _class = {
        'site': Site,
        'tag': Tag,
        'tipo': ContentType
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')