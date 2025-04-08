from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AccountsStaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['home', 'register', 'login']  # Include only public views

    def location(self, item):
        return reverse(item)
