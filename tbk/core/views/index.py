from django.views.generic import TemplateView

__all__ = ["PrivacyView", "PingView"]


class PrivacyView(TemplateView):
    template_name = "tbk/html/privacy.html"


class PingView(TemplateView):
    template_name = "tbk/html/ping.html"
