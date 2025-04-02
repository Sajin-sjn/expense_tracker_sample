from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.list_expenses, name='list_expenses'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),  # ✅ Fix missing edit_expense URL
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # ✅ Fix missing delete_expense URL
]
