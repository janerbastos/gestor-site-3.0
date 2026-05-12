from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Content, Event
from a_Site.models import FactoryClassModel


@receiver(post_save, sender=Content)
def sync_event_from_content(sender, instance, created, **kwargs):
    """
    Sincroniza automaticamente a entidade Event quando
    um Content do tipo ATInforme for criado ou atualizado.

    Os atributos temporais são obtidos do campo JSON
    presente em Content.data.
    """

    ContentType = FactoryClassModel.get_class('tipo')

    if instance.tipo not in [ContentType.ATEVENTO, ContentType.ATAGENDA]:
        return

    data = instance.data or {}

    inicio = data.get('inicio')
    termino = data.get('termino')

    if not inicio:
        return

    Event.objects.update_or_create(
        content=instance,
        defaults={
            'inicio': inicio,
            'termino': termino,
            'site': instance.site,
            'tipo' : instance.tipo
        }
    )