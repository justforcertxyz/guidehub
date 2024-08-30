from django import forms
from .models import Inquiry

class CreateInquiryForm(forms.Form):
    class Meta:
        model = Inquiry
        fields = ['email', 'subject', 'text']