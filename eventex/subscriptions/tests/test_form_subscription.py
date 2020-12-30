from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.test_utils.faker import fake


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        self.form = SubscriptionForm()
        expected = ["name", "cpf", "email", "phone"]
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_digit(self):
        """CPF must only accept digits"""
        form = self.make_validated_form(cpf="asdf1111111")
        self.assertFormErrorCode(form, "cpf", "digit")

    def test_length(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf="999999999")
        self.assertFormErrorCode(form, "cpf", "length")

    def test_capitalize(self):
        """Name must be capitalized"""
        form = self.make_validated_form(name="leonardo AUGUSTO")
        self.assertEqual(form.cleaned_data["name"], "Leonardo Augusto")

    def test_email_optional(self):
        """Email field should be optional"""
        form = self.make_validated_form(email="")
        self.assertFalse(form.errors)

    def test_phone_optional(self):
        """Phone field should be optional"""
        form = self.make_validated_form(phone="")
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and Phone are optional, but one must be informed"""
        form = self.make_validated_form(email="", phone="")
        self.assertListEqual(["__all__"], list(form.errors))

    def test_invalid_email_and_phone_not_informed(self):
        """Must show errors if email is invalid and phone is not informed"""
        form = self.make_validated_form(
            name=fake.name(), cpf=fake.document_id(), email="asdf", phone=""
        )
        self.assertListEqual(["email", "__all__"], list(form.errors))

    @staticmethod
    def make_validated_form(**kwargs):
        valid = dict(
            name=fake.name(),
            cpf=fake.document_id(),
            email=fake.email(),
            phone=fake.phone(),
        )
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

    def assertFormErrorCode(self, form, field, code):
        form.is_valid()
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)
