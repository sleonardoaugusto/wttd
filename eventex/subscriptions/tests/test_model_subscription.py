from django.test import TestCase

from eventex.subscriptions.models import Subscription
from eventex.test_utils.faker import fake


class SubscriptionModel(TestCase):
    def test_create(self):
        obj = Subscription.objects.create(
            name=fake.name(),
            cpf=fake.document_id(),
            email=fake.email(),
            phone=fake.phone(),
        )
        obj.save()
        self.assertTrue(Subscription.objects.all())
