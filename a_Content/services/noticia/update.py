from a_Content.models import FactoryClassModel

class UpdateNoticiaService:
    allowed_fields = [
        'url',
        'titulo',
        'descricao',
        'corpo',
        'tag',
        'show_in_menu',
        'excluir_nav',
    ]

    allowed_data_fields = [
        'imagem_destaque',
        'show_imagem',
        'legenda_imagem'
    ]

    def execute(self, data):

        Content = FactoryClassModel.get_class('content')

        content_id = data.get('id')

        if not content_id:
            return (
                'error',
                'ID não informado.'
            )

        try:

            content = Content.objects.get(id=content_id)

            updated_fields = []
            updated_data_fields = {}

            for field, value in data.items():
                if field not in self.allowed_fields:
                    continue
                setattr(content, field, value)
                updated_fields.append(field)

            # Atualizad campo data
            for field, value in data.items():
                if field not in self.allowed_data_fields:
                    continue
                if field == 'imagem_destaque' and not data.get('imagem_destaque'):
                    updated_data_fields[field]=content.data['imagem_destaque']
                    continue

                updated_data_fields[field]=value
            
            if updated_data_fields:
                setattr(content, 'data', updated_data_fields)
                updated_fields.append('data')

            if updated_fields:
                content.save(update_fields=updated_fields)

            return (
                'success',
                f'Conteúdo "{content.titulo}" atualizado.'
            )

        except Content.DoesNotExist:
            return (
                'error',
                'Conteúdo não encontrado.'
            )

        except Exception as e:
            return (
                'error',
                str(e)
            )