from django.shortcuts import resolve_url as r
from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(r("home"))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, "index.html")

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="{}"'.format(r("subscriptions:new")))

    def test_speakers(self):
        """Must contain spearkers section"""
        contents = [
            "Grace Hopper",
            "http://hbn.link/hopper-pic",
            "Alan Turing",
            "http://hbn.link/turing-pic",
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_speakers_link(self):
        expected = "{}#speakers".format(r("home"))
        self.assertContains(self.response, expected)
