# """ExpenseTracker URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('accounts.urls')), 
#     path('dashboard/', include('expenses.urls')),
#     # path('expenses/', include('expenses.urls')),
# ]



from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.views.generic import TemplateView

from accounts.sitemaps import AccountsStaticSitemap
from expenses.sitemaps import ExpensesStaticSitemap

sitemaps = {
    'accounts': AccountsStaticSitemap,
    'expenses': ExpensesStaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main routes
    path('', include('accounts.urls')),  # Landing + login/register
    path('dashboard/', include('expenses.urls')),  # Dashboard views

    # Sitemap route
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path('google3258ca76d67af9ee.html', TemplateView.as_view(template_name='google3258ca76d67af9ee.html', content_type='text/html')),

]


# pip install django-sitemap
