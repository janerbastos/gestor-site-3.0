from django.conf import settings
from django.core.cache import cache

from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient
)

from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)


class GoogleAnalyticsService:
    """
    Serviço responsável pela integração com Google Analytics 4.

    Objetivos:
    - Consultar métricas públicas do portal
    - Alimentar dashboards administrativos
    - Centralizar acesso à API GA4
    - Reduzir consultas repetidas via cache

    Métricas suportadas:
    - pageviews
    - usuários ativos
    - sessões
    - páginas populares
    - origem tráfego
    - dispositivos
    - países/cidades

    Requisitos:
    - Google Analytics 4
    - Google Analytics Data API habilitada
    - Service Account configurada

    Configurações esperadas:
    - GA4_PROPERTY_ID
    - GA4_CREDENTIALS_FILE
    """

    CACHE_TIMEOUT = 60 * 15

    PROPERTY_ID = getattr(
        settings,
        'GA4_PROPERTY_ID',
        None
    )

    CREDENTIALS_FILE = getattr(
        settings,
        'GA4_CREDENTIALS_FILE',
        None
    )


    @classmethod
    def get_client(cls):
        """
        Retorna cliente autenticado GA4.
        """

        return BetaAnalyticsDataClient.from_service_account_file(cls.CREDENTIALS_FILE)


    @classmethod
    def run_report(
        cls,
        metrics,
        dimensions=None,
        start_date='7daysAgo',
        end_date='today',
        limit=10,
        cache_key=None
    ):
        """
        Executa consulta genérica no GA4.
        """

        if cache_key:
            cached = cache.get(cache_key)
            if cached:
                return cached

        client = cls.get_client()
        request = RunReportRequest(
            property=f'properties/{cls.PROPERTY_ID}',
            metrics=[
                Metric(name=metric)
                for metric in metrics
            ],
            dimensions=[
                Dimension(name=dimension)
                for dimension in (
                    dimensions or []
                )
            ],
            date_ranges=[
                DateRange(
                    start_date=start_date,
                    end_date=end_date
                )
            ],
            limit=limit
        )

        response = client.run_report(request)
        result = []
        for row in response.rows:
            item = {
                'dimensions': [
                    value.value
                    for value in row.dimension_values
                ],
                'metrics': [
                    value.value
                    for value in row.metric_values
                ]
            }
            result.append(item)

        if cache_key:
            cache.set(
                cache_key,
                result,
                timeout=cls.CACHE_TIMEOUT
            )
        return result


    @classmethod
    def get_page_views( cls, days=7):
        """
        Retorna total pageviews.
        """
        result = cls.run_report(
            metrics=['screenPageViews'],
            start_date=f'{days}daysAgo',
            cache_key=f'ga4_pageviews_{days}'
        )

        if not result:
            return 0

        return int(
            result[0]['metrics'][0]
        )


    @classmethod
    def get_active_users(cls, days=7):
        """
        Retorna usuários ativos.
        """
        result = cls.run_report(
            metrics=['activeUsers'],
            start_date=f'{days}daysAgo',
            cache_key=f'ga4_active_users_{days}'
        )

        if not result:
            return 0

        return int(result[0]['metrics'][0])


    @classmethod
    def get_top_pages(cls, days=7, limit=10):
        """
        Retorna páginas mais acessadas.
        """
        return cls.run_report(
            metrics=['screenPageViews'],
            dimensions=['pagePath'],
            start_date=f'{days}daysAgo',
            limit=limit,
            cache_key=f'ga4_top_pages_{days}_{limit}'
        )


    @classmethod
    def get_top_cities(cls, days=7, limit=10):
        """
        Retorna cidades com mais acessos.
        """
        return cls.run_report(
            metrics=['activeUsers'],
            dimensions=['city'],
            start_date=f'{days}daysAgo',
            limit=limit,
            cache_key=f'ga4_top_cities_{days}_{limit}'
        )


    @classmethod
    def get_devices(cls, days=7):
        """
        Retorna acessos por dispositivo.
        """
        return cls.run_report(
            metrics=['activeUsers'],
            dimensions=['deviceCategory'],
            start_date=f'{days}daysAgo',
            cache_key=f'ga4_devices_{days}'
        )


    @classmethod
    def get_traffic_sources(cls, days=7, limit=10):
        """
        Retorna origem do tráfego.
        """
        return cls.run_report(
            metrics=['sessions'],
            dimensions=['sessionSource'],
            start_date=f'{days}daysAgo',
            limit=limit,
            cache_key=f'ga4_sources_{days}_{limit}'
        )