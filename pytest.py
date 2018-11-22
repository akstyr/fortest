import unittest
import Hill

class My_test(unittest.TestCase):

    def test_norm(self):
        res = Hill.add_text(['a'], 7)
        self.assertEquals(res,['a', 33, 33, 33, 33, 33, 33])

# if __name__ == '__main__':
#     unittest.main()

# def test_norm(self):
#     res = Hill.add_text(['a'], 7)
#     self.assertEquals(res, ['a', 33, 33, 33, 33, 33, 33])