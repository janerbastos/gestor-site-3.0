from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.text import slugify

from a_Site.models import FactoryClassModel



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
        descendants = Content.objects.filter(path__startswith=old_path).exclude(pk=self.pk)

        for item in descendants:
            item.path = item.path.replace(old_path, self.path, 1)
            item.save()


    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        
        # Garante a unicidade do slug
        base_slug = self.url
        slug = base_slug
        counter = 1
        while Content.objects.filter(url=slug).exclude(pk=self.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        self.url = slug

        old_path = None
        if self.pk:
            old = Content.objects.get(pk=self.pk)
            old_path = old.path


        self.path = self.build_path()
        
        super().save(*args, **kwargs)

        # Atualiza filhos se mudou estrutura
        if old_path and old_path != self.path:
            self.update_descendants_path(old_path)

    
    class Meta:
        ordering = ['titulo']
        db_table = 'catalog_content'
        verbose_name = 'Catalago de conteúdo'
        verbose_name_plural = 'Catalagos de conteúdos'
        unique_together = (('site', 'url'),)


# Metodo fabrica
class FactoryClassModel:

    _class = {
        'content': Content,
    }

    @classmethod
    def get_class(cls, value):
        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')