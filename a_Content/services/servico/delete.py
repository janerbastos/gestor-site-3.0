from a_Content.models import FactoryClassModel


class DeleteServicoService:

    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        content_id = data.get('content_id')
        if not content_id:
            return (
                'error',
                'ID do conteúdo não informado.'
            )
        try:
            content = Content.objects.get(id=content_id)
            titulo = content.titulo
            content.delete()
            return (
                'success',
                f'Conteúdo "{titulo}" excluído permanentemente.',
            )

        except Content.DoesNotExist:
            return 'error', 'Conteúdo não encontrado.'
        except Exception as e:
            return (
                'error',
                str(e)
            )