import unittest
from unittest.mock import patch
from app import app

class TestYourApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        response = self.app.get('/')

    # Check for the existence of key elements and content
        self.assertIn(b'<h1>System Monitoring</h1>', response.data)
        self.assertIn(b'<div id="cpu-gauge"></div>', response.data)
        self.assertIn(b'<div id="mem-gauge"></div>', response.data)

    # Check if the message is present when the condition is met
        if b'High CPU or Memory Detected' in response.data:
           self.assertGreaterEqual(response.data.count(b'<div class="alert alert-danger">'), 1)
        else:
           self.assertEqual(response.data.count(b'<div class="alert alert-danger">'), 0)

    def test_high_cpu_memory_message(self):
        with app.test_request_context():
            with app.test_client() as client:
            # Test when CPU is above the threshold
                with patch('psutil.cpu_percent', return_value=25):
                    response = client.get('/')
                    self.assertIn(b'High CPU or Memory Detected', response.data)

                # Test when memory is above the threshold
                with patch('psutil.virtual_memory') as mock_virtual_memory:
                    mock_virtual_memory.return_value.percent = 95
                    response = client.get('/')
                    self.assertIn(b'High CPU or Memory Detected', response.data)

if __name__ == '__main__':
    unittest.main()