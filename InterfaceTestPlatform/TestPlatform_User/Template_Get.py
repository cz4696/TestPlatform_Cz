# -*- coding: utf-8 -*-
import sys
import unittest
import requests

class TestCase_Get(unittest.TestCase):
    def setUp(self):
        pass

    def test_${ClassName}(self):
        res = requests.get(url='${UrlName}', params='${Params}')
        self.assertEqual(200,res.status_code,'失败')

    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_${ClassName})
    unittest.TextTestRunner(verbosity=2).run(suite)
