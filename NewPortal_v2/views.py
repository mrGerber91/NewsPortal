from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'flatpages/home.html'
