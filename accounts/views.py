from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users to the dashboard
    return render(request, 'accounts/home.html')


# @login_required
# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')

from django.db.models import Sum
from expenses.models import Expense
import json
from datetime import datetime

@login_required
def dashboard(request):
    user = request.user

    # Total Expenses
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Expenses by Category
    category_data = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))
    categories = [expense['category'] for expense in category_data]
    category_totals = [float(expense['total']) for expense in category_data]  # Convert Decimal to float

    # Monthly Expenses
    monthly_data = Expense.objects.filter(user=user).values('date').annotate(total=Sum('amount'))
    month_expense_dict = {}
    for entry in monthly_data:
        month_name = datetime.strptime(str(entry['date']), "%Y-%m-%d").strftime("%B")
        month_expense_dict[month_name] = month_expense_dict.get(month_name, 0) + float(entry['total'])

    months = list(month_expense_dict.keys())
    monthly_totals = list(month_expense_dict.values())

    return render(request, 'accounts/dashboard.html', {
        'total_expenses': total_expenses,
        'categories': json.dumps(categories),  # Properly formatted JSON
        'category_totals': json.dumps(category_totals),
        'months': json.dumps(months),
        'monthly_totals': json.dumps(monthly_totals),
    })


# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created! You can log in now.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

    return render(request, 'accounts/register.html')

# User Login
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:  # Keep session alive if "Remember Me" is checked
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser close = logout

            return redirect('dashboard')

    return render(request, 'accounts/login.html')


# User Logout
def user_logout(request):
    logout(request)
    return redirect('/')
