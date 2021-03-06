import uuid

from django.shortcuts import resolve_url as r
from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetalGet(TestCase):
    def setUp(self) -> None:
        self.obj = Subscription.objects.create(
            name="Subscriber Name",
            cpf="99999999999",
            email="subscriber@email.com",
            phone="99-999999999",
        )
        self.resp = self.client.get(r("subscriptions:detail", self.obj.uuid))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_detail.html")

    def test_context(self):
        subscription = self.resp.context["subscription"]
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (
            self.obj.name,
            self.obj.cpf,
            self.obj.email,
            self.obj.phone,
        )
        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r("subscriptions:detail", uuid.uuid4()))
        self.assertEqual(404, resp.status_code)
