from django.test import TestCase

from .. import lav_email


class LavEmailTestCase(TestCase):
    def test_hiding_email(self):
        value = lav_email.hiding_email('ivanenko123@mail.ru')
        result = 'iv***@mail.ru'
        self.assertEquals(value, result)
