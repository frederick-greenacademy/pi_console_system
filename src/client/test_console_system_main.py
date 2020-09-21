import unittest
import pi_bluetooth as cp
import io
import xmlrunner
from xmlrunner.extra.xunit_plugin import transform

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'foo')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    def test_scan_BLE(self):
        xx = cp.scan_ble_nearby()
        self.assertEqual(len(xx), 2)      

if __name__ == '__main__':
    out = io.BytesIO()
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=out),
    failfast=False, buffer=False, catchbreak=False, exit=False)

    with open('TEST-report.xml', 'wb') as report:
        report.write(transform(out.getvalue()))