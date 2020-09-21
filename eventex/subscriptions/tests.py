from django.core import mail
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


class SubscribePostTest(TestCase):
    def setUp(self) -> None:
        data = dict(
            name="Leonardo",
            cpf=45009877899,
            email="sleonardoaugusto@gmail.com",
            phone="16-99130-6312",
        )
        self.response = self.client.post("/inscricao", data)

    def test_post(self):
        """Valid POST must redirect to /inscricao"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(len(mail.outbox), 1)

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = "Confirmação de Inscrição"
        self.assertEqual(email.subject, expect)

    def test_subscription_email_form(self):
        email = mail.outbox[0]
        expect = "contato@eventex.com.br"
        self.assertEqual(email.from_email, expect)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ["contato@eventex.com.br", "leonardo@gmail.com"]
        self.assertEqual(email.to, expect)
