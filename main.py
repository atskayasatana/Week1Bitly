import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(headers, url):
    api_url = "https://api-ssl.bitly.com/v4/shorten"
    payload = {"long_url": url}
    response = requests.post(api_url, json=payload,
                             headers=headers)
    response.raise_for_status()
    bitlink = response.json()
    return bitlink['link']


def count_cliks(headers, url):
    parsed_url = urlparse(url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    clicks = response.json()
    return clicks['total_clicks']


def is_bitlink(url, headers):
    parsed_url = urlparse(url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?')
    bitly_token = os.getenv('BITLY_TOKEN')
    headers = {"Authorization": bitly_token}
    user_url = parser.parse_args().url
    try:
        if is_bitlink(user_url, headers):
            print('Число переходов по ссылке:', 
                  count_cliks(headers, user_url))
        else:
            print('Битлинк', shorten_link(headers, user_url))
    except(requests.exceptions.HTTPError):
        print('Ошибка в адресе страницы')


if __name__ == "__main__":
    main()

