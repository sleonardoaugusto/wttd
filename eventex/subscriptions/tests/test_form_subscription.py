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
