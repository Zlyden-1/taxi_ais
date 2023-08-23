from django import forms
from django.utils import timezone

from references.models import Driver
from .models import Rent


class CreateRentPaymentForm(forms.ModelForm):
    contractor = forms.ModelChoiceField(Driver.objects.all(), label='Исполнитель')
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.localdate(),
                                   label='Дата')
    summ = forms.IntegerField(label='Сумма')

    class Meta:
        fields = ('contractor', 'payment_date', 'summ', 'comment')
        model = Rent


class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=True, label='Начальная дата', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, label='Конечная дата', widget=forms.DateInput(attrs={'type': 'date'}))