from app import *
import datetime
import unittest

# test all pages are set up properly (correct page type, render appropriately)

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.app=app.test_client()
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        app.config['SECRET_KEY'] = 'SECRET_KEY'


if __name__ == '__main__':
    unittest.main()