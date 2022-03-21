from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
import requests
import csv
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def main(request):
    text_with_punctuation = add_punctuation()
    english_string = convert_to_phonetic(text_with_punctuation)
    return JsonResponse({text_with_punctuation, english_string})


def add_punctuation(request):
    listLetters = []
    response = requests.post(
        'https://nakdan-4-0.loadbalancer.dicta.org.il/api', json={
            "task": "nakdan",
            "data": request.body,
            "genre": "modern"
        },
    )
   # print(request.body, '<<<<<<<<<<<<<<<<<<<<<<')

    response.status_code
    data = response.json()
    return HttpResponse(data)


def convert_to_phonetic(request):
    response = requests.post(
        'https://alittlehebrew.com/transliterate/get.php?token=a83f12f84752f7d2099b447daa1746d490379bc983440ad6b08b38c9114b147f&style=210_spanish&syllable=auto&accent=auto&hebrew_text=שָׁלוֹם?',
        json={
            "data": request.body,
        },
        headers={
            "Content-Type": "application/json",
            "Cookie": 'PHPSESSID=c5c738286764224ca1cf8aacc49819be',
            "Connection": 'keep-alive',
            "Referer": 'https://alittlehebrew.com/transliterate/',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            "x-requested-with": 'XMLHttpRequest',
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": 'cors',
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-IE,en-US;q=0.9,en;q=0.8,he;q=0.7"
        },
    )
    response.status_code
    data = response.json()
    return(data)
