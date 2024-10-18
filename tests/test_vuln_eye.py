import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from vuln_eye import (
    make_request, test_sql_injection, test_xss, test_directory_traversal, test_open_redirect,
    test_command_injection, test_security_headers, test_admin_panel, test_csrf_token,
    test_file_upload, check_website_reachability, save_report
)

class TestVulnEye(unittest.TestCase):

    @patch('vuln_eye.requests.get')
    def test_sql_injection(self, mock_get):
        mock_get.return_value.text = "SQL syntax"
        self.assertTrue(test_sql_injection("http://example.com"))

        mock_get.return_value.text = "Safe response"
        self.assertFalse(test_sql_injection("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_xss(self, mock_get):
        mock_get.return_value.text = "<script>alert('XSS')</script>"
        self.assertTrue(test_xss("http://example.com"))

        mock_get.return_value.text = "Safe response"
        self.assertFalse(test_xss("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_directory_traversal(self, mock_get):
        mock_get.return_value.text = "root:x:0"
        self.assertTrue(test_directory_traversal("http://example.com"))

        mock_get.return_value.text = "Safe response"
        self.assertFalse(test_directory_traversal("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_open_redirect(self, mock_get):
        mock_get.return_value.status_code = 302
        mock_get.return_value.headers = {'Location': 'http://evil.com'}
        self.assertTrue(test_open_redirect("http://example.com"))

        mock_get.return_value.headers = {'Location': 'http://safe.com'}
        self.assertFalse(test_open_redirect("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_command_injection(self, mock_get):
        mock_get.return_value.text = "Linux"
        self.assertTrue(test_command_injection("http://example.com"))

        mock_get.return_value.text = "Safe response"
        self.assertFalse(test_command_injection("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_security_headers(self, mock_get):
        # Mock headers containing all security headers
        mock_get.return_value.headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': "default-src 'self'",
            'X-XSS-Protection': '1; mode=block'
        }
        result = test_security_headers("http://example.com")
        self.assertFalse(result)  # Expect no missing headers

        # Mock missing headers
        mock_get.return_value.headers = {}
        result = test_security_headers("http://example.com")
        self.assertEqual(result, {'Missing Security Headers': ['X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security', 'X-XSS-Protection']})

    @patch('vuln_eye.requests.post')
    def test_file_upload(self, mock_post):
        mock_post.return_value.text = "test.txt"
        self.assertTrue(test_file_upload("http://example.com"))

        mock_post.return_value.text = "Safe response"
        self.assertFalse(test_file_upload("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_csrf_token(self, mock_get):
        mock_get.return_value.text = "<form action='/submit'>"
        self.assertTrue(test_csrf_token("http://example.com"))

        mock_get.return_value.text = "<form action='/submit'><input name='csrf_token' value='12345'>"
        self.assertFalse(test_csrf_token("http://example.com"))

    @patch('vuln_eye.requests.get')
    def test_check_website_reachability(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertTrue(check_website_reachability("http://example.com"))

        mock_get.return_value.status_code = 404
        self.assertFalse(check_website_reachability("http://example.com"))

    @patch('vuln_eye.open', new_callable=unittest.mock.mock_open)
    def test_save_report(self, mock_open):
        # Simulate saving a report with vulnerabilities
        url = "http://example.com"
        vulnerabilities = {"SQL Injection": f"{url}?id="}
        save_report(url, vulnerabilities)

        # Check that the report file is opened for writing
        mock_open.assert_called_once()

        # Check each part of the report was written
        mock_open().write.assert_any_call(f"Vulnerability Report for {url}\n\n")
        mock_open().write.assert_any_call("Vulnerability: SQL Injection\n")
        mock_open().write.assert_any_call(f"Location: {url}?id=\n\n")

if __name__ == '__main__':
    unittest.main()
