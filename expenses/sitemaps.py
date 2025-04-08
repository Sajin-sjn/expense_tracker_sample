from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class ExpensesStaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ['add_expense', 'list_expenses']  # Include public views

    def location(self, item):
        return reverse(item)
