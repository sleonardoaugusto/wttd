from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError("CPF deve conter apenas números", "digit")

    if len(value) != 11:
        raise ValidationError("CPF deve conter 11 dígitos", "length")


class SubscriptionForm(forms.Form):
    name = forms.CharField(label="Nome")
    cpf = forms.CharField(label="CPF", validators=[validate_cpf])
    email = forms.EmailField(label="Email", required=False)
    phone = forms.CharField(label="Telefone", required=False)

    def clean_name(self):
        name = self.cleaned_data["name"]
        words = name.split()
        words_capitalized = [w.capitalize() for w in words]
        return " ".join(words_capitalized)

    def clean(self):
        if not self.cleaned_data.get("email") and not self.cleaned_data.get("phone"):
            raise ValidationError("Informe seu e-mail ou telefone")

        return self.cleaned_data
