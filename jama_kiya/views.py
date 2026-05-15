from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,CustomerForm,PaymentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test,login_required
from .models import Customer,Payment,User
from django.db.models import Q
from django.db.models import Sum
from datetime import date


@user_passes_test(lambda u: not u.is_authenticated,login_url="home")
def user_registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.save()

            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'jama_kiya/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # 🔥 email ko username ki tarah use kar rahe hain
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'jama_kiya/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    customers = Customer.objects.all()
    customer_data = []

    for c in customers:
        total_paid = c.payments.aggregate(Sum('amount'))['amount__sum'] or 0

        # 🔥 start_date based calculation
        if c.start_date > date.today():
            total_days = 0
        else:
            total_days = (date.today() - c.start_date).days

        total_required = total_days * c.daily_amount
        balance = total_paid - total_required

        customer_data.append({
            'customer': c,
            'balance': balance,
            'due':abs(balance)
        })

    return render(request, 'jama_kiya/home.html', {
        'customer_data': customer_data
    })


@login_required
def customer_detail(request, id):
    customer = Customer.objects.get(id=id)

    # 🔥 Payment add logic same view me
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer
            payment.received_by = request.user
            payment.save()
            return redirect('customer_detail', id=id)
    else:
        form = PaymentForm()

    # 🔹 history
    payments = customer.payments.all().order_by('-date')

    # 🔹 balance calculation
    total_paid = customer.payments.aggregate(Sum('amount'))['amount__sum'] or 0

    total_days = (date.today() - customer.start_date).days + 1
    total_required = total_days * customer.daily_amount

    balance = total_paid - total_required

    return render(request, 'jama_kiya/customerpro.html', {
        'customer': customer,
        'form': form,
        'payments': payments,
        'balance': balance,
        'due':abs(balance)
    })

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # save ke baad dashboard pe
    else:
        form = CustomerForm()

    return render(request, 'jama_kiya/customeradd.html', {'form': form})
