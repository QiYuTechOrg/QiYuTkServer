from django.views.generic import TemplateView

__all__ = ["IndexView", "PrivacyView", "PingView"]


class IndexView(TemplateView):
    template_name = "tbk/html/index.html"


class PrivacyView(TemplateView):
    template_name = "tbk/html/privacy.html"


class PingView(TemplateView):
    template_name = "tbk/html/ping.html"
