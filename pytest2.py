import unittest
import Hill

class My_test(unittest.TestCase):

    def test_norm(self):
        res = Hill.find_inverse_element(35)
        self.assertEquals(res, 28)
