from django.core.exceptions import PermissionDenied
from a_Acl.models import FactoryClassModel


class ACLService:

    @staticmethod
    def has_permission(user, site, tipo, permission_slug):

        SiteRole = FactoryClassModel.get_class('site_role')
        Permission = FactoryClassModel.get_class('permission')

        try:

            site_role = SiteRole.objects.prefetch_related(
                'permissions',
                'roles__permissions'
            ).get(
                user=user,
                site__url=site
            )

        except SiteRole.DoesNotExist:
            return False

        # permissões diretas
        if site_role.permissions.filter(
            slug=permission_slug,
            content_type__tipo=tipo
        ).exists():

            return True

        # roles do usuário
        roles = site_role.roles.all()


        # permissões herdadas
        return Permission.objects.filter(
            atribuidos_em_role__in=roles,
            slug=permission_slug,
            content_type__tipo=tipo
        ).exists()


    @staticmethod
    def require_permission(user, site, tipo, permission_slug):

        if not ACLService.has_permission(
            user,
            site,
            tipo,
            permission_slug,
        ):

            raise PermissionDenied(
                'Você não possui permissão.'
            )