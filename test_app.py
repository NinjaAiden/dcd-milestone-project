from app import *
import datetime
import unittest


# test all pages are set up properly (correct page type, render appropriately)

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.app=app.test_client()
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        app.config['SECRET_KEY'] = 'SECRET_KEY'
    
    def TestIndex(self):
        response = self.app.get('/', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestLogin(self):
        response = self.app.get('/login', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestRegister(self):
        response = self.app.get('/register', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestAdd(self):
        response = self.app.get('/add_recipe', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestEdit(self):
        response = self.app.get('/edit_recipe', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestViewRecipe(self):
        response = self.app.get('/view_recipe/5c8286d6fb6fc07201313698', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)
    
    def TestSearch(self):
        response = self.app.get('/custom_search', content_type='hmtl/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()