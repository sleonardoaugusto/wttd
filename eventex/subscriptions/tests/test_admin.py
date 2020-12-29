from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin
from eventex.test_utils.faker import fake


class SubscriptionModelAdminTestCase(TestCase):
    def setUp(self):
        Subscription.objects.create(
            name=fake.name(),
            cpf=fake.document_id(),
            email=fake.email(),
            phone=fake.phone(),
        )
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

    def test_has_action(self):
        """Action mark_as_paid must be installed"""
        model_admin = SubscriptionModelAdmin(Subscription, admin.site)
        self.assertIn("mark_as_paid", model_admin.actions)

    def test_mark_all(self):
        """It should mark all selected subscriptions as paid"""
        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        """It should send a message to the user"""
        mock = self.call_action()
        mock.assert_called_once_with(None, "1 inscrição foi marcada como paga.")

    def call_action(self):
        qs = Subscription.objects.all()

        mock = Mock()
        self.model_admin.message_user = mock
        self.model_admin.mark_as_paid(None, qs)

        return mock
