from a_Content.models import FactoryClassModel

class CreatePastaService:
    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        content = Content.objects.create(**data)
        return (
            'success',
            f'Conteúdo "{content.titulo}" registrado.',
            content,
        )