import random

from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class BrazilianProvider(BaseProvider):
    @staticmethod
    def document_id():
        return random.randint(11111111111, 99999999999)

    @staticmethod
    def phone(ddd=16):
        phone_number = random.randint(111111111, 999999999)
        return f"{ddd}{phone_number}"


fake.add_provider(BrazilianProvider)
