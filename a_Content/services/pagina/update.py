from a_Content.models import FactoryClassModel


class UpdatePaginaService:

    def execute(self, data):

        Content = FactoryClassModel.get_class('content')

        content_id = data.get('id')

        if not content_id:
            return 'error', 'ID não informado'

        try:

            content = Content.objects.get(id=content_id)

            for field, value in data.items():

                if field == 'id':
                    continue

                if hasattr(content, field):
                    setattr(content, field, value)

            content.save()

            return 'success', content

        except Content.DoesNotExist:
            return 'error', 'Conteúdo não encontrado'

        except Exception as e:
            return 'error', str(e)