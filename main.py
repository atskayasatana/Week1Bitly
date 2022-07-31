import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse
import sys


def shorten_link(authorization_data, url):
    api_url = "https://api-ssl.bitly.com/v4/shorten"
    payload = {"long_url": url}
    response = requests.post(api_url, json=payload,
                             headers=authorization_data)
    response.raise_for_status()
    bitlink = response.json()
    return bitlink['link']


def count_cliks(authorization_data, url):
    parsed_url = urlparse(url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    response = requests.get(api_url, headers=authorization_data)
    response.raise_for_status()
    clicks_info = response.json()
    return clicks_info['total_clicks']


def is_bitlink(url, authorization_data):
    parsed_url = urlparse(url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(api_url, headers=authorization_data)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('url',nargs='?',default='http://www.reddit.com')
    bitly_token = os.environ['BITLY_TOKEN']
    authorization_data = {"Authorization": bitly_token}
    user_url = parser.parse_args().url
    try:
        if is_bitlink(user_url, authorization_data):
            print('Число переходов по ссылке:', count_cliks(authorization_data, user_url))
        else:
            print('Битлинк', shorten_link(authorization_data, user_url))
    except(requests.exceptions.HTTPError):
        print('Ошибка в адресе страницы')


if __name__ == "__main__":
    main()
