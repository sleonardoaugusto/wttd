from django.core.exceptions import ValidationError
from django.forms import models

from eventex.subscriptions.models import Subscription


class SubscriptionForm(models.ModelForm):
    class Meta:
        model = Subscription
        fields = ["name", "cpf", "email", "phone"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        words = name.split()
        words_capitalized = [w.capitalize() for w in words]
        return " ".join(words_capitalized)

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get("email") and not self.cleaned_data.get("phone"):
            raise ValidationError("Informe seu e-mail ou telefone")

        return self.cleaned_data
