from handlers.pull_requests import get_pull_requests
from mock import patch
import unittest


class TestMergeRequests(unittest.TestCase):
    @patch('requests.get')
    def test_pull_requests(self, get_mock):
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = [
            {"title": "Add useful stuff", "number": 56, "html_url": "https://github.com/boto/boto3/pull/56"},
            {"title": "Fix something", "number": 57, "html_url": "https://github.com/boto/boto3/pull/57"},
        ]
        result = get_pull_requests(state="open")
        expected_result = [
            {"title": "Add useful stuff", "num": 56, "link": "https://github.com/boto/boto3/pull/56"},
            {"title": "Fix something", "num": 57, "link": "https://github.com/boto/boto3/pull/57"},
        ]
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_status(self, get_mock):
        get_mock.return_value.status_code = 404
        res = get_pull_requests(state='open')
        self.assertGreater(res.status_code, 200)

    @patch('response.json()')
    def test_reducing(self, get_mock):
        get_mock.return_value.json.return_value = [
            {"title": "Add useful stuff", "number": 56, "html_url": "https://github.com/boto/boto3/pull/56", "aboba": "some_info"},
            {"title": "Fix something", "number": 57, "html_url": "https://github.com/boto/boto3/pull/57"},
        ]
        result = get_pull_requests(state="close")
        expected_result = [
            {"title": "Add useful stuff", "num": 56, "link": "https://github.com/boto/boto3/pull/56"},
            {"title": "Fix something", "num": 57, "link": "https://github.com/boto/boto3/pull/57"},
        ]
        self.assertEqual(result, expected_result)

    @patch('my_module.requests.get')
    def test_get_pull_requests_empty_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        result = get_pull_requests(state="open")
        self.assertEqual(result, [])
