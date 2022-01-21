from django import forms
from django.urls import reverse_lazy
from datetime import date
from django.core.exceptions import ValidationError

from .models import Transaction

class DateInput(forms.DateInput):
    input_type = "date"


def convert_to_negative_value(data):
    """
    if the user entered a value and it's higher > 0, we wil convert to a,
    negative value.
    """

    if data and data > 0:
        data = data * -1
    return data

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "date",
            "exchange",
            "sold_currency_amount",
            "sold_currency",
            "sold_currency_fee",
            "bought_currency_amount",
            "bought_currency",
            "bought_currency_fee",
        )

        #bank label, removes the label
        labels = {
            "date": "Date of transaction",
            "exchange": "Exchange",
            "sold_currency_amount": "",
            "sold_currency": "",
            "sold_currency_fee": "",
            "bought_currency_amount": "",
            "bought_currency": "",
            "bought_currency_fee": "",
        }
        
        #we are using widgets and attrs to update the placeholder
        widgets = {
            "date": DateInput(),
            "exchange": forms.TextInput(
                attrs={
                    "placeholder": "Exchange"
                }
            ),
            "sold_currency_amount": forms.TextInput(
                attrs={
                    "placeholder": "Total Amount",
                }
            ),
            "sold_currency": forms.TextInput(
                attrs={
                    "placeholder": "Fiat or Crypto",
                    "autocomplete": "off",
                    "hx-trigger": "click",
                    "hx-get": reverse_lazy("currencies", kwargs = { "input_clicked" : "sold"  }),
                    "hx-target": "#results_sold"
                }
            ),
            "sold_currency_fee": forms.TextInput(
                attrs={
                    "placeholder": "Fee Amount",
                }
            ),
            "bought_currency_amount": forms.TextInput(
                attrs={
                    "placeholder": "Total Amount",
                }
            ),
            "bought_currency": forms.TextInput(
                attrs={
                    "placeholder": "Fiat or Crypto",
                    "autocomplete": "off",
                    "hx-trigger": "click",
                    "hx-get": reverse_lazy("currencies", kwargs = { "input_clicked" : "bought"  }),
                    "hx-target": "#results_sold"
                }
            ),
            "bought_currency_fee": forms.TextInput(
                attrs={
                    "placeholder": "Fee Amount",
                }
            ),
        }

    """
    if the user entered a value and it's higher > 0, we wil convert to a,
    negative value.
    """
    def clean_sold_currency_amount(self):
        data = self.cleaned_data["sold_currency_amount"]
        return convert_to_negative_value(data)

    def clean_sold_currency_fee(self):
        data =self.cleaned_data["sold_currency_fee"]
        return convert_to_negative_value(data)

    def clean_bought_currency_fee(self):
        data =self.cleaned_data["bought_currency_fee"]
        return convert_to_negative_value(data)

    """
    If user enters future date for transaction throw validation error.
    """

    def clean_date(self):
        data = self.cleaned_data["date"]

        if data > date.today():
            raise ValidationError("You can't enter a future transaction!")
        return data
