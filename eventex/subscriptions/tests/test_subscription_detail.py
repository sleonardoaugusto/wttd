import uuid
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
        self.resp = self.client.get(f"/inscricao/{self.obj.uuid}/")

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
        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(f"/inscricao/{uuid.uuid4()}/")
        self.assertEqual(404, resp.status_code)
