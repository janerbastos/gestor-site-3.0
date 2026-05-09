from a_Content.models import FactoryClassModel


class UpdatePaginaService:

    allowed_fields = [
        'url',
        'titulo',
        'descricao',
        'corpo',
        'show_in_menu',
        'excluir_nav',
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

            for field, value in data.items():

                if field not in self.allowed_fields:
                    continue

                setattr(content, field, value)

                updated_fields.append(field)

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