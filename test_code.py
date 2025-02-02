import unittest
from main import app  # импортируем приложение Flask

class TestHomePage(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Проверяем, что главная страница возвращает HTML и статус 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

if __name__ == '__main__':
    print(unittest.main())