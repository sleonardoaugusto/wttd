from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self) -> None:
        data = dict(
            name="Leonardo Augusto",
            cpf=45009877899,
            email="sleonardoaugusto@gmail.com",
            phone="16-99130-6312",
        )
        self.response = self.client.post("/inscricao/", data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = "Confirmação de Inscrição"
        self.assertEqual(self.email.subject, expect)

    def test_subscription_email_form(self):
        expect = "contato@eventex.com.br"
        self.assertEqual(self.email.from_email, expect)

    def test_subscription_email_to(self):
        expect = ["contato@eventex.com.br", "sleonardoaugusto@gmail.com"]
        self.assertEqual(self.email.to, expect)

    def test_subscription_email_body(self):
        contents = [
            "Leonardo Augusto",
            "45009877899",
            "sleonardoaugusto@gmail.com",
            "16-99130-6312",
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
