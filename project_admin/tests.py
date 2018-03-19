from django.test import TestCase
from .forms import TokenForm


class TokenFormTest(TestCase):

    def setUp(self):
        self.token = "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9"

    def test_valid(self):
        form = TokenForm(data={'token': "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9"})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = TokenForm(data={'token': ""})
        self.assertFalse(form.is_valid())

    def test_token(self):
        form = TokenForm(data={'token': "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9"})
        self.assertEquals(form.data['token'], "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9")
