# -*- coding: utf-8 -*-
import sys
import unittest
import requests
import json

class test_${ClassName}(unittest.TestCase):
    def setUp(self):
        pass

    def test_${ClassName}(self):
        res = requests.post(url='${UrlName}', data='${Data}',
                                 json=json.dumps('${Data}'))
        self.assertEqual(200,res.status_code,'失败')

    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_${ClassName})
    unittest.TextTestRunner(verbosity=2). run(suite)

