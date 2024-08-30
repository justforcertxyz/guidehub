from django.db import models
from django.utils import timezone

# TODO: Move from model to email


class Inquiry(models.Model):
    pub_date = models.DateTimeField("Date Published", default=timezone.now)
    email = models.EmailField("Inquirer E-Mail", max_length=254)
    subject = models.CharField("Inquiry Subject", max_length=50)
    text = models.TextField("Inquiry Text", max_length=2500)

    processed = models.BooleanField("Inquiry Processed", default=False)

    @classmethod
    def create_inquiry(cls, email, subject, text):
        return Inquiry.objects.create(email=email, subject=subject, text=text)

    def __str__(self):
        return self.subject

    def finish_processing(self):
        self.processed = True
        self.save()
