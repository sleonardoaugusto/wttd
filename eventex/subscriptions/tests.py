from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get("/inscricao")

    def test_get(self):
        """GET /inscricao must return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.resp, "<form")
        self.assertContains(self.resp, "<input", 6)

    def test_csrf(self):
        """HTML must contain CSRF token"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context["form"]
        self.assertSequenceEqual(["name", "cpf", "email", "phone"], list(form.fields))
