from django.core import mail
from django.shortcuts import resolve_url as r
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionNewGet(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get(r("subscriptions:new"))

    def test_get(self):
        """GET /inscricao must return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_html(self):
        """HTML must contain input tags"""
        tags = (
            ("<form", 1),
            ("<input", 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """HTML must contain CSRF token"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionNewPostValid(TestCase):
    def setUp(self) -> None:
        data = dict(
            name="Leonardo Augusto",
            cpf=45009877899,
            email="sleonardoaugusto@gmail.com",
            phone="16-99130-6312",
        )
        self.response = self.client.post(r("subscriptions:new"), data)

    def test_post(self):
        """Valid POST must redirect to /inscricao/<uuid>"""
        subscription = Subscription.objects.all().first()
        self.assertRedirects(
            self.response, r("subscriptions:detail", subscription.uuid)
        )

    def test_send_subscribe_email(self):
        self.assertEqual(len(mail.outbox), 1)

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionNewPostInvalid(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.post(r("subscriptions:new"), {})

    def test_post(self):
        """Invalid POST must not redirect"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_has_form(self):
        form = self.resp.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context["form"]
        self.assertTrue(form.errors)

    def test_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
