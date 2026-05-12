from a_Content.models import FactoryClassModel


class WorkflowAgendaService():
    allowed_fields = [
        'workflow',
    ]
    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        content_id = data.get('content_id')

        if not content_id:
            return (
                'error',
                'ID não informado.',
                None
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
                f'Conteúdo "{content.titulo}", {content.workflow}.',
                content
            )
        except Content.DoesNotExist:
            return (
                'error',
                'Conteúdo não encontrado.',
                None
            )

        except Exception as e:
            print(str(e))
            return (
                'error',
                str(e)
            )