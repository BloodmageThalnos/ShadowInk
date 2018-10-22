from django.test import TestCase
from TexasAPP.models import *
from TexasAPP.holdem_calc import run
from TexasAPP.holdem_functions import Card

class modelTestCase(TestCase):
    def setUp(self):
        pass

    def test_1(self):
        i,j = run([(Card('2s'),Card('3s')),(Card('2d'),Card('3d'))],40000)
        print(i)
        print(j)

    def test_model_2(self):
        print('ok2')
