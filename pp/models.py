from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Quote(models.Model):
    title = models.CharField(max_length=100)  # movie / book
    text = models.TextField(unique=True, max_length=200)
    weight = models.FloatField(default=1.0)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["text"], name="unique_quote"),
        ]

    def clean(self):
        count = Quote.objects.filter(title=self.title).exclude(id=self.id).count()
        if count >= 3:
            raise ValidationError(
                f"Лимит по цитатам - {self.title}!"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text} ({self.title}) [{self.weight}]"


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "title", "weight"]
