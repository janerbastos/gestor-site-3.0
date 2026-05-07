from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError


class SiteRole(models.Model):
    site = models.ForeignKey('a_Site.Site', on_delete=models.CASCADE, related_name='membros_roles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='site_roles')
    permissions = models.ManyToManyField('Permission', related_name='permissoes_em_sites')
    roles = models.ManyToManyField('Role', related_name='atribuidas_em_sites')


    def __str__(self):
        return f"{self.user.username} - {self.site.titulo}"

    class Meta:
        db_table = 'a_acl_siterole'
        unique_together = (("user", "site"),)
        verbose_name = 'Papel no Site'
        verbose_name_plural = 'Papéis nos Sites'


class Role(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    level = models.PositiveIntegerField(default=0)
    permissions = models.ManyToManyField('Permission', related_name='atribuidos_em_role')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'a_acl_role'
        verbose_name = 'Papel'
        verbose_name_plural = 'Papéis'


class Permission(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    content_type = models.ForeignKey('a_Site.ContentType', on_delete=models.CASCADE, related_name='permissoes')

    def __str__(self):
        return f"{self.nome} ({self.content_type.descricao})"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'slug': self.slug,
            'content_type': self.content_type.tipo
        }


    class Meta:
        db_table = 'a_acl_permission'
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'


class EmailToken(models.Model):
    """
    Modelo para armazenar tokens de verificação enviados por e-mail para autenticação em dois fatores (2FA).

    Campos:
        user (ForeignKey): Referência ao usuário que receberá o token.
        code (CharField): Código do token enviado por e-mail (ex: 6 dígitos).
        created_at (DateTimeField): Data e hora de criação do token.
        expires_at (DateTimeField): Data e hora de expiração do token.
        used (BooleanField): Indica se o token já foi utilizado.

    Métodos:
        is_valid():
            Verifica se o token ainda é válido (não expirou e não foi utilizado).
            Retorna True se válido, False caso contrário.
    """    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at


class AuditLog(models.Model):
    """
    Modelo para registro de eventos de auditoria relacionados a ações de usuários no sistema.

    Objetivo:
        Permitir rastreamento e análise de ações importantes para segurança, conformidade e diagnóstico.

    Campos:
        user (ForeignKey): Usuário relacionado ao evento (pode ser nulo para eventos anônimos).
        event (CharField): Tipo do evento, escolhido entre opções predefinidas (ex: login, 2FA, alteração de senha).
        ip_address (GenericIPAddressField): Endereço IP de onde a ação foi realizada (opcional).
        user_agent (TextField): Informações do navegador/dispositivo do usuário (opcional).
        timestamp (DateTimeField): Data e hora do evento (padrão: agora).
        extra (JSONField): Dados adicionais relevantes ao evento, armazenados em formato JSON.

    EVENT_CHOICES:
        - "login_success": Login com sucesso
        - "login_failed": Tentativa de login falha
        - "logout_success": Logout com sucesso
        - "2fa_token_sent": Token 2FA enviado
        - "2fa_validated": Token 2FA validado
        - "password_reset_requested": Solicitação de redefinição de senha
        - "password_reset_done": Senha redefinida
        - "password_changed": Senha alterada
        - "permissions_changed": Permissões ou grupos alterados

    Métodos:
        __str__(): Retorna uma representação textual do evento, incluindo data/hora, tipo e usuário.

    Exemplo de uso:
        AuditLog.objects.create(
            user=request.user,
            event="login_success",
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
            extra={"detalhe": "Login via formulário"}
        )
    """
    EVENT_CHOICES = [
        ("login_success", "Login com sucesso"),
        ("login_failed", "Tentativa de login falha"),
        ("logout_success", "Logout com sucesso"),
        ("register_success", "Registro de novo usuário"),
        ("register_send_email_activate", "Email de ativação de conta enviado"),
        ("register_activate", "Registro de usuário ativado com sucesso"),
        ("register_activate_failed", "Link de ativação inválido ou expirado"),
        ("2fa_token_sent", "Token 2FA enviado"),
        ("2fa_validated", "Token 2FA validado"),
        ("password_reset_requested", "Solicitação de redefinição de senha"),
        ("password_reset_done", "Senha redefinida"),
        ("password_changed", "Senha alterada"),
        ("permissions_changed", "Permissões ou grupos alterados"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    extra = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.event} - {self.user or 'desconhecido'}"


# Metodo fabrica
class FactoryClassModel:

    _class = {
        'role': Role,
        'site_role': SiteRole,
        'permission' : Permission
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')