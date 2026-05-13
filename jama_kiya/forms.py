from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Payment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']  # ❌ username hata diya

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email
    



# 🔥 Customer Form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'daily_amount', 'start_date']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


# 🔥 Payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'note']  # ❌ received_by yaha nahi

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)