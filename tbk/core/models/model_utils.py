from django.core.serializers.json import DjangoJSONEncoder

__all__ = ["MyJsonEncoder"]


class MyJsonEncoder(DjangoJSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs["ensure_ascii"] = False
        super().__init__(*args, **kwargs)
