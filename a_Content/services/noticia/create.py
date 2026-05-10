from a_Content.models import FactoryClassModel

class CreateNoticiaService:
    # Campos que são colunas reais na tabela catalog_content
    common_fields = [
        'url',
        'titulo',
        'descricao',
        'corpo',
        'show_in_menu',
        'excluir_nav',
        'site_id',
        'dono_id',
        'parent_id',
        'tipo',
        'tag',
        'workflow'
    ]

    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        
        content_params = {}
        metadata = {}

        # 1. Separação de campos (Colunas vs JSON)
        for field, value in data.items():
            if field in self.common_fields:
                content_params[field] = value
            elif field not in ['site_id', 'dono_id', 'parent_id']:
                # Campos como 'imagem-destaque', 'legenda_imagem', 'show_imagem' vão para o JSON
                metadata[field] = value

        # 2. Atribuição do JSONField
        content_params['data'] = metadata

        # 4. Criação do Conteúdo
        try:
            print(content_params)
            content = Content.objects.create(**content_params)
            return (
                'success',
                f'Notícia "{content.titulo}" registrada com sucesso.',
                content,
            )
        except Exception as e:
            return (
                'error',
                f'Erro ao registrar notícia: {str(e)}',
                None,
            )