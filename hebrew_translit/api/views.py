from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
import requests
import csv
import json
from urllib.parse import urlencode
import urllib.parse

from urllib.request import Request, urlopen
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def main(request):
    text_with_punctuation = add_punctuation(request)
    text_phonetic = convert_to_phonetic(text_with_punctuation)
    lyric_link = scrape_lyric()
    return JsonResponse({'text_with_punctuation': text_with_punctuation,
                         'text_phonetic': text_phonetic,
                         'lyric_link': lyric_link},
                        content_type="application/json", safe=False)


def add_punctuation(request):
    response = requests.post(
        'https://nakdan-4-0.loadbalancer.dicta.org.il/api', json={
            'data': request.body,
            'genre': "modern",
            'task': "nakdan",
        },
    )
    response.status_code
    dataPunctuation = response.json()
    returned_string = ""

    for word in dataPunctuation:
        if (word['options']):
            eachWord = word['options'][0]
            returned_string = returned_string + ' ' + eachWord
    return (returned_string)


def convert_to_phonetic(text_with_punctuation):
    # encode text to utf-8
    # text_with_punctuation.urllib.parse.quote(
    #     text_with_punctuation)
    # print(text_with_punctuation, 'after encoding')
    print("text_with_punctuation", text_with_punctuation)
    text_with_punctuation_encoded = urllib.parse.quote(text_with_punctuation)
    print("text_with_punctuation_encoded", text_with_punctuation_encoded)

    print(urllib.parse.unquote('%D7%97%D6%B2%D7%AA%D7%95%D6%BC%D7%A0%D6%B8%D7%94'))

    # assert text_with_punctuation_encoded == '%D7%97%D6%B2%D7%AA%D7%95%D6%BC%D7%A0%D6%B8%D7%94'

    post_prefix = 'https://alittlehebrew.com/transliterate/get.php?token=b68d80fe5b414070ec66441540697eac1b1bb3a34dcaaf1c552b6a33c023e093&style=000_simple_sefardi&syllable=auto&accent=auto&hebrew_text='
    response = requests.post(

        f'{post_prefix}{text_with_punctuation_encoded}',
        # f'{post_prefix}%D7%97%D6%B2%D7%AA%D7%95%D6%BC%D7%A0%D6%B8%D7%94',

        # json={
        #     'data': text_with_punctuation,
        #     'token': 'b68d80fe5b414070ec66441540697eac1b1bb3a34dcaaf1c552b6a33c023e093',
        #     'style': '000_simple_sefardi',
        #     'syllable': 'auto',
        #     'accent': 'auto',
        # },
        headers={
            "Content-Type": "application/json",
            'Accept': 'keep-alive',
            "Cookie": 'PHPSESSID=3203226df62e4868d7704ea3a24771a5',
            "Connection": 'keep-alive',
            "Referer": 'https://alittlehebrew.com/transliterate/',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            "x-requested-with": 'XMLHttpRequest',
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": 'cors',
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-IE,en-US;q=0.9,en;q=0.8,he;q=0.7",
            'sec-fetch-dest': 'empty',
            'Referer': 'https://alittlehebrew.com/transliterate/',
            'Connection': 'keep-alive',
            'Accept': '*/*'

        },

    )
    response.status_code
    dataPhonetic = response.json()
    first_option_phonetic = dataPhonetic['result']
    # todo FIX when there is an error on the call the object change and the value I need is from 'message', not result
    print("first_option_phonetic", first_option_phonetic)
    return (first_option_phonetic)


def scrape_lyric():
    lyric = 'כולם על הגל'
    source = requests.get(
        "https://shironet.mako.co.il/search?q=%D7%9B%D7%95%D7%9C%D7%9D%2B%D7%A2%D7%9C%2B%D7%94%D7%92%D7%9C")
    soup = BeautifulSoup(source.text, features="lxml")
    for sessionHebrew in soup.find_all('div', class_='search_results'):
        for table in sessionHebrew.find_all('a', class_='search_link_name_big'):
            link = table.get('href')
            return (link)
