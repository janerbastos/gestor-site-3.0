from a_Content.models import FactoryClassModel


class UpdateAgendaService:

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
        'inicio',
        'termino',
        'local',
        'participante',
        'responsavel',
        'cor',
        'dia_todo',
        'observacao',
    ]

    def execute(self, data):
        Content = FactoryClassModel.get_class('content')
        data = data.copy()
        content_id = data.get('id')
        if not content_id:
            return (
                'error',
                'ID não informado.',
                None
            )

        try:
            if data.get('inicio'):
                data['inicio'] = (
                    data.get('inicio').isoformat()
                )
            if data.get('termino'):
                data['termino'] = (
                    data.get('termino').isoformat()
                )
            content = Content.objects.get(id=content_id)

            updated_fields = []
            updated_data_fields = {}

            # Atualiza campos principais
            for field in self.allowed_fields:
                if field not in data:
                    continue
                setattr(content, field, data[field])
                updated_fields.append(field)

            # Atualiza JsonField
            for field in self.allowed_data_fields:
                if field not in data:
                    continue
                updated_data_fields[field] = data[field]

            if updated_data_fields:
                current_data = content.data or {}
                current_data.update(updated_data_fields)
                setattr(content, 'data', current_data)
                updated_fields.append('data')

            if updated_fields:
                content.save(update_fields=updated_fields)

            return (
                'success',
                f'Conteúdo "{content.titulo}" atualizado.',
                content
            )

        except Content.DoesNotExist:
            return (
                'error',
                'Conteúdo não encontrado.',
                None
            )

        except Exception as e:
            return (
                'error',
                str(e),
                None
            )