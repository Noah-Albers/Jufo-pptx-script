import unittest

# Import test cases from separate test files
from tests.unit.templater.texttemplate.TestTexttemplate import TestTexttemplate

# Create a test suite
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTexttemplate))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
