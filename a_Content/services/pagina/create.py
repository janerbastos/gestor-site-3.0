from a_Content.models import FactoryClassModel

class CreatePaginaService:
    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        content = Content.objects.create(**data)
        return {
            'status': 'success',
            'message': f'Conteúdo "{content.titulo}" registrado.',
            'object': content,
        }