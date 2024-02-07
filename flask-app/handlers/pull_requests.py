from flask import Flask, jsonify
import os

import requests

TOKEN = os.getenv("TOKEN")
HEADERS = {'Authorization': f'Bearer {TOKEN}'}


def get_pull_requests(state):
    """
    Example of return:
    [
        {"title": "Add useful stuff", "num": 56, "link": "https://github.com/boto/boto3/pull/56"},
        {"title": "Fix something", "num": 57, "link": "https://github.com/boto/boto3/pull/57"},
    ]
    """
    response = requests.get("https://api.github.com/repos/boto/boto3/pulls", headers=HEADERS,
                            params={'state': state, 'per_page': 100})
    if response.status_code == 200:
        pulls = response.json()
        reduced_info = []
        for pr in pulls:
            pr_info = {
                'title': pr['title'],
                'num': pr['number'],
                'link': pr['html_url'],
            }
            reduced_info.append(pr_info)
        return reduced_info
    else:
        return jsonify({"error": "Failed to fetch data from GitHub"}), 500

