from django import forms
from .models import Inquiry


class CreateInquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['email', 'subject', 'text']
        labels = {
            'email': 'E-Mail-Adresse',
            'subject': 'Betreff',
            'text': 'Anfragentext',
        }
