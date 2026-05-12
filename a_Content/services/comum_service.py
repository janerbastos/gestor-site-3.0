from a_Log.services.audit_service import (
    AuditService
)


class BaseContentServiceLog:
    """
    Classe base para serviços de conteúdo.

    Objetivos:
    - centralizar auditoria
    - reduzir duplicação
    - padronizar CRUD
    - facilitar manutenção
    - padronizar metadata/logs
    """

    action_create = 'create'
    action_update = 'update'
    action_delete = 'delete'

    def __init__(self, request, site):
        self.request = request
        self.site = site


    def log_create(self, obj, message=None, metadata=None):
        """
        Cria registro e audita.
        """

        AuditService.register_create(
            request=self.request,
            site=self.site,
            obj=obj,
            message=(message or self.get_create_message(obj)),
            metadata=(metadata or self.build_metadata(obj))
        )
        return obj


    def log_update(self, obj, obj_old, message=None, metadata=None):
        """
        Atualiza registro e audita.
        """
        before = self.serialize(obj_old)
        after = self.serialize(obj)

        AuditService.register_update(
            request=self.request, site=self.site, obj=obj,
            message=(message or self.get_update_message(obj) ),
            metadata=(metadata or {'before': before, 'after': after}
            )
        )
        return obj


    def log_delete(self, obj, message=None, metadata=None):
        """
        Remove registro e audita.
        """
        object_data = self.serialize(obj)
        object_id = obj.id
        object_name = str(obj)

        AuditService.register_delete(
            request=self.request,
            site=self.site,
            obj=obj,
            message=(message or f'{object_name} removido'),
            metadata=(
                metadata or {
                    'deleted_object': object_data,
                    'object_id': object_id
                }
            )
        )


    def serialize(self, obj):
        """
        Serialização simples para auditoria.
        """
        data = {}
        for field in obj._meta.fields:
            try:
                value = getattr(obj, field.name)
                data[field.name] = str(value)
            except Exception:
                continue
        return data


    def build_metadata(self, obj):
        """
        Metadata padrão.
        """
        return {'object_id': obj.id, 'object_type': (obj.__class__.__name__)}


    def get_create_message(self, obj):
        return (f'{obj} criado')


    def get_update_message(self, obj):
        return (f'{obj} atualizado')