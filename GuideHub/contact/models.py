from django.db import models
from django.utils import timezone


class Inquiry(models.Model):
    pub_date = models.DateTimeField("Date Published", default=timezone.now)
    email = models.EmailField("Inquirer E-Mail", max_length=254)
    subject = models.CharField("Inquiry Subject", max_length=50)
    text = models.TextField("Inquiry Text", max_length=2500)

    @classmethod
    def create_inquiry(cls, email, subject, text):
        return Inquiry.objects.create(email=email, subject=subject, text=text)
