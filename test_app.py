import unittest
from unittest.mock import patch, MagicMock
from format_engine import FormatEngine
import main
import json

class TestFormatEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FormatEngine()
        self.data = {"title": "Test Title", "content": "Test Content", "summary": "Test Summary"}

    def test_render_html(self):
        template = "<h1>{{ title }}</h1><p>{{ content }}</p>"
        result = self.engine.render_html(self.data, template)
        self.assertIn("<h1>Test Title</h1>", result)
        self.assertIn("<p>Test Content</p>", result)

    def test_render_markdown(self):
        result = self.engine.render_markdown(self.data)
        self.assertIn("# Test Title", result)
        self.assertIn("**Summary:** Test Summary", result)
        self.assertIn("Test Content", result)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()
        self.app.testing = True

    @patch('main.reflection_loop')
    def test_trigger_pipeline_html(self, mock_loop):
        mock_loop.return_value = {
            "original_draft": "Draft",
            "critique": "Critique",
            "final_content": "Final Content"
        }

        payload = {"data": "Some raw data"}
        response = self.app.post('/trigger', json=payload)

        self.assertEqual(response.status_code, 200)
        # response.data is bytes
        self.assertIn(b"Final Content", response.data)
        # Check Content-Type. Flask test client might return it in headers.
        self.assertTrue("text/html" in response.content_type)

    @patch('main.reflection_loop')
    def test_trigger_pipeline_markdown(self, mock_loop):
        mock_loop.return_value = {
            "original_draft": "Draft",
            "critique": "Critique",
            "final_content": "Final Content"
        }

        payload = {"data": "Some raw data", "format": "markdown"}
        response = self.app.post('/trigger', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Final Content", response.data)
        self.assertTrue("text/markdown" in response.content_type)

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
