from a_Content.models import FactoryClassModel

class CreatePaginaService:
    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        return 'success', Content.objects.create(**data)