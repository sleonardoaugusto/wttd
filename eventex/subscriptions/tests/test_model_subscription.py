from django.test import TestCase

from eventex.subscriptions.models import Subscription
from eventex.test_utils.faker import fake


class SubscriptionModel(TestCase):
    def setUp(self) -> None:
        self.obj = Subscription.objects.create(
            name=fake.name(),
            cpf=fake.document_id(),
            email=fake.email(),
            phone=fake.phone(),
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_str(self):
        person_name = self.obj.name
        self.assertEqual(person_name, str(self.obj))
