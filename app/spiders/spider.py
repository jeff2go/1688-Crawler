import requests

def get_html(url, headers):
    response = requests.get(url, headers=headers, allow_redirects=False)
    return response.text
