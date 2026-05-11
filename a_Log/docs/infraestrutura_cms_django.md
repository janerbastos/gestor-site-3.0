# Infraestrutura — CMS Django Portal

## Visão Geral

Arquitetura recomendada para um CMS Django escalável, desacoplado e preparado para:

- Analytics
- Auditoria
- Segurança
- Armazenamento/Mídia
- Observabilidade

---

# Arquitetura Geral

```text
                    ┌────────────────────┐
                    │   Google Analytics │
                    │        (GA4)       │
                    └─────────┬──────────┘
                              │
                              │ API
                              ▼
                    ┌────────────────────┐
                    │  GoogleAnalytics   │
                    │      Service       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Dashboard CMS      │
                    │ Analytics Público  │
                    └────────────────────┘



┌─────────────────────────────────────────────┐
│                 Django CMS                  │
└─────────────────────────────────────────────┘

        ┌─────────────────────────────┐
        │        a_Log App            │
        └─────────────────────────────┘

        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼
   Auditoria       Segurança      Storage
```

---

# Estrutura do Projeto

```text
a_Log/
├── admin.py
├── apps.py
├── middleware.py
├── signals.py
├── urls.py
├── views.py
│
├── models/
│   ├── audit.py
│   ├── security.py
│   └── storage.py
│
├── services/
│   ├── audit_service.py
│   ├── security_service.py
│   ├── storage_service.py
│   └── google_analytics_service.py
│
├── dashboards/
│   ├── analytics_dashboard.py
│   ├── storage_dashboard.py
│   └── security_dashboard.py
│
├── templatetags/
│   └── storage_tags.py
│
├── tasks/
│   ├── cleanup_logs.py
│   └── aggregate_stats.py
│
└── templates/
    └── components/
```

---

# Componentes da Infraestrutura

## 1. Google Analytics 4 (GA4)

Responsável por:

- pageviews
- sessões
- usuários ativos
- geolocalização
- dispositivos
- origem do tráfego

### Fluxo

```text
Usuário
   ↓
Portal
   ↓
GA4 coleta métricas
   ↓
Django consulta API
   ↓
Dashboard CMS
```

---

## 2. Auditoria

Responsável por registrar:

- criação conteúdo
- edição
- exclusão
- permissões
- login/logout
- publicação

### Modelo

```python
class AuditLog(models.Model):

    user
    action
    object_type
    object_id
    site
    ip
    message
    create_at
```

---

## 3. Segurança

Responsável por registrar:

- 403
- login inválido
- brute force
- acessos suspeitos

### Middleware

```text
PortalSecurityMiddleware
```

---

## 4. Storage/Mídia

Responsável por:

- espaço utilizado
- espaço livre
- percentual de uso
- quota futura

### Serviço

```text
MediaStorageService
```

### Exemplo de retorno

```python
{
    'partition_total_gb': 500,
    'partition_free_gb': 300,
    'media_used_gb': 120,
    'media_percent_used': 24.0
}
```

---

# Middleware

O middleware NÃO deve registrar todos os acessos.

Deve registrar apenas:

- eventos críticos
- acessos negados
- falhas autenticação
- eventos segurança

---

# Tasks/Celery

## cleanup_logs.py

Remove:

- logs antigos
- registros expirados

## aggregate_stats.py

Responsável por:

- consolidar estatísticas
- gerar relatórios
- cachear dashboards

---

# Dashboard CMS

## Cards sugeridos

- acessos hoje
- usuários ativos
- storage utilizado
- espaço livre
- erros 403
- login falho
- uploads recentes

---

# Infraestrutura Recomendada

## Aplicação

- Django 5+
- Gunicorn
- Nginx
- Python 3.12+

---

## Banco de Dados

- PostgreSQL

---

## Cache

- Redis

---

## Filas

- Celery
- Redis Broker

---

## Storage

- MEDIA_ROOT local
- NAS
- MinIO
- S3 futuro

---

## Observabilidade

- Grafana
- Loki
- ElasticSearch

---

# Docker

## Serviços recomendados

```text
nginx
django
postgres
redis
celery
celery-beat
```

---

# Segurança

## Recomendado

- ModSecurity
- OWASP CRS
- Fail2Ban
- CSRF
- CSP
- HTTPS obrigatório

---

# Escalabilidade

A arquitetura suporta:

- multiportal
- múltiplos domínios
- milhares acessos
- microsserviços futuros
- Kubernetes

---

# Benefícios

- desacoplamento
- escalabilidade
- baixo consumo banco
- manutenção simplificada
- analytics profissional
- auditoria organizada
- segurança centralizada

---

# Evolução Futura

Possíveis integrações:

- Google Analytics 4
- Google Tag Manager
- Looker Studio
- Grafana
- Redis
- Celery
- ElasticSearch
- OpenTelemetry

---

# Conclusão

Essa infraestrutura fornece:

- performance
- observabilidade
- segurança
- analytics
- auditoria
- escalabilidade

para um CMS Django moderno e multiportal.
