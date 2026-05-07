import importlib
from a_Content.services.core.registry import SERVICES


class ServiceDispatcher:

    @staticmethod
    def dispatch(type_, action, **kwargs):
        key = f"{type_}.{action}"

        path = SERVICES.get(key)
        if not path:
            raise ValueError(f"Serviço não encontrado: {key}")

        module_path, class_name = path.rsplit(".", 1)

        module = importlib.import_module(module_path)
        service_cls = getattr(module, class_name)

        return service_cls().execute(**kwargs)