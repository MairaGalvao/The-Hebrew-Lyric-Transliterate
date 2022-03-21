from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import csv
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.views.decorators.csrf import csrf_exempt


inputUser = "שלום"


@csrf_exempt
def main(request):

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
