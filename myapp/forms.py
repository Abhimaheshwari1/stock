from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction 

class SimpleSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SimpleSignupForm, self).__init__(*args, **kwargs)
        # Simplify field labels and remove verbose help text
        self.fields['username'].label = "Username"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['stock_symbol', 'transaction_type', 'shares', 'price']  # Replace with your actual fields

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Customizing field labels or help texts if needed
        self.fields['stock_symbol'].label = "Stock Symbol"
        self.fields['transaction_type'].label = "Transaction Type"
        self.fields['shares'].label = "Number of Shares"
        self.fields['price'].label = "Price per Share"