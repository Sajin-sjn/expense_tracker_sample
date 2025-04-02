from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from django.contrib import messages
from .models import Expense
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Assign logged-in user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('list_expenses')  # Redirect to expense list page
        else:
            messages.error(request, "There was an error adding the expense. Please check your inputs.")

    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


# @login_required
# def list_expenses(request):
#     expenses = Expense.objects.filter(user=request.user).order_by('-date')  # Fetch user-specific expenses
#     return render(request, 'expenses/list_expenses.html', {'expenses': expenses})


@login_required
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    category_choices = Expense.CATEGORY_CHOICES  # Get categories for dropdown

    # Get filter values from request
    category = request.GET.get('category')
    date = request.GET.get('date')
    search_query = request.GET.get('search')

    # Apply filters
    if category:
        expenses = expenses.filter(category=category)
    
    if date:
        expenses = expenses.filter(date=date)
    
    if search_query:
        expenses = expenses.filter(title__icontains=search_query) | expenses.filter(description__icontains=search_query)

    return render(request, 'expenses/list_expenses.html', {'expenses': expenses, 'category_choices': category_choices})



@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('list_expenses')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('list_expenses')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})
